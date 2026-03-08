# Accounting Mapping

## Core line-item mapping

| 项目 | HKFRS / IFRS | US-GAAP | CN-GAAP |
|:-----|:-------------|:--------|:--------|
| 现金及等价物 | Cash and cash equivalents | Cash and cash equivalents | 货币资金 |
| 短期理财/有价证券 | Financial assets at FVTPL (short-term) | Trading investments / Short-term investments | 交易性金融资产 / 其他货币资金 |
| 定期存款(>3个月) | Other financial assets / time deposits | Certificates of deposit | 其他流动资产（需手动识别） |
| 应收账款 | Trade receivables | Accounts receivable | 应收账款 |
| 存货 | Inventories | Inventories | 存货 |
| 合同负债/预收款 | Contract liabilities | Deferred revenue | 合同负债 / 预收款项 |
| 短期借款 | Short-term bank borrowings | Short-term debt | 短期借款 |
| 长期借款 | Long-term bank borrowings | Long-term debt | 长期借款 |
| 总负债 | Total liabilities | Total liabilities | 负债合计 |
| 经营性现金流 | Cash generated from operations / Net cash from operating activities | Net cash provided by operating activities | 经营活动产生的现金流量净额 |
| 资本开支 | Purchase of PPE / capex additions | Capital expenditures | 购建固定资产、无形资产和其他长期资产支付的现金 |
| 商誉 | Goodwill | Goodwill | 商誉 |

## Extraction notes

- Prefer statement face values first, then use notes for breakdown.
- Separate unrestricted cash from restricted cash when possible.
- Pull lease liabilities into interest-bearing debt where the standard puts them on balance sheet.
- Identify listed securities separately from opaque Level 3 financial assets.
- For interim reports, balance-sheet values are point-in-time and can be used directly; income-statement and cash-flow items may need annualization and must be labeled.

## Common no-guess areas

If not disclosed clearly, do not estimate:

- Restricted cash ratio
- Aging bucket over 90 days
- Related-party AR share
- Capital commitments
- Pension funding gap
- Level 3 asset composition
- Top-5 customer concentration
- Q4 revenue share when only annual totals are shown
