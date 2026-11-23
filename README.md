# fesilent-ai-figure (`scientific-figure` Skill)

## 技能入口

- **Codex 科研示意图直出**使用 [`scientific-figure-authoring`](skills/scientific-figure-authoring/SKILL.md)。支持图像生成、局部编辑和审图，包含个人 C4D 风格参考、原件复用和球棍质感校准。
- **SVG 合成工作流**使用仓库根目录的 [`scientific-figure`](SKILL.md)，安装和使用方法见下文。

安装 Codex 直出技能时，从 GitHub 选择 `skills/scientific-figure-authoring` 子目录安装到用户技能目录（默认 `~/.agents/skills`）。安装后用 `$scientific-figure-authoring` 调用。

## 仓库根目录工作流

一个用于 AI Agent 的**顶刊级、零 AI 味通用理工科科研示意图**制作技能（Skill）。

## 设计理念

同行一眼识别科研图“AI 味”的本质，不是反感工具本身，而是反感**装饰性熵增（无意义发光/霓虹渐变/飘带）、约束真空区脑补、实例不一致、几何与标注混融**带来的学术不可信感。

本 Skill 摒弃“写长 Prompt 让文生图直出整图”的传统做法，采用**四阶段解耦编译流水线**：

1. **阶段 0 · 信息架构师**：先拆解对照组、多尺度层级、3–4 色学术语义色板与复用清单，严禁直接画图。
2. **阶段 1 · 分路资产生产**：2D 机理/框架/化学式/放大框强制纯 SVG 矢量；复杂有机/3D 固体材质仅允许“一图一物、纯白底、无字无发光”隔离生成，并用 `clean_asset.py` 自动透明抠图与去饱和。
3. **阶段 2 · 统一矢量合成与高清渲染**：通过 HTML/SVG 统一拼装底层素材与全局矢量标注层（字体、上下标、箭头、放大引线），调用本机无头 Chrome（`render_figure.py`）输出 2x/3x 出版级 PNG 与可选矢量 PDF。
4. **阶段 3 · 双层“反 AI 味”门禁**：先过脚本客观体检（`audit_figure.py` 检测纯白底、霓虹高饱和像素占比、暗黑占比与分辨率），再对照 6 项鉴伪清单做视觉审查。

## 目录结构

```text
.
├── SKILL.md                           # Agent 技能主指令（已对齐 C4D 科研成品风格）
├── assets/
│   └── style-references/              # 5 张 C4D 科研成品风格锚点参考图
├── references/
│   ├── c4d-style-guide.md             # C4D 高调粉彩哑光风格 DNA 与场景对照表
│   ├── visual-spec.md                 # C4D 粉彩 / Nature / Cell / IEEE 色板与排版规范
│   ├── anti-ai-checklist.md           # 6 大反 AI 味鉴伪验收清单
│   └── isolated-asset-prompts.md      # C4D 风格对齐的隔离式文生图提示词模板
└── scripts/
    ├── render_figure.py               # 无头 Chrome 高清 PNG / PDF 渲染脚本
    ├── clean_asset.py                 # 边缘泛洪透明抠图 + 去灰底/压饱和度后处理脚本
    └── audit_figure.py                # 自动化反 AI 味客观指标体检脚本
```

## 环境要求

- Python 3（依赖 `Pillow`、`numpy`）
- Google Chrome / Chromium（用于无头高清渲染）

## 安装方式

将本仓库克隆到你的全局 Agent Skills 目录（以 Antigravity / Gemini 为例）：

```bash
git clone https://github.com/id399-dzx/fesilent-ai-figure.git ~/.gemini/config/skills/scientific-figure
```

## 脚本快速用法

```bash
# 1. 清理隔离式素材（白底转透明 + 轻度压饱和度）
python3 scripts/clean_asset.py --input raw.png --output clean.png --desaturate 0.12

# 2. 渲染 HTML/SVG 科研图为 2x 高清 PNG（可选导出矢量 PDF）
python3 scripts/render_figure.py --html figure.html --output figure.png --width 1600 --height 960 --scale 2 --pdf figure.pdf

# 3. 运行反 AI 味客观体检门禁
python3 scripts/audit_figure.py --image figure.png
```
