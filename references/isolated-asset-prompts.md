# 隔离式文生图资产提示词规范（Isolated Asset Prompts）

本技能仅在**纯 2D SVG 无法表达复杂有机形态或特定 3D 固体材质**时，才允许调用文生图工具，且**严禁生成整张科研图**。

---

## 核心铁律
1. **一图一物**：每次只生成**单个孤立组件**（例如：一个多孔碳颗粒块、一只实验小鼠、一个脂质体剖面、一个工业机械臂），绝不生成包含多模块、空白腔体或对照组的完整场景。
2. **纯白无影底**：强制 `isolated on pure solid white background (#FFFFFF)`，方便 `clean_asset.py` 一键透明抠图。
3. **无字无符号**：强制 `no text, no letters, no numbers, no arrows, no labels, no diagram lines`。
4. **哑光克制材质**：强制哑光粘土/磨砂玻璃/拉丝金属等学术建模质感，彻底封杀霓虹发光与电影渲染。

---

## 必用禁用词清单（Negative Constraints）
在提示词末尾显式排除以下所有 AI 味触发词：
```text
Strictly no text, no letters, no numbers, no arrows, no annotations, no glowing effects, no neon colors, no light trails, no floating sparkles or particles, no sci-fi hologram, no dark background, no dramatic cinematic lighting, no depth of field bokeh, no glossy plastic glare.
```

---

## 标准提示词模板

### 模板 1：3D 学术哑光材质孤立部件（材料/器件/生物大分子）
```text
A single isolated [SUBJECT: e.g., porous carbon electrode block / spherical core-shell nanoparticle with a clean 90-degree cutaway], scientific visualization style rendered in Blender Cycles, clean matte clay and subtle brushed material texture, soft uniform studio ambient occlusion lighting, orthographic isometric view, muted academic color palette ([COLORS: e.g., slate blue and warm neutral gray]), centered and completely isolated on a pure solid white background (#FFFFFF), crisp clean edges. Strictly no text, no arrows, no labels, no glowing particles, no neon gradient, no light trails, no bokeh, no background clutter.
```

### 模板 2：2D 极简科学插画孤立元素（生物/实验动物/植物/解剖局部）
```text
A single isolated [SUBJECT: e.g., laboratory mouse in side profile / cell membrane cross-section], Nature journal scientific illustration style, clean flat 2D vector aesthetic with subtle matte shading, uniform crisp outlines, muted academic colors ([COLORS]), centered on a pure solid white background (#FFFFFF). Strictly no text, no letters, no arrows, no labels, no glow, no decorative background.
```

---

## 生成后的强制加工流程
1. 用 `scripts/clean_asset.py` 去除纯白/微灰背景并转为透明 PNG，同时轻度压制异常饱和度；
2. 将处理后的透明 PNG 作为 `<img src="...">` 或 `<image href="...">` 嵌入 HTML/SVG 合成画布；
3. 在同一张图的多个子图（如 `a` vs `b`）中直接**复用同一份透明 PNG**，确保 100% 实例一致性。
