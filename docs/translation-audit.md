# human-writing 历史著作译文润色兼容性审查

审查日期：2026-10-18。底本为 AM5R56/human-writing `main`，提交 `4fda173f3fef7fb808f3eba991eeb2528ea4b189`，VERSION 为 1.1.0。GitHub 读取确认 Fork 上游为 KKKKhazix/human-writing；审查时双方 main 指向同一提交。以下证据固定于该提交。

## 结论及证据边界

原版适合它声明的中文创作目标，不宜未经分流直接用于历史研究著作的保真翻译润色。最直接的冲突是要求命中风格禁令的原话转述或省略；另有删减论证、背景、排比、限定和结尾的风险。原有优先序确实把当前用户要求放在前面，也承认文体例外；但没有翻译路线，硬禁项仍覆盖引语，不能仅靠“要求忠实”消除执行歧义。

检查脚本是只读检测器，不会自行删除译文。风险来自规则要求改稿者一直改到失败项清零，以及把警告里的删减建议机械用于译文。本审查证明不兼容规则和可复现的检测表现，不能据此断言任何既有译本已经被修改；未检查用户其他译文文件。

下面所有中英文验证句都是自拟材料，模拟制度研究、历史证词和犯罪术语语境，不是原书摘录。

## 固定版本的证据

