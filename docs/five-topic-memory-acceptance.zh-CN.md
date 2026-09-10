# 五课题科研记忆整理与冷恢复验收

2026-09-09；**有限范围验收完成：五课题 30/30 冻结题通过，Si 整理后独立复测 7/7 通过。**

目标不是把所有 warning 消掉，而是让新会话能说清：当时结论是什么、
适用条件和依据是什么、后来为什么改变、哪些证据仍可取回。
这是有限题集的恢复测试，不是实际等待数月后的保管实验、全历史召回保证，
更不是重新证明五个课题。

## 范围与当前入口

| 课题 / 显式 workstream | 当前 working Note | 当前验收状态 |
| --- | --- | --- |
| GW Si / qsgw-headwing | note-9f78030be667423aad87782960aa67f4 | 原六题通过；整理后六题复测及新增旧源码恢复题通过 |
| GW NiO / crpa | note-211fea5f99094da5b4851e5f1543f5e2 | 六题基线通过，已有综合覆盖本次核对，不重复造 Note |
| GW Bi2Se3 / magnetic-symmetry | note-84fd10c37e894204a6f211393c248490 | 六题基线通过，保留同线不同材料的边界 |
| 幂律 Heisenberg / symmetry-operator-search | note-95855242c7c04183a225aead405bf8be | 六题通过，精确 L=6 障碍与 L=7/8 未认证结果明确区分 |
| SYM 畴壁 / sun-generalization-theory-first | note-1f6033d26449485d83c209963430c239 | 整理后六题通过，并恢复历史文章归档内的精确旧稿 |

GW 三线共用 Topic，但不共享科学结论；qsgw-semiconductor 不是
qsgw-headwing 的隐式别名。某条记录有多个明确 workstreams，不代表其他
记录会因共用文稿或源码而获得这些归属。

## 做了哪些实际整理

- **Si：**公开 save 新增 observation `entry-3df8b35a837a4644bc66c23cc52c8353`，
  记录从固定 nested Git commit 取回旧 exporter 并匹配原 pin。
  新 working Note 替代旧 agent Note a2b8a5ff，保留 nfreq6 旧失败、nfreq16
  首轮请求、refresh=false 与旧三轮 ON 的区别，以及未验收的物理链条。
  nested Git 位置是明确检索入口，不伪称为 AITP 根仓库已验证的 git pin。
- **畴壁：**公开 save 新增 observation `entry-eec825612a084c1b92697a160188ddec`，
  为缺少必填章节的旧 SU4 记录提供有效、可查询的恢复说明。原推导文件
  匹配原 pin；这不等于重新证明其全篇论证。新 working Note 替代旧 agent
  Note 84858cf，连接条件范畴结果、物理 probe/neutral attachment 和不同的
  SU5 sewing 缺口。旧 malformed 记录没有被编辑或自动 supersede/resolve。
- **NiO、Bi2Se3、自旋链：**核读已有 scoped 综合及相关旧记录。没有为了
  “每课题都写一次”重复已有科学事件、编造新结果或批量制造 Method cards。

全部真实写入只编辑 CLI 返回的 draft，再经公开 record/note save。
Entry 使用 paired expected-topic/exact-workstream；Note 没有该原子变体。
每次 save 后执行 check/enter，验证当前入口及未决关系。
后续日常记录仍使用已有 Entry/Note：在实质结论、反证、判断变化时保存事件，
当当前综合落后于这些事件时新建 superseding working Note；没有 durable delta
就不制造记录。执行时机属于 Skill/agent 判断，AITP 运行时不强制科研步骤，
这次新会话验收也不是 exactly-once 自动维护证明。
相对本轮早期捕获的 975 个原有 canonical Markdown，原字节全部不变，
只新增上述两条 Entry 和两份 Note；该保留性基线是在首个只读测试开始后捕获，
不是声称在全部任务之前完成了备份。

## 怎样测试，而不是只检查保存成功

整理前冻结每课题六题，共 30 题：当前结论及条件、历史结果及依据、认识
变化原因、失败/未决问题、推导或产物位置、跨线或错误前提负例。
参考答案保留在监督方，不注入被测会话。新会话只获得工作区、已确认 scope、
公开 AITP Skill 路径和问题；Research Mode 关闭，无旧聊天，不启动原 Goal、
子 agent、远端作业或科学计算。实际模型为 `openai-codex/gpt-6-astra`。

