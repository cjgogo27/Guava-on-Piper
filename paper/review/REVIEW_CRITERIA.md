# 作者授权的CVPR标准模拟预审：证据门槛

不是CVPR实际分配审稿、不是评审决定、不是外部同行认可。官方CVPR2026政策禁止正式审稿人用LLM生成评审，本文件用于作者自己的草稿改进。核查来源：https://cvpr.thecvf.com/Conferences/2026/ReviewerGuidelines 。目标CVPR2027政策仍需投稿前重查。

## 文章定位

建议：单一Piper仿真迁移的可审计技术报告；三层success语义是组织框架，不宣称新理论。题目可以保留When Tool Calls Succeed but Manipulation Does Not，副标题需明确single-stack evidence audit。既不自动科研案例，也不新算法论文。

## 证据门槛

| 事项 | 本稿要求 | 当前能到哪里 |
|---|---|---|
| 因果 | 相同checkpoint/prompt/scenes、仅变executor；基线未变，随机化或严格配对 | 未完成，接口错配不能解释SFT托盘退化 |
| 独立单位 | layout/episode；共享setup/多arm/多时间步不得作独立N | G1 N48含7拒绝；G2 N16含5拒绝；held N32，4重复不扩N |
| 统计 | 报配对discordants、效应和区间、预声明family与Holm；小p不等于实用价值 | G1 p校正不显著；G2校准p.5；held TP损失支持具体否定 |
| 负结果 | 固定候选、真实执行、非基础设施错误、强基线及完整失败记录 | 可发表为局部证据，不能推所有主动感知/融合无效 |
| 成功语义 | command/arrival、task reward、physical qualification分表 | 不合并不同研究为一个SR |
| 可部署性 | RGBD/CAD/FK为online；GT仅offline；质心/身份估计不冒充GT | 目前纯仿真，不能声称真机安全/迁移 |
| 数据质量 | 旧approved/unreviewed/needs_review/rejected标签保留 | 1041训练集不称全合格训练数据 |
| 强基线 | SOR/CC、分位、固定方向、实际观察成本；同数据/预算 | G2强基线应进入主文而非只附录 |
| 完整评分 | common setup/观察/抓/抬/保持一起；reject/abort完整分母 | 2.917mm共同setup扣除必须保留；不能拿旧after-parent更高数 |
| 复现 | release明确能数值重算还是能完整物理复跑；依赖/哈希/许可证 | 当前public rows只能数值重算，不能声称外部完整物理复现 |
| 新颖性 | 窄且有证据的insight；别靠“首次”或论文数量装创新 | 没有已证明的新方法优势，先技术报告 |

## 建议结构

1. 特定迁移问题与三个success层级；2. provenance与契约审计方法；3.历史schema/固定模型评测（descriptive）；4.两个独立局部诊断（强基线和视觉proxy负结果）；5.可复现release；6.限制与未来受控executor研究。不要把未完成实验写进results，不用训练loss解释操作能力。

## 人类最终责任

仓库owner应核实作者、第三方许可、引用以及未来venue披露政策；本模拟审查不是自动录用证据。所有科学数值以随稿数据及脚本重算为准。
