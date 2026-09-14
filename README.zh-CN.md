# 金融与会计研究方法顾问

[English](README.md) | 简体中文

这是一个 Codex 技能，用于设计、验证、实现和审计学术金融与会计研究中的机器学习、自然语言处理、嵌入、LLM 和因果机器学习方法。

## 适用场景

当研究问题类似以下形式时，可以使用本技能：

- 我应该使用哪种计算方法？
- 应该使用词典、嵌入、BERTopic、BERT，还是 LLM？
- 如何验证由 LLM 构建的研究变量？
- 如何将文本模型输出转换为公司—年度指标？
- 训练集与测试集之间是否存在公司层面或时间层面的信息泄漏？
- 应该使用 DoubleML 还是因果森林？
- 如何撰写计算测量方法的方法部分？
- 如何设计标注规范？

本技能的主要用途不是概述单篇论文。对于单篇论文，应先使用论文精读技能，再用本技能判断论文中的方法是否适合当前项目，以及应如何调整和验证。

---

# 推荐目录结构

```text
finance-accounting-methods-advisor/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── AGENTS.md
├── references/
│   ├── Finance_Accounting_ML_LLM_Methods_Handbook.md
│   ├── Finance_Accounting_Methods_Advisor_Prompt.md
│   ├── method-selection-matrix.md
│   ├── validation-guidelines.md
│   ├── textual-analysis-and-embeddings.md
│   ├── llm-measurement.md
│   └── causal-ml.md
├── templates/
│   ├── research-design-blueprint.md
│   ├── construct-codebook.md
│   ├── validation-protocol.md
│   ├── methods-section-template.md
│   ├── method-decision-log.md
│   └── reproducibility-checklist.md
├── scripts/
│   ├── scripts-README.md
│   ├── requirements-starter.txt
│   ├── init_research_project.py
│   ├── text_classifier.py
│   ├── embedding_similarity.py
│   ├── topic_discovery.py
│   ├── llm_classification.py
│   ├── doubleml_template.py
│   └── _io_utils.py
└── evals/
    └── evaluation-cases.md
```

---

# 安装

将整个文件夹放入 Codex 的技能目录。

例如：

```text
C:/Users/<username>/.codex/skills/finance-accounting-methods-advisor/
```

然后重启或重新加载 Codex，使其重新发现该技能。

不同 Codex 配置的技能目录可能不同；请使用现有自定义技能所在的目录。

---

# 技能的工作方式

方法顾问遵循以下顺序：

```text
研究构念
→ 分析单位
→ 任务类型
→ 基准方法
→ 首选方法
→ 验证
→ 实现
→ 计量应用
```

它不应从选择算法开始。

示例：

## 主题发现

提示词：

```text
我有 2005—2025 年的 SEC 问询函。
我想了解 SEC 会提出哪些类型的问题。
```

预期逻辑：

```text
可能以单条 SEC 问询为分析单位
→ 真正的发现型任务
→ LDA/NMF 基准
→ BERTopic/嵌入聚类
→ 稳定性检验和人工解释
→ 冻结分类体系
→ 使用监督学习进行正式分类
```

不应直接把 BERTopic 产生的聚类数量当成真实的经济主题数量。

## 已知构念

提示词：

```text
我想衡量董事长致辞是否强调创新。
```

预期逻辑：

```text
研究构念已经明确
→ 主要任务不是主题发现
→ 词典基准
→ 若语义细微差异重要，则使用经过验证的分类器或 LLM
→ 人工标注金标准样本
→ 聚合到公司—年度层面
```

## 因果机器学习

提示词：

```text
我想使用因果森林证明 AI 采用提高了公司价值。
```

预期逻辑：

```text
明确处理变量、结果变量和时间顺序
→ 质疑识别策略
→ 因果森林不能解决 AI 采用的内生性
→ 先建立可信的因果识别设计
→ 仅在有充分理由时用因果机器学习估计异质性
```

---

# 日常使用示例

