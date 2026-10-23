# 展示页设计参考：5个机器人开源项目

联网检查日期：2026-10-23。只借鉴展示结构，不复制代码、视频、图片或品牌设计，不暗示这些项目支持本项目。

| 项目与实际读取入口 | 展示方式／可借鉴的做法 | 本页如何使用 |
|---|---|---|
| [openpi](https://github.com/Physical-Intelligence/openpi) · 实读README | 将模型类型、使用/微调入口、硬件需求与已知限制分开；偏工程交付而非只放高光视频 | “展示→数据→重算”资源入口与适配范围；不借其模型能力作本项目背书 |
| [OpenVLA](https://github.com/openvla/openvla) · [项目页](https://openvla.github.io/) | 任务命名的视频网格，明确零样本与微调机器人视频的差别；部分视频标2×/4× | 每段视频单独标任务、原判据、审核状态和4×，不混淆实验条件 |
| [Octo](https://github.com/octo-models/octo) · [项目页](https://octo-models.github.io/) | 顶部集中Paper/Code/Weights入口，随后用概览、模型与数据图解释系统 | 顶部论文/仓库入口，后续用分层证据解释工具回执、任务reward和物理资格 |
| [MimicGen](https://github.com/NVlabs/mimicgen) · [项目页](https://mimicgen.github.io/) | 按重置分布、物体、机器人和任务类型组织大量并列视频；对比对象/条件直接标在素材旁 | 将历史录像和受控诊断分区；真实前后观测并列，明确不是修复因果对照 |
| [ManiSkill](https://github.com/mani-skill/ManiSkill) · 实读README | 开场用环境/机器人teaser建立直观印象，再提供文档、基线与可运行示例入口；标明渲染/数据来源 | 以真实Piper录像开场，随后链接基线数值与复现说明；所有来源单独记录 |

没有比较它们的机器人性能。页面参考与HTTP获取哈希见`showcase_reference_fetches.json`；HTML中video/image标签数量只用于确认素材组织，不等同于独立实验数。本项目仅使用自己的仿真录像与已发布诊断图。

## 本页自己的证据边界

-3段历史录像来自`piper_multitask_collect_v2`，含1个原判据成功和2个未完成例；与论文G1/G2/32布局样本分开。
-视频保留完整源时间线，以4×编码；它不是执行速度测量，也不是同seed修复前后对照。
-2组C0/C1图像是保存的原始观测；身份切换的解释来自历史保存掩码检查，当前展示图不伪装成新的分割标注。
-数字来自仓库已发布JSON；分母、初态拒绝、终审状态、非显著结果和校准限制随图一起展示。
-网页无第三方字体/CDN/统计追踪，无模型API调用。静态站点由本仓库GitHub Pages发布。
