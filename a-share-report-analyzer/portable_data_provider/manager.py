from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from .fundamental_adapter import AkshareFundamentalAdapter
from .realtime_types import RealtimeSource, UnifiedRealtimeQuote, safe_float, safe_int


logger = logging.getLogger(__name__)

ETF_PREFIXES = ("51", "52", "56", "58", "15", "16", "18")


def normalize_stock_code(stock_code: str) -> str:
    code = (stock_code or "").strip()
    upper = code.upper()
    if upper.startswith(("SH", "SZ", "BJ")) and "." not in upper[:3]:
        candidate = code[2:]
        if candidate.isdigit() and len(candidate) in (5, 6):
            return candidate
    if "." in code:
        base, suffix = code.rsplit(".", 1)
        if suffix.upper() in {"SH", "SZ", "SS", "BJ"} and base.isdigit():
            return base
        if suffix.upper() == "HK" and base.isdigit() and 1 <= len(base) <= 5:
            return f"HK{base.zfill(5)}"
    if upper.startswith("HK"):
        digits = upper[2:]
        if digits.isdigit() and 1 <= len(digits) <= 5:
            return f"HK{digits.zfill(5)}"
    return upper if upper.isalpha() else code


def _is_us_market(code: str) -> bool:
    text = (code or "").strip().upper()
    return text.isalpha() and 1 <= len(text) <= 5


def _is_hk_market(code: str) -> bool:
    text = (code or "").strip().upper()
    if text.startswith("HK"):
        digits = text[2:]
        return digits.isdigit() and 1 <= len(digits) <= 5
    return text.isdigit() and len(text) == 5


def _is_etf_code(code: str) -> bool:
    normalized = normalize_stock_code(code)
    return normalized.isdigit() and len(normalized) == 6 and normalized.startswith(ETF_PREFIXES)


def _market_tag(code: str) -> str:
    if _is_us_market(code):
        return "us"
    if _is_hk_market(code):
        return "hk"
    return "cn"


def _first_present(mapping: pd.Series | Dict[str, Any], candidates: List[str]) -> Any:
    for key in candidates:
        if isinstance(mapping, pd.Series):
            if key in mapping.index:
                return mapping.get(key)
        elif key in mapping:
            return mapping.get(key)
    return None