- [S：SKILL.md](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/SKILL.md)：重点见“第一关先看作品靠什么站住”“多条规则同时出现时”“第一稿直接带着人写”“成稿绝对不能出现”。
- [R：revision.md](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/references/revision.md)：重点见第二至第五遍、第七遍及“使用检查脚本”。
- [F：forum-prose.md](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/references/forum-prose.md)：重点见“知识等问题走到那里再出现”“让句子有松有紧”“判断要带着来路”。
- [现实题材规则](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/references/reality.md)：重点见“正文只保留读者需要知道的归属”“判断要有边界”“来源怎样交付”。
- [虚构规则](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/references/fiction.md)、[形式规则](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/references/formats.md)、[蒸馏版](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/dist/human-writing-lite.md)：补查题材分流和替代入口。
- [原检查器](https://github.com/AM5R56/human-writing/blob/4fda173f3fef7fb808f3eba991eeb2528ea4b189/human-writing/scripts/check_prose.py)：检查常量、`mask_non_prose` 和 `main` 的失败/警告处理。

## 逐项规则与替代方案

| 原有规则 | 可能破坏什么 | translation 模式替代规则 | 证据位置及验证编号 |
| --- | --- | --- | --- |
| 原话命中禁令必须转述或省略，引号不能保留 | 引语范围、证词形式、人物声音和具体信息 | 原话完整保留；引语有误时单列原文与建议，不直接改成已核准正文 | S 硬禁项末条；R 第五遍末段；R02 |
| 否定对照及“原以为／后来发现”等固定句式不能出现 | 否定对象、制度分类、认识变化；不等于先立假误解 | 保留原文 not…but、否定范围和认识过程 | S 翻案腔；R 第五遍；R01、R05、R08 |
| 三项以上排比留两项，第三项换说法或删除 | 第三件事实、受害对象、修辞力度与动员方式 | 保留项数、顺序和可辨识的重复节奏 | S 排比；R 第五遍；R03 |
| 破折号清零，冒号仅能引人物直接原话 | 定义、解释、插入限定、对白中断和书名副题 | 标点按原文功能与项目规范处理，不以风格清零为目标 | S 标点；R 第五遍；R01、R02、R11 |
| 抽象概念借喻、拟人及部分抒情词删除或还原本义 | 作者评价、时代修辞和意象；词表不识别作者意图 | 原文有修辞就译出，解释放独立译注 | S 抽象名词及借喻；R 第三、五遍；R04 |
| 名词化改成人物动作 | 官职买卖、管辖权行使等研究对象与概念层级 | 保留专业概念，只作原文支持的搭配改善 | S 名词化；R 第五遍；R10 |
| 硬停词、路标与黑话强制删除 | “从某种意义上说”等可能是作者限定；专业术语不等于模型腔 | 不应用创作黑名单，逐词对照原文和核准术语 | R 第五遍；R15、R16 |
| 重复解释、没有新增内容的段落合并删除，试删三分之一 | 累积论证、强调、史学讨论及必要背景 | 不基于密度删段、并段或重排；节译另作明确任务 | R 第二遍；F 知识和细节；R11、R12 |
| 动作后情绪解释删去，给读者留白 | 原作者明示的恐惧对象、动机或心理判断 | 原文写了解释就译出，不替作者重新设计留白 | R 第四遍；R14 |
| 主干提前、长定语拆开、删重复主语 | 施事者、否定、条件和限定范围；多个人物可能混淆 | 可调整语序，逐项保留谁做什么、对象与条件 | R 第四遍；R05、R06 |
| 连词删一半，按句长差异调整节奏 | 必要条件、让步和因果；统计形状不证明译文质量 | 不按频率配额删词，不按句长配额重写 | F 让句子有松有紧；R06 |
| 难懂、需解释的成语典故删掉 | 历史人物身份、时代语域和典故本身 | 保留时代语言，解释另列译注 | R 第四遍；R04、R16 |
| 试删最后两段；结尾重新概括全文也先删 | 作者结论、限制条件和跨章照应 | 结尾全译；不得以“更有力”为由裁剪 | R 第七遍；R13 |
| 至少五件材料，缺材料就研究、追问或缩到短答 | 原文被当作素材重写，新增背景或缩译 | 不执行创作材料门槛；缺页标疑，不补写底本 | S 第一关；R12 |
| 开头留检索痕迹，疑点与来源归属少说，边界说明一次 | 新增译者经历冒充作者经历；删除证据限定和归属 | 区分作者、译者、史料人物，保留每处归属及限定 | 现实题材规则；R07、R18 |
| 重新核验现实事实、含禁式的来源题名改短说明 | 用现代知识覆盖原作者认识或错误；书目不再准确 | 原书陈述、标题和注释照译；纠错列译注或校勘意见 | 现实题材规则的材料、来源交付；R17 |
| 历史走现实创作、小说对白走可补场景的虚构路线 | 题材分流掩盖“翻译任务”，新增场景、对白或动机 | 翻译先分流，历史小说也不进入虚构创作流程 | S 按任务读取；fiction / formats；R02、R18 |
| 缺少原文对齐、跨章术语锁、首次括注和原注保护机制 | sawdust man 等可能按字面译或跨章改名；书籍结构无校验 | 项目术语清单、原段号与不可变基线；先括注及原注按项目要求 | 三份目标文件未实现这些机制；R09、R17 |

正常重复在原规则中并未被一概禁止，术语漂移也不是原检查器强制产生的结果。相关风险来自缺少项目约束与原文核对机制，不应把“可能遗漏”说成已发生误改。

## 原检查脚本的行为

`PIVOT_PATTERNS`、冒号/破折号、`HARD_STOPS`、`HARD_JARGON` 与部分 `ROAD_SIGN_PATTERNS` 命中会失败。其他变形翻案、排比、名词化、词语、句长、连词、段落和借喻统计主要是警告，不能混称为全部硬失败或自动删改。

`mask_non_prose` 屏蔽代码、URL、部分元数据和 HTML 标签，却不识别普通引语、史料对白与项目术语。引出引号的冒号只会降为提醒，但引号内的禁式或破折号仍可能失败。简单屏蔽所有引号也解决不了作者自己论述被风格规则删改的问题。

原版没有英文原文、逐段对齐或中文基线输入，无法检查信息遗漏、引语转述、译名一致性和原注完整性。补丁保留创作检查主体，只在 CLI 早期分流到独立的保真检查器。

## 中英文验证

各行危险改写均是故意构造的反例，不是建议采用的译文。“原脚本退出码”由固定版本原脚本对忠实中文实际运行得出；0 可能仍有警告，并不证明翻译准确，1 只表示命中创作硬禁令。

| 编号 | 英文原文（自拟） | 忠实中文 | 危险改写 | 风险 | 原脚本退出码 |
| --- | --- | --- | --- | --- | --- |
| R01 | This was not a tax but a gift: a distinction the council insisted upon. | 这不是税，而是赠礼：市议会坚持这一区别。 | 这是一份赠礼。 | 删去税与赠礼的制度边界及证据主体 | 1 |
| R02 | The witness said, “I paid, I waited, I appealed—and no one answered.”[7] | 证人说：“我付了钱，我等着，我申诉了——没有人回答。”[7] | 证人说他申诉无门。[7] | 丢失付款、等待、叙述人声及修辞 | 1 |
| R03 | They seized our grain, they seized our cattle, they seized our children. | 他们夺走我们的粮食，他们夺走我们的牲畜，他们夺走我们的孩子。 | 他们夺走我们的粮食和牲畜。 | 按两项上限删掉孩子会删去暴力事实 | 0 |
| R04 | Fear kept the town silent; the old order was crumbling. | 恐惧使城镇沉默；旧秩序正在坍塌。 | 城镇无人说话，秩序发生变化。 | 削弱因果与作者评价强度 | 0 |
| R05 | Not all officials accepted gifts. | 并非所有官员都接受赠礼。 | 所有官员都不接受赠礼。 | not all 与 all not 的范围不同 | 0 |
| R06 | Although he paid, he obtained no office; only if the council agreed could he appeal. | 虽然他付了钱，却没有获得官职；只有市议会同意，他才能申诉。 | 他付了钱，没有获得官职，可以申诉。 | 删连词丢失必要条件 | 0 |
| R07 | It may have been tolerated, according to one witness, although the register is silent. | 据一位证人说，这也许曾获容忍，尽管登记簿没有记载。 | 这种做法受到容忍。 | 推测被升级为定论且删除来源限制 | 0 |
| R08 | I believed the levy lawful; later I discovered that the charter forbade it. | 我原以为这项征收合法，后来才发现特许状禁止它。 | 特许状禁止这项征收。 | 自述的认识过程与时间性丢失 | 0 |
| R09 | The sawdust man employed a panel game, while the panel thief watched the bag. | 假钞骗子使用暗板局，暗板贼盯着皮包。 | 锯末工玩面板游戏，骗子盯着皮包。 | 词面翻译和泛称破坏项目译名 | 0 |
| R10 | The sale of offices and the exercise of jurisdiction were distinct rights. | 官职买卖与司法管辖权的行使是不同的权利。 | 有人卖官，有人审案。 | 概念分类被改成几个人的具体动作 | 0 |
| R11 | The gift was lawful. I repeat: the gift was lawful, though the demand was not. | 赠礼是合法的。我再说一遍：赠礼是合法的，尽管索取赠礼并不合法。 | 赠礼是合法的。 | 删重复连带删除主动赠予与索取的区别 | 1 |
| R12 | The office was hereditary. Under the old charter, daughters too could inherit it. | 这个官职可以世袭。根据旧特许状，女儿也可以继承。 | 这个官职可以世袭。 | 背景信息涉及继承制度，不是可任意压缩的常识 | 0 |
| R13 | Thus the practice survived: law and custom protected it. | 因此，这种做法延续了下来：法律和习惯保护着它。 | 这种做法延续了下来。 | 结尾总结中的因果解释被删 | 1 |
| R14 | He shut the door. He was afraid, not of the soldiers, but of his neighbours. | 他关上门。他害怕的不是士兵，而是他的邻居。 | 他关上门。 | 动作后解释含恐惧对象，不能因留白删除 | 1 |
| R15 | In a certain sense, the gift was compulsory. | 从某种意义上说，这份赠礼是强制性的。 | 这份赠礼是强制性的。 | 清路标会消除论断限定 | 0 |
| R16 | The methodology of this study distinguishes statements from inferences. | 本研究的方法论区分陈述与推断。 | 本研究讲述事实。 | 语境词不能因黑话嫌疑变成不同概念 | 0 |
| R17 | In 1750 he paid 30 livres, not 300.[12] | 1750年，他付了30里弗尔，并非300里弗尔。[12] | 1750年，他付了300里弗尔。 | 数字对比、货币与注号均受损 | 0 |
| R18 | The record contains no statement of motive. | 档案中没有记载动机。 | 我把档案查了一遍，没有找到动机。 | 新增译者检索经历冒充作者原话 | 0 |

R01 的忠实候选会被原脚本以冒号及翻案句判为失败。若按风格建议缩成“这是一份赠礼”，虽然更容易符合创作检查，却丢失否认税收性质以及市议会坚持此分类的两项信息。保真模式允许前一句；后一句相对基线的删改会完整报告，不能静默通过。

R09 是术语语义反例，不声称原风格规则必然导致该错误。测试另行配置 sawdust man→假钞骗子、panel game→暗板局、panel thief→暗板贼，验证大小写别名、同段与跨段、禁译词和译名次数。gold brick、green goods 等可按项目表分别配置；不能把一本书核准的黑话译名当成所有文献的唯一词义。

## 具体补丁

| 文件 | 修改 |
| --- | --- |
| human-writing/SKILL.md | 在全部创作流程前增加翻译分流，直接执行独立保真路线；原创作禁令限于创作模式 |
| human-writing/references/revision.md | 明确七遍删改和禁式清零不适用于 translation |
| human-writing/dist/human-writing-lite.md | 标明蒸馏版仅用于原创，译文使用完整版保真模式 |
| human-writing/references/translation-fidelity.md | 原文、基线、项目术语、逐句校订、引语保护、修改记录和人工复核；完整输入格式及命令 |
| human-writing/scripts/check_prose.py | 新增 --mode / --baseline / --manifest / --json；默认分支保留原行为 |
| human-writing/scripts/check_translation.py | 严格验证清单和基线哈希；只读检测对齐段号、引语、注号、数字、图片、术语与全部文字变化 |
| tests/ | 双语风险反例、CLI/退出码、只读和结构约束测试，以及原版创作输出快照 |

创作仍用原命令；翻译调用新模式：

```bash
python3 human-writing/scripts/check_prose.py 稿件.md
python3 human-writing/scripts/check_prose.py 候选译文.md --mode translation --baseline 润色前译文.md --manifest 对齐清单.json --json
```

清单包含逐段原文、段号、可选的整段锁定/指定保护文本，以及原词别名、核准译名和禁译词。其基线哈希可防意外选错版，不能防同时篡改基线和清单。采用者须固定并审阅输入，不允许为了通过检查覆盖基线、重算哈希或清空规则。完整结构见 [翻译保真流程](../human-writing/references/translation-fidelity.md)。

任何文字变化都返回待复核，即使是合理的搭配改善。退出码 0 只表示未改动且机械约束通过；1 表示结构违规或候选变化待复核；2 表示输入损坏或缺失。JSON 的 status 区分 blocked / review_required / unchanged / input_error。这是保护和审阅流程，不是自动翻译质量认证，也不禁止有依据的润色。

## 验证结果

- `python3 -m unittest discover -s tests -v`：29 个测试方法通过。其中双语风险测试覆盖 R01–R18 的忠实候选和危险改写，每项危险改写均被记录且不能静默通过。
- 创作回归用原提交实际生成的 10 组 stdout、stderr、退出码快照，分别测试默认命令与显式 creative 模式，20 次完整输出比较一致。覆盖硬禁式、标点、引语、警告、代码/URL 屏蔽、长文统计和无汉字输入。这是代表性回归，未宣称穷尽输入。
- 新模式测试包括嵌套/跨行/英文双引号/Markdown 块引文、英文弯撇号、数字和注号、图片、缺段/新增/重排/重复段、术语跨段、坏清单、重复 JSON 字段、缺文件、标准输入、退出码及文件不变。
- Skill 的 `quick_validate.py` 及 `git diff --check` 通过。
- 一次独立任务验证：测试者只读取修改后的 Skill 与其指定的翻译参考文件，处理三个自拟历史段落。保留否定对照、冒号、破折号、三次“我”、直接引语、[7] 注号和两项核准犯罪术语；引语不直接替换，将建议另列。其他改动给出原文、旧译、新译及不确定点。这不等于整书质量评测。

## 人工复核边界

正则不能跨语言证明命题等价，也不能判断全部典故、代词、语气、币值、中文数字、制度术语或首次括注。译名在段内出现不代表每次使用正确；词形需明确列为别名，异义须按适用章节维护清单。检查器也可能保留基线已有错误。

引语默认逐字锁定，合理纠错也会拦截并要求核准。英文单引号、复杂 HTML/引用式图片、特殊注号、单位和表格可整段锁定或显式保护，未声称全部自动解析。注号同段移位、相同文本段内移位、未知同义替换依靠差异及人工复核，不能靠计数冒充位置保护。输入以行首【段号】分段，底本含相同标记时必须建立可追溯映射。

本补丁不追溯修改已有译本，也不自动安装到其他翻译工作流。启用后应以小段真实底本及项目术语做人工验收。
