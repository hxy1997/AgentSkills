# AgentSkills

自己维护的一组可复用 Agent Skills，目前主要覆盖：

- `jobTarget`：社招岗位价值评估、简历匹配、外部信号核验、反问设计

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
```

如果不想使用软链，也可以直接复制目录：

```bash
cp -R "/Users/hexingyuan/CodeProjects/skills/jobTarget" "$CODEX_HOME/skills/"
```

### 2. Claude Code

根据 Claude Code skills 文档，个人级 skills 可放在 `~/.claude/skills/<skill-name>/SKILL.md`，项目级 skills 可放在 `.claude/skills/<skill-name>/SKILL.md`。

个人级安装示例：

```bash
mkdir -p ~/.claude/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" ~/.claude/skills/jobTarget
```

项目级安装示例：

```bash
mkdir -p .claude/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" .claude/skills/jobTarget
```

`claude/CLAUDE.md` 不是必需文件，但用于补充 Claude Code 的推荐调用方式和运行前提。

### 3. Qoder

Qoder CLI 官方文档使用 `~/.qoder/skills/<skill-name>/SKILL.md`；QoderWork 文档中也有 `~/.qoderwork/skills/<skill-name>/SKILL.md` 的安装方式。你使用哪个产品，就放到对应目录。

Qoder CLI 示例：

```bash
mkdir -p ~/.qoder/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" ~/.qoder/skills/jobTarget
```

QoderWork 示例：

```bash
mkdir -p ~/.qoderwork/skills
ln -s "/Users/hexingyuan/CodeProjects/skills/jobTarget" ~/.qoderwork/skills/jobTarget
```

## 从远端仓库安装

如果你是从 GitHub 安装，推荐先 clone 到本地再软链：

```bash
git clone git@github.com:hxy1997/AgentSkills.git ~/AgentSkills
```

然后把需要的 skill 软链到对应平台目录：

```bash
ln -s ~/AgentSkills/jobTarget "$CODEX_HOME/skills/jobTarget"
ln -s ~/AgentSkills/jobTarget ~/.claude/skills/jobTarget
ln -s ~/AgentSkills/jobTarget ~/.qoder/skills/jobTarget
```

## 平台兼容说明

- `jobTarget`
  - Codex: 支持
  - Claude Code: 支持
  - Qoder: 支持

## 维护建议

- 新增 skill 时，至少补齐 `SKILL.md`
- 如果需要更好的 Codex 展示，补 `agents/openai.yaml`
- 如果需要更好的 Claude Code 落地指引，补 `claude/CLAUDE.md`
- 若 skill 依赖外部仓库、虚拟环境或数据目录，必须在 `SKILL.md` 中写清楚
