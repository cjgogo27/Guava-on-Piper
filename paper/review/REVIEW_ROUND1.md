# 模拟预审 Round 1

材料：2026-10-23版paper/DRAFT.md全文。身份：作者授权的CVPR标准写作检查，不是正式会议评审。无付费API、无新实验。

## 总体判断

作为公开技术报告初稿，结构和证据边界基本合适；不宜称已达到CVPR主会证据标准。优点是主动保留拒绝/abort、任务异质性、强基线、负结果和未完成因果对照。没有发现必须增加新实验才能诚实发布技术报告的问题。

## 发布前应修

1. **§4.3 detector定义**：B0/B1/B2/H应写准确布尔公式，避免“additionally”使读者误以为B2依赖B1。对照executed entry.py确认。表格计数相符不等于定义相同。明确缺失估计是negative还是abstention，报告coverage32/32。
2. **Abstract与§4.2解释**：“robust point-cloud processing is a strong alternative”易被读成确认优越；改为“simple filtering matched the observed candidate union on calibration”。G1差异未过Holm，G2是选择过强基线的校准，均不能声称population优势。
3. **全文排版**：大量英文数字粘连（in420、of1,041、checkpoint15-task、at least25mm等）应修为空格和单位格式，否则可读性很差。
4. **§3.2 label窗口**：明确held-detection的25mm是整个0.3s保持窗每个采样时刻都满足还是均值/末帧；Q的<=2mm按全sequence最大值，不是均值。32布局held标签不约束接触，已区分但建议精确公式。
5. **§4.1/§6计数与公开边界**：将15468calls、438/603 schema rows的计数单位明确为trajectory-tool-schema declaration，而非工具调用行。公开data列若是聚合历史审计而非原1041条，写明source-summary evidence，不让读者误以为public release能复核每一次2476调用。
6. **References**：BibTeX未到位前不要声称“verified in references.bib”。实际取得原站BibTeX后用真实文件；Guava是2026preprint，别按官方16任务模型说明当公开code 7任务白名单等同训练分布。

## 可通过收窄解决的主要限制

- 核心洞见当前是A/R/Q不可互换的工程case study，不是三个层级之间总体错误率的系统估计。现有证据没有在同一大cohort同时标A/R/Q。可在limitations明确这一点，不必为了发布报告临时拼新实验。
- 450评测是同一checkpoint的一轮fixed-run，不是重复训练分布；不要给总17success差值独立训练显著性解释。
- G1/G2与held-detection的对象/单位/标签/代码版本不同，不应汇总为96个新benchmark样本或平均SR。
- 审稿参考文献规模不是贡献；20篇reading log保留阅读层级，不能写“全文精读20篇”。
- 第三方源码/CAD未许可公开时，公开artifact贡献是原创checks+numerical reconstruction，不是开箱即用Guava/Piper全栈；稿件已基本承认，应与README保持一致。

## 证据充分的窄结论

- 当前训练schema里确有扩展参数使用，不能由此归因性能。
- 该固定运行整体49→66，但trained32→33、tray14→2，说明描述性异质性。
- G1完整评分窗口改变1个共享setup布局所有arm结果；这种审计能改变计数，无需宣称改变物理策略。
- G2校准固定SOR/CC达到已测8arm并集，不证明泛化，也不证明观察永远不需要。
- 32布局当前视觉AND没有减少FP、损失11TP；只否定这个具体规则。

## 可选改进（不阻塞技术报告发布）

增加一张A/R/Q流程图和一张按study的证据分母表；用effect-size与pair discordance替代仅p值。若以后投主会，优先做受控executor对照而非补更多故障照片。