class DataFetcherManager:
    """Portable subset of the external data manager used by this skill."""

    def __init__(self) -> None:
        self._fundamental_adapter = AkshareFundamentalAdapter()
        self._stock_name_cache: Dict[str, str] = {}
        self._realtime_cache: Dict[str, Dict[str, Any]] = {}
        self._realtime_cache_ttl = 1200

    def _read_cache(self, cache_key: str) -> Optional[pd.DataFrame]:
        item = self._realtime_cache.get(cache_key)
        if not item:
            return None
        if time.time() - float(item.get("ts", 0.0)) > self._realtime_cache_ttl:
            self._realtime_cache.pop(cache_key, None)
            return None
        return item.get("data")

    def _write_cache(self, cache_key: str, df: pd.DataFrame) -> None:
        self._realtime_cache[cache_key] = {"ts": time.time(), "data": df}

    def _get_realtime_quote_efinance(self, stock_code: str) -> Optional[UnifiedRealtimeQuote]:
        try:
            import efinance as ef
        except Exception:
            return None

        cache_key = "efinance_etf" if _is_etf_code(stock_code) else "efinance_stock"
        df = self._read_cache(cache_key)
        if df is None:
            try:
                if _is_etf_code(stock_code):
                    df = ef.stock.get_realtime_quotes(["ETF"])
                else:
                    df = ef.stock.get_realtime_quotes()
                if isinstance(df, pd.DataFrame) and not df.empty:
                    self._write_cache(cache_key, df)
            except Exception as exc:
                logger.debug("efinance realtime quote failed for %s: %s", stock_code, exc)
                return None

        if df is None or df.empty:
            return None

        code_col = "股票代码" if "股票代码" in df.columns else "code"
        code_series = df[code_col].astype(str).str.upper().str.replace(r"^(SH|SZ|BJ)", "", regex=True).str.zfill(6)
        row = df[code_series == str(stock_code).strip().upper().replace("HK", "").zfill(6)]
        if row.empty:
            return None

        item = row.iloc[0]
        quote = UnifiedRealtimeQuote(
            code=normalize_stock_code(stock_code),
            name=str(_first_present(item, ["股票名称", "名称", "name"]) or ""),
            source=RealtimeSource.EFINANCE,
            price=safe_float(_first_present(item, ["最新价", "最新价格", "price"])),
            change_pct=safe_float(_first_present(item, ["涨跌幅", "pct_chg"])),
            change_amount=safe_float(_first_present(item, ["涨跌额", "change"])),
            volume=safe_int(_first_present(item, ["成交量", "volume"])),
            amount=safe_float(_first_present(item, ["成交额", "amount"])),
            turnover_rate=safe_float(_first_present(item, ["换手率", "turnover_rate"])),
            amplitude=safe_float(_first_present(item, ["振幅", "amplitude"])),
            high=safe_float(_first_present(item, ["最高", "high"])),
            low=safe_float(_first_present(item, ["最低", "low"])),
            open_price=safe_float(_first_present(item, ["今开", "开盘", "open"])),
            pre_close=safe_float(_first_present(item, ["昨收", "pre_close"])),
            volume_ratio=safe_float(_first_present(item, ["量比", "volume_ratio"])),
            pe_ratio=safe_float(_first_present(item, ["市盈率", "PE", "pe_ratio"])),
            pb_ratio=safe_float(_first_present(item, ["市净率", "PB", "pb_ratio"])),
            total_mv=safe_float(_first_present(item, ["总市值", "total_mv"])),
            circ_mv=safe_float(_first_present(item, ["流通市值", "circ_mv"])),
        )
        return quote if quote.has_basic_data() else None

    def _get_realtime_quote_tushare(self, stock_code: str) -> Optional[UnifiedRealtimeQuote]:
        token = os.getenv("TUSHARE_TOKEN")
        if not token:
            return None

        normalized = normalize_stock_code(stock_code)
        try:
            import tushare as ts
        except Exception:
            return None

        try:
            api = ts.pro_api(token)
            suffix = "SH" if normalized.startswith(("6", "5", "9")) else "SZ"
            ts_code = f"{normalized}.{suffix}"
            df = api.daily_basic(ts_code=ts_code, limit=1)
            quote_df = ts.get_realtime_quotes(normalized)
            if quote_df is None or quote_df.empty:
                return None
            row = quote_df.iloc[0]
            basic = df.iloc[0] if isinstance(df, pd.DataFrame) and not df.empty else {}
            quote = UnifiedRealtimeQuote(
                code=normalized,
                name=str(_first_present(row, ["name", "名称"]) or ""),
                source=RealtimeSource.TUSHARE,
                price=safe_float(_first_present(row, ["price", "当前价"])),
                open_price=safe_float(_first_present(row, ["open", "今开"])),
                pre_close=safe_float(_first_present(row, ["pre_close", "昨收"])),
                high=safe_float(_first_present(row, ["high", "最高"])),
                low=safe_float(_first_present(row, ["low", "最低"])),
                volume=safe_int(_first_present(row, ["volume", "成交量"])),
                amount=safe_float(_first_present(row, ["amount", "成交额"])),
                pe_ratio=safe_float(_first_present(basic, ["pe", "pe_ttm"])),
                pb_ratio=safe_float(_first_present(basic, ["pb"])),
                total_mv=safe_float(_first_present(basic, ["total_mv"])),
                circ_mv=safe_float(_first_present(basic, ["circ_mv"])),
            )
            if quote.price is not None and quote.pre_close:
                quote.change_amount = quote.price - quote.pre_close
                if quote.pre_close:
                    quote.change_pct = (quote.change_amount / quote.pre_close) * 100.0
            return quote if quote.has_basic_data() else None
        except Exception as exc:
            logger.debug("tushare realtime quote failed for %s: %s", stock_code, exc)
            return None

    def _get_realtime_quote_akshare(self, stock_code: str) -> Optional[UnifiedRealtimeQuote]:
        normalized = normalize_stock_code(stock_code)
        if _market_tag(normalized) != "cn":
            return None
        try:
            import akshare as ak
        except Exception:
            return None

        cache_key = "akshare_spot_em"
        df = self._read_cache(cache_key)
        if df is None:
            try:
                df = ak.stock_zh_a_spot_em()
                if isinstance(df, pd.DataFrame) and not df.empty:
                    self._write_cache(cache_key, df)
            except Exception as exc:
                logger.debug("akshare realtime quote failed for %s: %s", stock_code, exc)
                return None

        if df is None or df.empty:
            return None

        code_col = "代码" if "代码" in df.columns else "code"
        row = df[df[code_col].astype(str) == normalized]
        if row.empty:
            return None

        item = row.iloc[0]
        quote = UnifiedRealtimeQuote(
            code=normalized,
            name=str(_first_present(item, ["名称", "name"]) or ""),
            source=RealtimeSource.AKSHARE,
            price=safe_float(_first_present(item, ["最新价", "最新"])),
            change_pct=safe_float(_first_present(item, ["涨跌幅"])),
            change_amount=safe_float(_first_present(item, ["涨跌额"])),
            volume=safe_int(_first_present(item, ["成交量"])),
            amount=safe_float(_first_present(item, ["成交额"])),
            turnover_rate=safe_float(_first_present(item, ["换手率"])),
            amplitude=safe_float(_first_present(item, ["振幅"])),
            high=safe_float(_first_present(item, ["最高"])),
            low=safe_float(_first_present(item, ["最低"])),
            open_price=safe_float(_first_present(item, ["今开"])),
            pre_close=safe_float(_first_present(item, ["昨收"])),
            pe_ratio=safe_float(_first_present(item, ["市盈率-动态", "市盈率"])),
            pb_ratio=safe_float(_first_present(item, ["市净率"])),
            total_mv=safe_float(_first_present(item, ["总市值"])),
            circ_mv=safe_float(_first_present(item, ["流通市值"])),
        )
        return quote if quote.has_basic_data() else None

    @staticmethod
    def _merge_quote_fields(primary: UnifiedRealtimeQuote, secondary: UnifiedRealtimeQuote) -> UnifiedRealtimeQuote:
        for field_name in (
            "change_pct",
            "change_amount",
            "volume",
            "amount",
            "volume_ratio",
            "turnover_rate",
            "amplitude",
            "open_price",
            "high",
            "low",
            "pre_close",
            "pe_ratio",
            "pb_ratio",
            "total_mv",
            "circ_mv",
        ):
            if getattr(primary, field_name) is None:
                value = getattr(secondary, field_name)
                if value is not None:
                    setattr(primary, field_name, value)
        if not primary.name and secondary.name:
            primary.name = secondary.name
        return primary

    def get_realtime_quote(self, stock_code: str, *, log_final_failure: bool = True) -> Optional[UnifiedRealtimeQuote]:
        normalized = normalize_stock_code(stock_code)
        sources = [
            self._get_realtime_quote_efinance,
            self._get_realtime_quote_tushare,
            self._get_realtime_quote_akshare,
        ]
        primary = None
        for getter in sources:
            quote = getter(normalized)
            if quote is None:
                continue
            if primary is None:
                primary = quote
            else:
                primary = self._merge_quote_fields(primary, quote)
        if primary is None and log_final_failure:
            logger.debug("All portable realtime quote sources failed for %s", stock_code)
        return primary

    def get_stock_name(self, stock_code: str, allow_realtime: bool = True) -> Optional[str]:
        normalized = normalize_stock_code(stock_code)
        cached = self._stock_name_cache.get(normalized)
        if cached:
            return cached

        if allow_realtime:
            quote = self.get_realtime_quote(normalized, log_final_failure=False)
            if quote and quote.name:
                self._stock_name_cache[normalized] = quote.name
                return quote.name

        token = os.getenv("TUSHARE_TOKEN")
        if token and normalized.isdigit():
            try:
                import tushare as ts

                api = ts.pro_api(token)
                suffix = "SH" if normalized.startswith(("6", "5", "9")) else "SZ"
                df = api.stock_basic(ts_code=f"{normalized}.{suffix}", fields="ts_code,name")
                if isinstance(df, pd.DataFrame) and not df.empty:
                    name = str(df.iloc[0].get("name") or "")
                    if name:
                        self._stock_name_cache[normalized] = name
                        return name
            except Exception as exc:
                logger.debug("tushare stock name lookup failed for %s: %s", stock_code, exc)

        return None

    @staticmethod
    def _normalize_belong_boards(raw_data: Any) -> List[Dict[str, Any]]:
        if raw_data is None:
            return []

        rows: List[Dict[str, Any]] = []
        if isinstance(raw_data, pd.DataFrame):
            iterable = raw_data.to_dict("records")
        elif isinstance(raw_data, list):
            iterable = raw_data
        elif isinstance(raw_data, dict):
            iterable = [raw_data]
        else:
            return []

        dedupe = set()
        for item in iterable:
            if not isinstance(item, dict):
                continue
            name = (
                item.get("板块名称")
                or item.get("板块")
                or item.get("所属板块")
                or item.get("板块名")
                or item.get("industry")
                or item.get("行业")
                or item.get("name")
            )
            code = item.get("板块代码") or item.get("代码") or item.get("code")
            board_type = item.get("板块类型") or item.get("类别") or item.get("type")
            if name is None:
                continue
            normalized = {"name": str(name).strip()}
            if not normalized["name"]:
                continue
            if code not in (None, ""):
                normalized["code"] = str(code).strip()
            if board_type not in (None, ""):
                normalized["type"] = str(board_type).strip()
            dedupe_key = (normalized["name"], normalized.get("code"), normalized.get("type"))
            if dedupe_key in dedupe:
                continue
            dedupe.add(dedupe_key)
            rows.append(normalized)
        return rows

    def get_belong_boards(self, stock_code: str) -> List[Dict[str, Any]]:
        normalized = normalize_stock_code(stock_code)
        if _market_tag(normalized) != "cn":
            return []

        try:
            import efinance as ef
        except Exception:
            return []

        try:
            raw = ef.stock.get_belong_board(normalized)
        except Exception as exc:
            logger.debug("efinance belong boards failed for %s: %s", stock_code, exc)
            return []
        return self._normalize_belong_boards(raw)

    @staticmethod
    def _has_meaningful_payload(payload: Dict[str, Any]) -> bool:
        for value in payload.values():
            if isinstance(value, dict):
                if DataFetcherManager._has_meaningful_payload(value):
                    return True
            elif isinstance(value, list):
                if value:
                    return True
            elif value not in (None, "", "not_supported"):
                return True
        return False

    @staticmethod
    def _build_block(status: str, data: Dict[str, Any], source_chain: List[str], errors: List[str]) -> Dict[str, Any]:
        return {
            "status": status,
            "data": data,
            "source_chain": source_chain,
            "errors": errors,
        }

    def get_fundamental_context(self, stock_code: str, budget_seconds: Optional[float] = None) -> Dict[str, Any]:
        normalized = normalize_stock_code(stock_code)
        market = _market_tag(normalized)
        context: Dict[str, Any] = {
            "market": market,
            "valuation": {},
            "growth": {},
            "earnings": {},
            "institution": {},
            "capital_flow": {},
            "dragon_tiger": {},
            "boards": {},
            "belong_boards": [],
            "coverage": {},
            "source_chain": [],
            "errors": [],
        }

        if market != "cn":
            context["status"] = "not_supported"
            context["errors"].append("market not supported")
            return context

        quote = self.get_realtime_quote(normalized, log_final_failure=False)
        valuation_payload = {
            "pe_ratio": getattr(quote, "pe_ratio", None) if quote else None,
            "pb_ratio": getattr(quote, "pb_ratio", None) if quote else None,
            "total_mv": getattr(quote, "total_mv", None) if quote else None,
            "circ_mv": getattr(quote, "circ_mv", None) if quote else None,
        }
        valuation_status = "ok" if self._has_meaningful_payload(valuation_payload) else "not_supported"
        context["valuation"] = self._build_block(
            valuation_status,
            valuation_payload,
            [f"realtime_quote:{quote.source.value}" if quote else "realtime_quote:none"],
            [],
        )

        bundle = self._fundamental_adapter.get_fundamental_bundle(normalized)
        bundle_errors = list(bundle.get("errors", [])) if isinstance(bundle, dict) else []
        growth_data = bundle.get("growth", {}) if isinstance(bundle, dict) else {}
        earnings_data = bundle.get("earnings", {}) if isinstance(bundle, dict) else {}
        institution_data = bundle.get("institution", {}) if isinstance(bundle, dict) else {}
        bundle_sources = list(bundle.get("source_chain", [])) if isinstance(bundle, dict) else []
        bundle_status = str(bundle.get("status", "not_supported")) if isinstance(bundle, dict) else "not_supported"

        context["growth"] = self._build_block(
            "ok" if self._has_meaningful_payload(growth_data) else bundle_status,
            growth_data if isinstance(growth_data, dict) else {},
            bundle_sources,
            bundle_errors,
        )
        context["earnings"] = self._build_block(
            "ok" if self._has_meaningful_payload(earnings_data) else bundle_status,
            earnings_data if isinstance(earnings_data, dict) else {},
            bundle_sources,
            bundle_errors,
        )
        context["institution"] = self._build_block(
            "ok" if self._has_meaningful_payload(institution_data) else bundle_status,
            institution_data if isinstance(institution_data, dict) else {},
            bundle_sources,
            bundle_errors,
        )

        capital_flow = self._fundamental_adapter.get_capital_flow(normalized)
        context["capital_flow"] = self._build_block(
            str(capital_flow.get("status", "not_supported")),
            capital_flow.get("data", {}) if isinstance(capital_flow, dict) else {},
            list(capital_flow.get("source_chain", [])) if isinstance(capital_flow, dict) else [],
            list(capital_flow.get("errors", [])) if isinstance(capital_flow, dict) else [],
        )

        dragon_tiger = self._fundamental_adapter.get_dragon_tiger_flag(normalized)
        context["dragon_tiger"] = self._build_block(
            str(dragon_tiger.get("status", "not_supported")),
            dragon_tiger.get("data", {}) if isinstance(dragon_tiger, dict) else {},
            list(dragon_tiger.get("source_chain", [])) if isinstance(dragon_tiger, dict) else [],
            list(dragon_tiger.get("errors", [])) if isinstance(dragon_tiger, dict) else [],
        )

        belong_boards = self.get_belong_boards(normalized)
        context["belong_boards"] = belong_boards
        context["boards"] = self._build_block(
            "ok" if belong_boards else "not_supported",
            {"belong_boards": belong_boards},
            ["efinance:get_belong_board"] if belong_boards else [],
            [],
        )

        context["coverage"] = {
            "valuation": context["valuation"]["status"],
            "growth": context["growth"]["status"],
            "earnings": context["earnings"]["status"],
            "institution": context["institution"]["status"],
            "capital_flow": context["capital_flow"]["status"],
            "dragon_tiger": context["dragon_tiger"]["status"],
            "boards": context["boards"]["status"],
        }
        context["source_chain"] = (
            context["valuation"]["source_chain"]
            + context["growth"]["source_chain"]
            + context["capital_flow"]["source_chain"]
            + context["dragon_tiger"]["source_chain"]
            + context["boards"]["source_chain"]
        )
        context["errors"] = (
            context["valuation"]["errors"]
            + context["growth"]["errors"]
            + context["earnings"]["errors"]
            + context["institution"]["errors"]
            + context["capital_flow"]["errors"]
            + context["dragon_tiger"]["errors"]
            + context["boards"]["errors"]
        )
        context["status"] = "ok" if any(
            status == "ok" for status in context["coverage"].values()
        ) else "partial"
        if not any(self._has_meaningful_payload(block.get("data", {})) for block in (
            context["valuation"],
            context["growth"],
            context["earnings"],
            context["institution"],
            context["capital_flow"],
            context["dragon_tiger"],
            context["boards"],
        )):
            context["status"] = "not_supported"
        return context
