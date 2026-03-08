# AgentSkills

自己维护的一组可复用 Agent Skills，目前主要覆盖：

- `jobTarget`：社招岗位价值评估、简历匹配、外部信号核验、反问设计
- `static-cigar-butt-analyzer`：静态价值型烟蒂股分析，适用于净资产折价、资产支撑、控股折价、事件驱动与高股息破净框架

## 仓库结构

每个 skill 目录都尽量采用通用结构：

```text
<skill-name>/
├── SKILL.md
├── scripts/
├── references/
├── assets/ or templates/
├── agents/openai.yaml      # Codex / OpenAI 风格元数据
└── claude/CLAUDE.md        # Claude Code 附加说明（可选）
```

说明：

- `SKILL.md` 是通用核心入口，`Codex`、`Claude Code`、`Qoder` 都可复用。
- `agents/openai.yaml` 用于 `Codex/OpenAI` 风格的展示元数据。
- `claude/CLAUDE.md` 用于补充 `Claude Code` 的调用和运行提示。
- `Qoder` 当前不要求额外清单文件，直接识别 `SKILL.md`。

## 安装方式

### 1. Codex

Codex 本地 skills 目录通常在 `$CODEX_HOME/skills/`。把需要的 skill 目录拷贝或软链进去即可。

示例：

```bash
mkdir -p "$CODEX_HOME/skills"
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" "$CODEX_HOME/skills/jobTarget"
ln -s "/Users/hexingyuan/CodeProjects/skills/static-cigar-butt-analyzer" "$CODEX_HOME/skills/static-cigar-butt-analyzer"
```

如果不想使用软链，也可以直接复制目录：

```bash
cp -R "/Users/hexingyuan/CodeProjects/skills/jobTarget" "$CODEX_HOME/skills/"
cp -R "/Users/hexingyuan/CodeProjects/skills/static-cigar-butt-analyzer" "$CODEX_HOME/skills/"
```

### 2. Claude Code

根据 Claude Code skills 文档，个人级 skills 可放在 `~/.claude/skills/<skill-name>/SKILL.md`，项目级 skills 可放在 `.claude/skills/<skill-name>/SKILL.md`。

个人级安装示例：

```bash
mkdir -p ~/.claude/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" ~/.claude/skills/jobTarget
ln -s "/Users/hexingyuan/CodeProjects/skills/static-cigar-butt-analyzer" ~/.claude/skills/static-cigar-butt-analyzer
```

项目级安装示例：

```bash
mkdir -p .claude/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" .claude/skills/jobTarget
ln -s "/Users/hexingyuan/CodeProjects/skills/static-cigar-butt-analyzer" .claude/skills/static-cigar-butt-analyzer
```

`claude/CLAUDE.md` 不是必需文件，但用于补充 Claude Code 的推荐调用方式和运行前提。

### 3. Qoder

Qoder CLI 官方文档使用 `~/.qoder/skills/<skill-name>/SKILL.md`；QoderWork 文档中也有 `~/.qoderwork/skills/<skill-name>/SKILL.md` 的安装方式。你使用哪个产品，就放到对应目录。

Qoder CLI 示例：

```bash
mkdir -p ~/.qoder/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" ~/.qoder/skills/jobTarget
ln -s "/Users/hexingyuan/CodeProjects/skills/static-cigar-butt-analyzer" ~/.qoder/skills/static-cigar-butt-analyzer
```

QoderWork 示例：

```bash
mkdir -p ~/.qoderwork/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" ~/.qoderwork/skills/jobTarget
ln -s "/Users/hexingyuan/CodeProjects/skills/static-cigar-butt-analyzer" ~/.qoderwork/skills/static-cigar-butt-analyzer
```

## 从远端仓库安装

如果你是从 GitHub 安装，推荐先 clone 到本地再软链：

```bash
git clone git@github.com:hxy1997/AgentSkills.git ~/AgentSkills
```

然后把需要的 skill 软链到对应平台目录：

```bash
ln -s ~/AgentSkills/jobTarget "$CODEX_HOME/skills/jobTarget"
ln -s ~/AgentSkills/static-cigar-butt-analyzer "$CODEX_HOME/skills/static-cigar-butt-analyzer"
ln -s ~/AgentSkills/jobTarget ~/.claude/skills/jobTarget
ln -s ~/AgentSkills/static-cigar-butt-analyzer ~/.claude/skills/static-cigar-butt-analyzer
ln -s ~/AgentSkills/jobTarget ~/.qoder/skills/jobTarget
ln -s ~/AgentSkills/static-cigar-butt-analyzer ~/.qoder/skills/static-cigar-butt-analyzer
```

## 平台兼容说明

- `jobTarget`
  - Codex: 支持
  - Claude Code: 支持
  - Qoder: 支持
- `static-cigar-butt-analyzer`
  - Codex: 支持
  - Claude Code: 通过 `SKILL.md` 使用
  - Qoder: 通过 `SKILL.md` 使用

## Skills 简介

### `jobTarget`

- 适合社招岗位分析、简历匹配、职位信号核验和面试反问设计。
- 内含脚本、参考资料和模板，可直接复用到求职分析场景。

### `static-cigar-butt-analyzer`

- 面向深度价值 / 烟蒂股分析，核心看三件事：资产垫、低维护烧损、价值兑现路径。
- 支持 `HKFRS/IFRS`、`US-GAAP`、`CN-GAAP` 三类口径。
- 输出严格 Markdown 报告，适合做 `T0/T1/T2 NAV`、`A/B/C` 子类型判断、`Fact Check 22 项` 以及入场/退出方案。
- 当前目录包含：
  - `SKILL.md`
  - `references/workflow.md`
  - `references/accounting-mapping.md`
  - `references/report-template.md`

## 维护建议

- 新增 skill 时，至少补齐 `SKILL.md`
- 如果需要更好的 Codex 展示，补 `agents/openai.yaml`
- 如果需要更好的 Claude Code 落地指引，补 `claude/CLAUDE.md`
- 若 skill 依赖外部仓库、虚拟环境或数据目录，必须在 `SKILL.md` 中写清楚
