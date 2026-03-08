# Output Format

Use this structure for markdown output:

```markdown
# 个股投票结论

- 标的：
- 角色：
- 最终结论：
- 投票结果：

## 结论摘要

## 支持票

## 反对票

## 关键证据

## 风险与证伪条件

## 行动条件

## 原始分析对照

## 数据来源
```

JSON should include these keys:
- `stock`
- `role`
- `verdict`
- `vote_summary`
- `supporting_votes`
- `opposing_votes`
- `evidence`
- `risks`
- `action_conditions`
- `upstream`
- `data_sources`