可以直接向本技能提出：

```text
为……设计一个达到发表标准的方法方案。
```

```text
比较 BERTopic、LDA、嵌入和 LLM 分类对……的适用性。
```

```text
以严格的 JAR/JAE/RAST 审稿人视角审计以下计算方法……
```

```text
为……创建标注规范。
```

```text
为……创建验证方案。
```

```text
将这个已经冻结的测量流程写成论文的方法部分。
```

```text
先定义验证策略，再为首选方法编写 Python 代码。
```

---

# 渐进式加载参考资料

本技能不会默认加载所有文档，而是根据任务选择所需资料。

典型路由如下：

| 问题 | 主要文件 |
|---|---|
| 方法选择 | `method-selection-matrix.md` |
| 验证 | `validation-guidelines.md` |
| 文本、嵌入或主题 | `textual-analysis-and-embeddings.md` |
| LLM 测量 | `llm-measurement.md` |
| DML 或因果森林 | `causal-ml.md` |
| 更全面的细节 | 主手册 |

---

# 模板

## 研究设计蓝图

在启动新项目时使用。

生成一份结构化计划，涵盖：

- 研究构念
- 数据
- 分析单位
- 基准方法
- 首选方法
- 金标准标签
- 信息泄漏
- 验证
- 聚合
- 计量设计
- 稳健性
- 表格与图形
- 审稿风险

## 构念与标注规范

在人工标注或 LLM 编码之前使用。

用于定义：

- 研究构念
- 分析单位
- 纳入与排除规则
- 模糊情形处理规则
- 正例、负例和边界案例
- 多标签或有序分类规则
- 编码员流程
- 金标准样本治理

## 验证方案

在大规模推断之前使用。

用于定义：

- 金标准样本
- 数据划分
- 评价指标
- 错误分析
- 构念效度
- 方法稳健性
- 领域漂移
- 阈值
- 接受标准

## 方法决策日志

贯穿整个项目使用，用于记录重要的方法选择、备选方案、证据、风险和计划中的稳健性检验。被取代的决策仍应保留，以形成可审计的研究轨迹。

## 可复现性清单

在冻结最终实证数据集或传阅论文之前使用。清单涵盖原始数据来源、标注、建模、信息泄漏、变量构造、软件环境和仓库级可复现性。

## 方法部分模板

仅在研究设计已经冻结后使用。

对于尚未获得的结果，应保留占位符，不得虚构模型表现。

---

# 推荐的配套技能

配套的 `finance-accounting-paper-reader` 技能可以回答：

> 这篇论文具体做了什么？

本方法顾问则回答：

> 该方法是否适合我的项目？我应如何调整和验证它？

应保持两者的职责边界。

---

# 质量标准

本技能应优先追求：

> 有效、可复现、可解释的测量

而不是：

> 最新的模型。

高质量回答应帮助研究者捍卫以下逻辑链条：

```text
理论
→ 研究构念
→ 数据
→ 测量
→ 验证
→ 研究变量
→ 实证设计
→ 经济推断
```

# 初始化新的研究项目

本技能包包含 `scripts/init_research_project.py`。

完整的入门脚本命令和依赖分组请参见 `scripts/scripts-README.md` 与 `scripts/requirements-starter.txt`。

示例：

```bash
python scripts/init_research_project.py \
  --name sec_comment_novelty \
  --output-root D:/Research/Projects \
  --title "SEC Comment Novelty and Future Restatements"
```

该命令会创建：

```text
project/
├── data/
├── code/
├── prompts/
├── configs/
├── outputs/
├── models/
├── docs/
│   ├── research-design-blueprint.md
│   ├── construct-codebook.md
│   ├── validation-protocol.md
│   ├── method-decision-log.md
│   └── reproducibility-checklist.md
└── manuscript/
    └── methods-section-template.md
```

项目脚手架采用保守策略：原始数据、模型产物、`.env` 和生成的输出会被排除或分离，以便研究者自行决定哪些内容适合安全提交。
