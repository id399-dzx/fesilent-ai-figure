# 隔离式文生图资产提示词规范（C4D 风格对齐版）

本技能仅在**纯 2D SVG 无法表达复杂 3D 装置、球棍晶格或有机形态**时，才允许调用文生图工具，且**严禁生成整张科研图**。

所有生成的 3D 素材必须严格对齐 `assets/style-references/` 中的 **Cinema 4D 高调清透粉彩哑光科研风**（详见 `references/c4d-style-guide.md`）。

---

## 核心铁律
1. **一图一物**：每次只生成**单个孤立组件**（例如：一台涂布辊压装置、一段碳纳米管晶格、一只白色哑光机械手、一个电池剖面壳体），绝不生成包含多组对比或复杂文字排版的完整场景。
2. **高调清透 C4D 质感**：强制 `Cinema 4D (C4D) standard physical render, bright high-key soft white studio lighting, clean pastel matte clay and smooth satin materials, infinite depth of field (everything sharp)`。
3. **纯白无影底**：默认强制 `isolated on pure solid white background (#FFFFFF), no ground shadow`（俯视光学实验台除外，可指定 `#ECEEEF` 极浅灰底与极柔和接触阴影）。
4. **无字无符号**：强制 `no text, no letters, no numbers, no arrows, no labels, no diagram lines`。

---

## 必用禁用词清单（Negative Constraints）
在提示词末尾显式排除所有破坏 C4D 清透科研风的 AI 味触发词：
```text
Strictly no text, no letters, no numbers, no arrows, no annotations, no glowing effects, no neon colors, no light trails, no floating sparkles or particles, no sci-fi hologram, no dark background, no dramatic shadows, no cinematic lighting, no depth of field bokeh, no glossy oily metal, no grunge or scratches, no vignette.
```

---

## 标准提示词模板（按 C4D 参考题材分类）

### 模板 1：工艺装置 / 器件 / 电芯剖面（对齐 `01-battery-cutaway.png` & `02-roll-to-roll-process.png`）
```text
A single isolated 3D scientific model of [SUBJECT: e.g., roll-to-roll coating machine / cylindrical battery cutaway], rendered in Cinema 4D (C4D) physical renderer style, bright high-key uniform white studio lighting, clean minimalist geometric primitives with subtle beveled edges, smooth pastel matte plastic and light satin aluminum materials, muted pastel color palette ([COLORS: e.g., soft dusty blue #8AA7D6, pastel pink #DFB6C9, warm beige #B39B73, light silver gray #D0D5DC, clear sky blue #8FD3FF]), orthographic or slight isometric view, infinite depth of field with crisp sharp edges throughout, completely isolated on a pure solid white background (#FFFFFF) with no ground shadow. Strictly no text, no arrows, no labels, no glowing particles, no neon gradient, no dark shadows, no cinematic lighting, no bokeh, no grunge.
```

### 模板 2：纳米晶格 / 分子球棍 / 碳管结构（对齐 `03-cnt-graphene-lattice.png`）
```text
A single isolated 3D scientific ball-and-stick molecular model of [SUBJECT: e.g., graphene sheet interwoven with carbon nanotubes and embedded metal nanoclusters], rendered in Cinema 4D (C4D) clean scientific visualization style, bright even diffuse white studio lighting, smooth light silver-gray carbon spheres and cylindrical bonds (#A6AAB0) with crisp royal blue (#3359D6) and warm amber (#E8A33D) nanoparticle spheres, infinite depth of field, sharp clean geometry, isolated on a pure solid white background (#FFFFFF) with no floor shadow. Strictly no text, no labels, no glow, no bokeh, no dark background, no floating dust.
```

### 模板 3：光学/物理仪器部件或仿生洁白机械件（对齐 `04-optical-setup.jpg` & `05-bio-ion-composite.png`）
```text
A single isolated 3D scientific component of [SUBJECT: e.g., minimalist white matte bionic robotic hand / optical beam splitter cube / compact CCD camera module], Cinema 4D (C4D) clean industrial design render, bright high-key soft studio lighting, smooth matte white, soft light gray, and muted matte accent materials ([COLORS]), clean simple geometric forms, infinite depth of field, centered and isolated on a pure solid white background (#FFFFFF), no ground shadow. Strictly no text, no cables, no arrows, no glowing effects, no neon, no bokeh, no cinematic contrast.
```

---

## 生成后的强制加工流程
1. 用 `scripts/clean_asset.py` 去除纯白/微灰背景并转为透明 PNG（对已经很淡雅的 C4D 粉彩素材，`--desaturate` 可设为 `0.05` 或 `0.0` 以保留干净粉彩色感）；
2. 将处理后的透明 PNG 嵌入 HTML/SVG 合成画布，按参考图 `04` / `05` 的方式，用**纯黑细折线、淡蓝渐变箭头、2D 扁平机理小图与朴素无衬线黑字**完成最终工程合成；
3. 在同一张图的多个子图中直接复用同一份透明 PNG，确保 100% 实例一致性。
