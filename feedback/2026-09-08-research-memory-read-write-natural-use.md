# 三个课题的科研记忆读写观察

## 读写效率切片：需求与初始实现

用户认可 Research Mode 关闭时隐藏 Skill 的边界，本轮不将其视为待修bug。
给定安装入口的自旋链/Domain Walls短测分别耗时253.293/130.751秒；审批等待
122.923/16.997秒；模型请求12/13次，首响应与流式生成累计118.437/111.441秒。
指标可能重叠，不作机械分解。独立check计时约6.086/0.599秒。全库JSON约
113/98KB导致后续上下文与截断读取负担；主Skill+reference原911行约58KB。
因此本轮将主入口684行压缩为182行，保留安全规则，将低频细节移至按需文档，
增加独立读取同批及完整报告按需查看的指导。未新增CLI/schema/runtime，
安装、隔离写入与真实比较验收尚待进行；不据此宣称因果或行为优越性。

## 本轮收尾：授权导航更新与短测

用户明确确认 Topic canonical 编辑例外后，只更新 GW Topic 导航章节，原身份/
Research Goal 保留。跨三课题974个旧 Markdown 中仅该文件变更，无新增记录。
公开 check 前后逐字相同；四条线的 scoped enter 保持各自 Note 入口。专用
mode-off 会话确认改后导航不暗示当前活跃会话或跨线 Goal 归属。另一个全新
会话找回相位失配修正推导及限制，在允许必要综合写入时仍选择零写入，因为
现有 Note 已覆盖。完整ledger190项通过，插件63文件匹配。辅助入口测试，
不声称自动发现、全面召回、正向新模板写入或因果提速；未作新科学计算。

## 本轮追加：Topic 地图指导的 mode-off 入口探测

2026-09-08 14:47–14:49 UTC，新建只读 Hakimi 会话先尝试 `aitp --help`
（PATH 无命令），再查工作区 Skill，最后 `Skill(using-aitp)` 被宿主以
Research Mode 未开启拒绝。模型报告未读到记录，未冒称恢复成功。未改科研
文件、启用 Mode 或 Goal。它证明仅安装指导不足以使该 host 的 mode-off
会话自动发现它；不能当作记录恢复通过。随后只补提供插件文件和公开 Python
CLI 入口，继续原查询，单独记为辅助验收。源码定位为 Hakimi
`aitpResearchFeature.ts` 的 `SkillVisibilityContribution`：插件 Skill 的可见性
绑定 `isActive`，不属于此次 AITP-only 指导修改可修复的范围。

以下历史观察保持原文，不能代替本轮验收。

- **Topic / 日期**：2026-09-08 对 GW/LibRPA、Power-law Heisenberg、Domain Walls 既有科研记录的只读审阅；不是新的计算或受控行为实验。会话/记录细节不复制为公开测试数据。
- **handoff**：GW 的 scoped 读取可同时给出旧 closeout 的等待动作及较新的失败/重试 Entry；最近的 Working Note 也不一定覆盖随后结果。此前 Hakimi handoff 已记录“按 Glob 顺序错选另一条线 Note”的真实问题。
- **检索**：Heisenberg 的 symmetry-operator-search 有相关代数修正 Entry，但没有该 scope 的 Working Note；其他 scope 的 Note 不能替代它。较新结果不取消既有人类暂停。
- **综合**：Domain Walls 的 Working Note 已能用 basis_refs 指向阶段 closeout 和稿件依据，并明确候选构造与缺失映射的边界；现有 schema 能表达这类综合。卡片被引用多次不等于同数目的合格 trial。
- **成本 / 漏记**：本次没有测量模型自主恢复耗时或写入成本，也没有证明缺失 Note 等于遗漏 durable 事件；没有向真实账本补写。大型 mutable 证据的整文件校验与 pin drift 是另一个性能/证据生命周期问题，不在此次指导优化中宣称修复。
- **自然需求**：请求更清楚地区分归属、依据与理解修订，按问题恢复综述和未综合证据，按信息变化选 Entry/Note/零写入。无需为此增加 schema、structured prepare、lineage 或 registry；真实自主遵循和效率仍待后续验收。

## 同日追加：本地交付后的受监督 Si 会话

以上为安装前观察，原文保留。后续通过既有 Hakimi 插件 API 重装并 reload，
原 Si 会话实际读取了新指南，识别旧 Note 后的同线记录，更新 Question 并保存
一个 superseding Working Note。未新增 Entry/card/trial，也未改动旧记录、其他
研究线或 Goal。完整 ledger 测试重跑 187 项通过。

但一次成功 save 不是内容验收通过：

- 安装包内的 Skill reference Read 先被无 active action 的执行策略拒绝；开启
  action 后才恢复，反映说明读取和科研执行尚未恰当分开。
- Question 更新先错用 snapshot revision，随后改用 Question revision 成功；
  这增加了一次不必要的模型往返。
