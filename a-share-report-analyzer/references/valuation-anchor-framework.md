# 行业估值方法库与版本核查

`valuation_anchors/*.json` 保存子行业常用方法、适用条件、周期背景与来源。它是研究起点；市场当前流行的估值语言不能证明内在价值，也不能覆盖普通股现金流、资本约束和会计事实。

## 使用步骤

1. 确认子行业后，用 `scripts/check_valuation_anchor.py --sub-industry "<子行业>" --as-of-date YYYY-MM-DD` 检查记录。匹配不确定时先用 `--list` 查看，不强套相近行业或境外市场记录。
2. `ok` 只表示记录日期未过期。仍须核对来源、研究截止日可获得性、`valid_when` / `invalid_when`、公司特征及近期重大事件；不能直接把记录内周期判断当作当前事实。
3. `expired` 或 `missing` 时，用当前可追溯证据在报告内重建方法依据；有必要才保存为新记录。不能仅改日期来“刷新”。`not_yet_available` 表示记录晚于研究截止日，应寻找当时版本或当时已公开的证据。
4. 原记录是否过期与公司是否可估值分开。只要独立证据足以支持方法，仍可给出估值并说明替代依据；若关键证据不足，则标条件性或暂缓，经营研究可以完成。

## 日期与事件

记录优先用 `refresh_interval_days` 与 `next_review_due`。快速变化科技行业通常100天复核，成熟/消费/周期行业通常190天；这些是维护窗口，不是有效性保证。重大政策、资本约束、行业盈利模式或价格周期变化可使记录在日期到期前失效。

历史研究不得使用研究截止日之后的记录或来源。日期检查工具不能识别网页后续修订和记录内全部引用日期，分析者须另核对。

## 保留的记录结构

沿用现有字段，避免破坏已有数据：

- 标识：`anchor_id`、`display_name`、`sector`、`sub_industry`、`aliases`。
- 版本：`last_updated`、`next_review_due`、`refresh_interval_days`。
- 方法：`primary_anchor`、`secondary_anchors`、`weak_or_floor_anchors`、`disabled_anchors`。
- 依据：`current_cycle_state`、`anchor_switch_rationale`、`valid_when`、`invalid_when`、`peer_set`、`market_pricing_language`、`key_cycle_indicators`、`confidence`、`sources`、`analyst_notes`。

更新时引用具体材料、日期、URL与关键依据，不只列机构主页。将稳定行业原则与会变化的周期假设分开；跨市场公司可作业务参照，但监管、风险溢价、会计、币种与股份类别不能直接照搬。

## 如何选方法

主方法先回答企业如何产生可分配收益，再考虑市场参照。方法库中的 `weight` 是定性提示，不是机械加权系数。

- 银行：普通股PB-ROE、剩余收益或资本约束下股利模型；PB-ROE与股利模型可能代数相关，不冒充独立交叉验证。
- 稳定企业：正常化PE、FCF、DCF或EV/经营利润，按可见度及资本需要选择。
- 周期/商品：周期正常化盈利、NAV/DCF及显式价格情景；账面价值只作经核验的参照，不是自动保底价。
- 亏损/转型科技：收入或毛利、正常化利润、SOTP等需有利润率、资本消耗、稀释与转正约束；历史增长率不直接用于未来估值。
- 管线研发：风险调整现金流需披露成功概率、里程碑与现金存续期，缺乏证据不凭行业倍数硬估。

选择经济视角不同的交叉检查；同行/历史倍数可供比较，但安全边际价格不是第二个独立估值。输出方法版本、适用性判断、主方法/交叉方法及推翻条件。商品、汇率或利率假设与 `macro-policy-transmission.md`、`market-liquidity-expectations.md` 共用一次假设调整记录。

日期检查的 `action_required` 提示分别是 `verify_sources_and_applicability`、`refresh_evidence_before_valuation`、`establish_method_from_current_evidence`、`use_record_available_at_cutoff`。单记录命令退出码：0=日期可用，1=过期，2=缺失，3=晚于截止日；`--list` 返回全部状态供逐项检查。