| 已完成基线 | 总耗时 | 审批等待并集 | 模型请求 / 工具调用 |
| --- | --- | --- | --- |
| Si | 389.366 秒 | 180.759 秒 | 17 / 38 |
| NiO | 274.503 秒 | 97.182 秒 | 12 / 28 |
| Bi2Se3 | 345.183 秒 | 141.434 秒 | 15 / 40 |
| 自旋链 | 834.258 秒 | 307.857 秒 | 12 / 32 |
| 畴壁 | 928.104 秒 | 439.631 秒 | 13 / 33 |

结果为 **30 道冻结题通过，Si 整理后 7/7 复测通过**（六题重复，不算 37 道独立题）。上述剩余时间混合模型、网络、
工具与调度，不能称为纯推理耗时；不同审批等待也不支持因果速度比较。
模型曾先使用不兼容的 Python 3.10，随后找到 3.12 并恢复；Skill 已有优先选择
兼容解释器的指引，但实际执行并不保证遵循。部分宽检索和重复读取也仍存在。
本次不把答案正确宣称为全流程最高效，更不据此改动 Hakimi 权限或绕过审批。
自旋链/畴壁此前的 522 失败没有完整答案，不计为召回通过或召回错误。
畴壁后续是整理后的首次验收，不能伪称有修复前后的行为提升对照。
Si 专项复测用时 1548.728 秒，审批等待 383.249 秒，18 次模型请求、36 次工具调用。
它独立读回固定 Git 对象并匹配原 pin，原六题没有回退，但耗时比基线更长；
新增题目、模型/网络和审批时序不同，不能归因为 AITP 本身变慢或宣称提速。
所有完成的测试均以 idle/completed 结束，Research Mode inactive、Goal/action/
pendingCheckpoint 为空、无排队 prompt。

### 逐课题恢复到了什么

每行对应该课题六道冻结问题；详细题目、原始答案及逐题判定存于下述私有证据包。

| 课题 | 已找回的主要历史链条 | 正确保留的限制 / 负例 |
| --- | --- | --- |
| Si | 旧 nfreq6 的 HR 失败 → 新 nfreq16 首轮能带请求；输入、回执、HR 相位界推导和分析入口 | iter0/构建成功不等于 iteration1 物理验收；refresh=false 不等于三轮 head-wing 自洽；不能借另一线验收 |
| NiO | 早期无 U 输出 → 后来的诊断张量；旧六频率点 Dyson 失败与后续检查器改动 | 检查器通过不修复 nonpassive 响应；正频率节点不是 U(0)，不能用 Bi2Se3 验收代替 |
| Bi2Se3 | 旧 SOC WFC 不完整、后续终态和标准路径比较；reader、图表与推导入口 | 部分 WFC 与后续 OOM 不混淆；142/220 bands、占据/Fermi 缺口仍在；不导入 Mn3Sn 或旧非 SOC 结果 |
| 自旋链 | 受限数值搜索 → 人类选择证明路线；L=6 精确障碍、归一化、端点/延拓/all-level 草稿 | L=7/8 认证仍失败；leakage 的处理不继承到其他 failure；证明方向不代表 Goal 已恢复或全模型不可积 |
| 畴壁 | 条件性的中心/中性分解 → 真实 probe、neutral attachment 和 junction 需求；SU4/SU5 分别恢复 | 范畴相容性不等于微观唯一性或物理 F_web；原格式缺陷及 SU5 旧版本缺口未被掩盖 |

畴壁新会话另外从 `2026-09-06-before-offline-handoff.tar.gz` 向 stdout
读取旧文章 TeX，匹配 `entry-7e70fd2418a64aa5b941d24723fa811f` 的原 pin。
监督方独立复核了归档和成员摘要。这是按需旧版本取回，不是重新编译或物理验收。

## 最小 AITP 优化与交付

在 `using-aitp/references/research-memory.md` 中按需补充历史版本恢复边界，
同步已有 enter 描述和双方 handoff。区分记录发现、原版本取回和科学验证，
不增加每轮检查、schema、CLI 命令、索引或备份平台。Skill 负责提醒和判断；
AITP CLI 负责确定性读写/验证；Hakimi 本轮只承担测试会话和安装，不改编排或权限。

