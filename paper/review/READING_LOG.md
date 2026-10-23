# 阅读日志：10篇CVPR＋10篇实证分析论文

日期：2026-10-23（北京时间）。作者授权的写作辅助与模拟预审，不是正式CVPR评审。使用peer-review与ml-paper-writing技能；没有调用付费模型API，没有运行新实验。

**阅读层级诚实说明**：20篇均实际读取主来源摘要；下表逐篇标出额外阅读的引言、方法或实验片段。部分全文PDF已获取并提取，全文获取不等于全文精读；不声称已完整精读20篇。CVF浏览工具直接open返回403，随后本地urllib实际取得主站HTML及7篇PDF片段，原始fetch记录保留。其余以主站检索返回、arXiv、出版社及作者页面交叉核实。全文/页面缓存仅保留私有工作目录，不发布第三方全文。

| ID | 论文、年份、来源 | 实际阅读层级 | 提炼的写作／审查要求 |
|---|---|---|---|
| C01 | [GraspNet-1Billion: A Large-Scale Benchmark for General Object Grasping](https://openaccess.thecvf.com/content_CVPR_2020/html/Fang_GraspNet-1Billion_A_Large-Scale_Benchmark_for_General_Object_Grasping_CVPR_2020_paper.html)，2020，CVPR | 摘要＋PDF第1/2/8页片段 | 统一抓取表示和解析评分，并用实际机器人核查指标；本项目局部抬升标签不能直接称GraspNet式抓取质量。 |
| C02 | [SAPIEN: A SimulAted Part-Based Interactive ENvironment](https://openaccess.thecvf.com/content_CVPR_2020/html/Xiang_SAPIEN_A_SimulAted_Part-Based_Interactive_ENvironment_CVPR_2020_paper.html)，2020，CVPR | 摘要＋PDF第6/7/8页片段 | 显式区分感知、运动属性和操纵指标；GT分割启发式的结果不能冒充可部署视觉策略。 |
| C03 | [GAPartNet: Cross-Category Domain-Generalizable Object Perception and Manipulation via Generalizable and Actionable Parts](https://openaccess.thecvf.com/content/CVPR2023/html/Geng_GAPartNet_Cross-Category_Domain-Generalizable_Object_Perception_and_Manipulation_via_Generalizable_and_CVPR_2023_paper.html)，2023，CVPR | 摘要 | 部件语义、位姿和操作分开评估；跨类别推广必须有未见类别划分。 |
| C04 | [Generalizing 6-DoF Grasp Detection via Domain Prior Knowledge](https://openaccess.thecvf.com/content/CVPR2024/html/Ma_Generalizing_6-DoF_Grasp_Detection_via_Domain_Prior_Knowledge_CVPR_2024_paper.html)，2024，CVPR | 摘要 | 物理先验和接触图优化已有先例；不能把CAD/接触修复称首次物理知识操作。 |
| C05 | [Do Better ImageNet Models Transfer Better?](https://openaccess.thecvf.com/content_CVPR_2019/html/Kornblith_Do_Better_ImageNet_Models_Transfer_Better_CVPR_2019_paper.html)，2019，CVPR | 摘要及引言（原站PDF检索返回） | 转移相关性随冻结/微调和训练正则而变；必须交代训练与评测条件，不能只比较总准确率。 |
| C06 | [PointNet: Deep Learning on Point Sets for 3D Classification and Segmentation](https://openaccess.thecvf.com/content_cvpr_2017/html/Qi_PointNet_Deep_Learning_CVPR_2017_paper.html)，2017，CVPR | 摘要 | 点集合的几何表示并不自动解决语义实例对应；点云处理层与动作成效层应分开。 |
| C07 | [PointASNL: Robust Point Clouds Processing Using Nonlocal Neural Networks With Adaptive Sampling](https://openaccess.thecvf.com/content_CVPR_2020/html/Yan_PointASNL_Robust_Point_Clouds_Processing_Using_Nonlocal_Neural_Networks_With_CVPR_2020_paper.html)，2020，CVPR | 摘要＋PDF第2/8页片段 | 噪声/离群点影响早期采样及后续任务；模块贡献需消融，简单过滤是必要强基线。 |
| C08 | [A Closer Look at Spatiotemporal Convolutions for Action Recognition](https://openaccess.thecvf.com/content_cvpr_2018/html/Tran_A_Closer_Look_CVPR_2018_paper.html)，2018，CVPR | 摘要＋PDF第2/5/8页片段 | 用匹配结构及训练设置隔离时空建模贡献；对我们意味着观察、时间和调用预算不能混杂。 |
| C09 | [Making Better Mistakes: Leveraging Class Hierarchies With Deep Networks](https://openaccess.thecvf.com/content_CVPR_2020/html/Bertinetto_Making_Better_Mistakes_Leveraging_Class_Hierarchies_With_Deep_Networks_CVPR_2020_paper.html)，2020，CVPR | 摘要＋PDF第2/5/8页片段 | 错误类型和严重性不是一个top-1数；报告误报、漏报及接触风险，不能只报总成功。 |
| C10 | [ImageNet-E: Benchmarking Neural Network Robustness via Attribute Editing](https://openaccess.thecvf.com/content/CVPR2023/html/Li_ImageNet-E_Benchmarking_Neural_Network_Robustness_via_Attribute_Editing_CVPR_2023_paper.html)，2023，CVPR | 摘要 | 通过控制属性变化做模型调试；本项目可报告具体估计/观察干预，但未做因果隔离不能称原因。 |
| E01 | [Deep Reinforcement Learning That Matters](https://ojs.aaai.org/index.php/AAAI/article/view/11694)，2018 | 摘要＋PDF第1/2页片段 | 实现、随机性和报告程序影响RL结论；单训练seed是限制，不把450评测episode当450训练重复。 |
| E02 | [Implementation Matters in Deep Policy Gradients: A Case Study on PPO and TRPO](https://arxiv.org/abs/2005.12729)，2020 | arXiv摘要（ICLR2020版） | 代码级细节可改变算法排名；本项目接口不一致只是风险证据，需受控executor对照才能归因。 |
| E03 | [A Closer Look at Deep Policy Gradients](https://arxiv.org/abs/1811.02553)，2020 | arXiv摘要（ICLR2020版） | 研究理论代理量与实际行为的错位；为command/reward/physical outcome分层提供写作先例，不替代本项目证据。 |
| E04 | [Deep Reinforcement Learning at the Edge of the Statistical Precipice](https://arxiv.org/abs/2108.13264)，2021 | arXiv摘要＋作者项目页 | 少run的聚合点估计不可靠；应报告区间、配对差异和任务分层。 |
| E05 | [Do ImageNet Classifiers Generalize to ImageNet?](https://proceedings.mlr.press/v97/recht19a.html)，2019 | 摘要＋PDF第1/2/8页片段 | 复建数据分布仍会引入变化；分开发、校准和未消费测试，避免把校准优势写成泛化。 |
| E06 | [Underspecification Presents Challenges for Credibility in Modern Machine Learning](https://jmlr.org/papers/v23/20-1335.html)，2022 | 摘要＋PDF第7页主站检索片段 | 同测试表现可掩盖部署行为不同；用匹配输入的contrastive evaluation定位局部差异。 |
| E07 | [Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations](https://proceedings.mlr.press/v97/locatello19a.html)，2019 | 摘要及原站方法规模说明 | 代理指标变好不等于下游收益；我们原判据、局部合格、学习增益必须分别报告。 |
| E08 | [Are GANs Created Equal? A Large-Scale Study](https://proceedings.neurips.cc/paper/2018/hash/e46de7e1bcaaced9a54f1e9d0d2f800d-Abstract.html)，2018 | 摘要及PDF引言主站检索片段 | 匹配调参与计算预算可能消除方法优势；不能只对弱默认基线报收益。 |
| E09 | [A Metric Learning Reality Check](https://arxiv.org/abs/2003.08505)，2020 | arXiv摘要 | 旧方法在公平协议下可能仍强；本项目强SOR/CC不能藏在附录。 |
| E10 | [A Step Toward Quantifying Independently Reproducible Machine Learning Research](https://proceedings.neurips.cc/paper_files/paper/2019/hash/c429429bf1f2af051f2021dc92a8ebea-Abstract.html)，2019 | 摘要及PDF引言主站检索片段 | 发布代码不等于独立复现；明确数值重算、原状态forward复核、重新积分执行是不同层级。 |

## 结论

20篇提供的是研究设计与证据表达参照，不是对本稿可发表性的背书。最接近本稿的是Implementation Matters、Statistical Precipice和Metric Learning Reality Check：都要求可定位、可重复且公平的对照；本稿目前仍是单stack证据审计技术报告。不要将本阅读清单20篇全部硬塞进正文，正文引用应只支持对应句子。

## 文献获取记录

`paper_sources.json`列出20个主链接；`fetch_receipts.json`保留实际HTTP取回与哈希，技术失败亦保留。`verified_references.bib`是从CVF HTML实际提取；`draft_verified_references.bib`是初稿8篇的arXiv原站BibTeX导出。摘要层级的作者结论未被当作本项目因果证据。
