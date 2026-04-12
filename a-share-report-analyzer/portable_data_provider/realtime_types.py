from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


def safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None:
            return default
        if isinstance(value, str):
            text = value.strip().replace(",", "").replace("%", "")
            if text in {"", "-", "--"}:
                return default
            value = text
        result = float(value)
        if result != result:
            return default
        return result
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    numeric = safe_float(value, default=None)
    if numeric is None:
        return default
    return int(numeric)


class RealtimeSource(Enum):
    EFINANCE = "efinance"
    TUSHARE = "tushare"
    AKSHARE = "akshare"
    FALLBACK = "fallback"


@dataclass
class UnifiedRealtimeQuote:
    code: str
    name: str = ""
    source: RealtimeSource = RealtimeSource.FALLBACK
    price: Optional[float] = None
    change_pct: Optional[float] = None
    change_amount: Optional[float] = None
    volume: Optional[int] = None
    amount: Optional[float] = None
    volume_ratio: Optional[float] = None
    turnover_rate: Optional[float] = None
    amplitude: Optional[float] = None
    open_price: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    pre_close: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    total_mv: Optional[float] = None
    circ_mv: Optional[float] = None

    def has_basic_data(self) -> bool:
        return self.price is not None and self.price > 0

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "code": self.code,
            "name": self.name,
            "source": self.source.value,
        }
        for field_name in (
            "price",
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
            value = getattr(self, field_name)
            if value is not None:
                payload[field_name] = value
        return payload