新增合成回归验证：原工作文件变化后，通过旧快照找回原字节，新记录可保存、
重试可复用，但旧 pin finding、原 failure 和跨线隔离保持不变。
全量 ledger **192 passed / 41.93 秒**，Skill 验证和相关 diff 检查通过。
这是协议回归，不替代真实新会话的答案核对。

安装前确认 224 个会话空闲、仅两份预期 bundle 文件不同。单次安装请求
先超时；未重试该 mutation，随后 2026-09-08 17:57 UTC 核验 65 文件一致，
插件 API enabled/ok。安装完成与后续冷恢复通过是两项不同证据。

## 剩余证据边界

全局 check 均正常产生报告（exit 1），整理后 findings 数未变化：

| 工作区 | errors | warnings |
| --- | --- | --- |
| GW | 73 | 201 |
| 自旋链 | 24 | 263 |
| 畴壁 | 34 | 221 |

这些是 findings 数，不是独立科学失败数。Si 恢复旧 exporter 不会让当前
working-path 的旧 pin 自动匹配；畴壁有效恢复说明不删除原格式错误。
SU5 两份历史文稿的严格 pin 仍未恢复，部分其他旧可变引用漂移或缺失；
不以同名新文件、重写 pin 或降低策略冒充修复。需要依赖其精确旧论证时，
必须保留这个版本缺口。哈希并不保存文件，长期保管仍需普通证据/仓库备份。
M2 reviewed artifacts、M3 cross-topic links/catalog、M4 collaborator protocol
仍为各自证据驱动的 planned / unavailable；本次没有提前实现它们。也没有
新增自动备份、全历史语义召回服务或跨课题自动合并。

冻结问题、五份原始答案、逐题评分、耗时和测试会话索引已保存到持久私有目录
`/home/bhjia/.local/state/aitp-memory-acceptance/20260909-five-topic/`。
临时工作副本和完整 check 报告仍在 `/tmp/aitp-five-topic-recall-Y3UkEdyn/`；
native wire 在对应 Hakimi session 中。验收包是本次测试材料，不是科研档案备份服务。
Si 复测的 prompt、原始答案、指标与七题评分也已纳入持久验收目录；本文件不替代原始证据。

## 本次变更与验收边界

AITP 本次增量是 memory reference 的旧版本恢复指引、现有 contract 描述、
一项 synthetic history-recovery 回归，以及 README/本报告/双方 handoff。
`test_research_memory.py` 与 references 目录原本即为未跟踪用户工作，未将其全文件
冒称为本次新实现。Hakimi 只改两份 integration handoff 文档并安装本地 bundle，
未改 Research Loop、权限或客户端实现。四份科学新增记录见上文。

验收命令包括公开 CLI prepare/save → check/enter、scoped list/show、
`.venv/bin/python -B -m pytest -q tests/ledger`（192 passed）、Skill validator，
以及双方相关 `git diff --check`。fixture 覆盖 Entry/Note 写入、重试、历史替代、
human authority、失败关系及跨 scope 负例；真实测试没有写虚构科学数据。
现有 schema/fixtures/adapter contract 回归通过，不等于重新验收 Hakimi 全部客户端。

下一步唯一最小 action：在下一次真实科研产生实质新结论或反证时，沿用对应显式
workstream 写入一条有依据的 Entry，并检查当前综合是否需要更新；无需先增加 Hakimi 编排。

仓库核验：AITP HEAD `eae1bce5eba367a5f6db6ba73ff0912dd3a5e290`，
Hakimi 测试 checkout HEAD `cdf5f1638430751d19f8e3bcde71d508a74e8739`。
两者原有 dirty changes 保留，未 commit/push。AITP 0.9.0 / adapter-contract-0.2，
Hakimi CLI 0.21.0；现有 REST/WS/SDK/klient/TUI/Web 协议没有在本次改动或重新全量验收。
2026-09-08 18:34 UTC 再次只读核验 65 个 bundle 文件一致、CLI help 可用。
18:41 UTC 最终核验仍为 65 文件一致、227 个会话均空闲；双方 diff 检查通过，
975 个原 canonical 文件仍无变化，新增四份记录与预期完全一致。
