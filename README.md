# fesilent-ai-figure

`scientific-figure-authoring` 用图像模型直接生成、编辑和重绘科研示意图，默认交付透明背景 PNG（RGBA）。适用于机制图、方法图、图文摘要、设备结构图和拟三维剖面，也可单独用于审图。

出图前先确认图意和用户偏好。领域惯例由技能查阅资料，整体方向模糊时可生成 2–3 张独立候选图。局部修改时逐区核对原件复用、结构替换和放大窗。指定 C4D 材质参考时，先校准代表部件，再把配色、亮度和质感应用到整图。

## 在 Codex 中安装

将仓库根目录安装到用户技能目录。首次安装时运行以下命令。

```bash
git clone https://github.com/id399-dzx/fesilent-ai-figure.git ~/.agents/skills/scientific-figure-authoring
```

安装后用 `$scientific-figure-authoring` 调用。出图需要当前客户端提供图像生成或编辑工具，例如 Codex 的 `imagegen`。此前从 `skills/scientific-figure-authoring/` 安装的用户，后续更新请使用仓库根目录。此前使用仓库旧版 `scientific-figure` 的用户，更新后使用新版技能名 `scientific-figure-authoring`。

## 技能资料

- [技能入口](SKILL.md)
- [直出提示词与局部返修示例](references/direct-image-prompts.md)
- [成图审查与材质校准](references/figure-review.md)
- [C4D 科研制图风格参考](references/personal-c4d-style.md)
- [顶刊构图范式与进阶视觉语法](references/composition-patterns.md)