- 新 Note 的最新状态陈述来自 canonical Entries，但其 basis_refs 只固定相应
  提交凭证而未固定这些 Entries。凭证/已记录观察/独立重验应明确分层引用。
- relay 在保存后连续四次返回服务错误。验收请求的重试和未执行的补正请求
  已取消，既有 Goal 不变；引用修订仍未完成，不能声明自主遵循或效率提升。

这些是本次具体观察，不授权新 schema、索引、状态机或自动科学判断。交付边界
与后续唯一动作见 [科研记忆指南 §8](../docs/research-memory.zh-CN.md#8-本地交付与真实会话复核2026-09-08)。

## 同日追加：五个新会话的 mode-off 冷启动与修复草稿

五个新会话分别恢复 Si、NiO、Bi2Se3、Heisenberg、Domain Walls，没有开启
Research Mode 或修改原科研会话。Si 的引用后续已另行修订；NiO/Bi2Se3 的
Working Note 落后于新结果，进入用户明确授权的综合修复，尚待保存及独立复测。
Heisenberg 初读把 superseded resolver 当成当前关闭依据；canonical show
证实后继无 resolves，故 unresolved 投影没有错。监督纠正后模型承认误读。
初读每会话约23--26工具调用、约7--10分钟（包含审批等待），不支持提速结论。

NiO 草稿阶段另观察到：模型为预检临时 import yaml，缺依赖后改用正则做
文本检查，增加一次失败和往返；本不需要重造验证器。后续参考指导明确由公开
save 做正式验证，普通审阅关注内容、归属和引用，并避免把“等监督保存草稿”
写成永久科研 next action。该观察不授权新CLI或取消保存后检查。

## 同日追加：保存与独立恢复结果

上节待办随后推进：公开CLI已追加NiO、Bi2Se3综合；五个独立mode-off会话读取
同一新指导、使用同模型和原请求复测，找回两份新Note。Si首轮虽较快，却漏了
新运行配置与旧ON计划的区别，不能通过覆盖验收。因此又由Hakimi追加一份有据
Si综合，旧971份canonical文件全保留，合计只新增三份Note，未新增findings、
Entry、卡片、trial或人类决定。Si进一步独立复测已找回新旧refresh、dataset与
历史状态边界：非审批188秒、24工具、3次check；基线233秒/26工具/2次check。
这不是减少所有检查的证明，完整性优先于压低计数。最终189测试/35.58秒通过。

Heisenberg另一新会话仅收到定向问题、没有记录ID或答案，自行查明三条关系链：
两条有active resolver的failure关闭，另一条旧resolver被supersede且后继无
resolves，故仍未关闭；没有再把这个状态当投影错误，也没有自动补边。提问中
“正文缺失”与原failure的“公式/范围错误”被区分，不能将检索问题当科学事实。

首轮非审批耗时（秒，基线→复测）：Si233→181（覆盖不全）、NiO237→246、
Bi281→181、Heisenberg292→248、Walls252→229。工具数分别26→27、23→21、
26→22、23→24、25→37。审批等待从原生日志单独计算；不隐去NiO变慢和Walls
更多工具，不声称因果提速。五个首次只读复测零canonical写入。

剩余边界：普通历史索引可能陈旧；未分线记录不能自动归线；缺Note不自动等于
遗漏事件；旧严格pin漂移不通过改pin消除；卡片引用不等于合格trial。新schema、
索引、自动闭合、人类决定与发布规则均不需要改变。同行为验收明细、工具轨迹
和模型输出保留在Hakimi私有.tmp目录，不把科研原文变成公开fixtures。
# Efficiency follow-up acceptance (2026-09-09 Asia/Shanghai)

This later result does not rewrite earlier pending observations below. Lean
using-aitp main182lines and on-demand references are locally installed; all65
plugin files matched at Sep8 16:14:48UTC, all217sessions idle. Ledger191passed.
Same short mode-off read prompts used12->8 and13->9 model requests; tools17->18
and16->15. Chain first answer required a15.822s/2-request correction about the
still-paused Goal; no unassisted correctness claim. Walls wall time increased
130.751->151.227s due longer supervision approval wait; non-approval time
113.754->94.850s. No causal/general speedup claim. Full numbers and limitations
are in docs/research-memory.zh-CN.md, efficiency acceptance section.

Isolated synthetic public prepare/save/retry/working-Note/query test passed:
oneEntry/oneNote, exactTopic/workstream, already_saved retry, empty other scope,
noextra records.532.277s includes341.996s of supervisor approval waits; no write
baseline or write-speedup claim. Three real stores974canonical Markdown files
unchanged. No Skill visibility/permissions/runtime/schema/CLI/human semantics
changed. Details are private Hakimi .tmp/aitp-lean-read-write-20260909 reports.
Remaining natural-demand candidate: host read-only approval/report presentation;
not authorization for a new AITP protocol, index, registry or background service.
