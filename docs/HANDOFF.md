# Planner 项目交接文件

最后更新：2026 年 10 月 16 日

这份文件记录 Planner 的全部现况，方便在新的对话里接着做。开新对话时，请让 Claude 先读这份文件（开场提示词见最后一节）。

---

## 1. 项目概况

一个类似 Microsoft Teams Planner 的个人规划 App，现在用来记功课、课程表和考试，以后上班也能用来管项目。

| 项目 | 位置 |
|---|---|
| App 网址（主要使用） | https://jewentew.github.io/Planner/ |
| GitHub 仓库（公开） | https://github.com/JewenTew/Planner |
| Claude 版本（另一份，数据分开） | https://claude.ai/artifact/GXGRWURQNX1zDRSssfnWB9 |
| Firebase 控制台 | https://console.firebase.google.com/project/planner-fc94d |
| API 密钥设定（Google Cloud） | https://console.cloud.google.com/apis/credentials?project=planner-fc94d |

- 电脑：已在 Edge 安装成 App（网页应用 PWA），不是从商店下载的。
- 手机：用同一个网址“添加到主屏幕”（Android 用 Chrome，iPhone 用 Safari）。
- **主要版本是 GitHub 网址那个**。Claude 版本的数据和 GitHub 版本分开，不会同步。

---

## 2. 账号与安全设定

- **GitHub**：账号 `JewenTew`。提交记录使用的身份：`JewenTew <JewenTew@users.noreply.github.com>`，只设定在这个仓库里。
- **Firebase 项目**：`planner-fc94d`（免费 Spark 方案，没有绑信用卡，不会扣钱）。
  - 登录方式：Google 登录，每次都会先显示选择账号的画面。
  - 授权网域：`localhost`、`planner-fc94d.firebaseapp.com`、`planner-fc94d.web.app`、`jewentew.github.io`。
  - Firestore 位置：asia-southeast1（新加坡）。
  - Firestore 规则：每个用户只能读写自己的数据：
    ```
    rules_version = '2';
    service cloud.firestore {
      match /databases/{database}/documents {
        match /users/{userId}/{document=**} {
          allow read, write: if request.auth != null && request.auth.uid == userId;
        }
      }
    }
    ```
- **API 密钥**（Browser key, auto created by Firebase）：已限制只能从以下网站使用（2026-10-16 设定，测试有效）：
  - `https://jewentew.github.io/*`
  - `https://planner-fc94d.firebaseapp.com/*`（Google 登录弹窗需要，不能删）
  - API 限制（25 APIs）保持 Firebase 默认，不要改。
  - 如果登录出错，可以把“应用限制”改回“无”来复原。
- `firebase-config.js` 里的设定值是公开识别码，放在公开仓库没有问题，安全靠上面的规则和密钥限制。
- 其他人可以用自己的 Google 账号登录，各自有独立的空白 Planner。作为项目拥有者，技术上能在 Firebase 控制台看到所有人的数据，给别人用之前要先告知（马来西亚 PDPA）。

---

## 3. 文件结构

```
Planner/
├─ src/planner.html      ← 原始程序（唯一要改的文件，约 3200 行）
├─ tools/build.py        ← 打包工具：src/planner.html → index.html
├─ index.html            ← 打包后的网站（不要直接改）
├─ sw.js                 ← 离线与更新（每次发布要改 CACHE 版本号）
├─ manifest.webmanifest  ← App 名称、图标、颜色
├─ firebase-config.js    ← Firebase 设定
├─ icons/                ← App 图标（粉蓝渐变 + 白色星星）
├─ docs/HANDOFF.md       ← 这份文件
└─ README.md             ← 功能介绍与开发说明
```

- `src/planner.html` 是“没有 html/head 外壳”的页面，同一个文件也直接发布成 Claude 版本。
- `tools/build.py` 会加上外壳：manifest、图标、`firebase-config.js`、service worker 注册。
- 整个 App 是单一 HTML 文件，用原生 JavaScript，没有框架、没有安装步骤。外部只用到 Google Fonts、Firebase compat SDK 10.14.1（gstatic）和 Tesseract.js 5.1.1（jsdelivr，图片识别）。

---

## 4. 修改与发布流程

1. 修改 `src/planner.html`。
2. 打包：`python tools/build.py`
3. 把 `sw.js` 里的 `CACHE` 版本号加 1（目前是 `planner-v21`），让已安装的 App 尽快更新。
4. **测试时不要碰真实数据**：复制一份 `index.html` 成 `_localtest.html`，把 `<script src="firebase-config.js"></script>` 换成 `<script>window.PLANNER_FIREBASE={apiKey:""};</script>`，这样会用浏览器本地储存，不会连云端。用 `python -m http.server 5178` 在本机开来测，测完删掉测试文件。
5. 提交并推送：`git add -A`、`git commit`、`git push`。GitHub Pages 大约 1 分钟后更新。
6. （可选）把 `src/planner.html` 重新发布到上面的 Claude 版本链接。
7. 打开 App 按 **Ctrl + Shift + R** 确认是新版本。

注意：
- Windows 的命令行工具有时会把字符串里的反斜线吃掉。写正则表达式时用 `/.../` 字面量，或用 `RegExp(/.../.source)` 组合，不要用字符串。
- 只有在仓库里的东西才算保存。对话用的临时文件夹可能会被删掉。

---

## 5. 数据结构（Firestore：`users/{uid}/...`）

| 集合 | 内容 |
|---|---|
| `plans` | 计划：`name`、`color`（c1 到 c6）、`buckets[{id,name}]`、`labels`、`archived`、`gradeTarget` |
| `tasks` | 任务：`planId`、`title`、`bucketId`、`progress`（todo/doing/done）、`priority`、`start`、`due`（YYYY-MM-DD）、`assignee`、`labels`、`notes`、`checklist`、`links`、`repeat`、`myDay`、`order`、成绩字段 `inGrades`/`weight`/`score`/`outOf` |
| `classes` | 课程：`title`、`code`、`type`、`day`（1=星期一）、`start`/`end`（HH:MM 24 小时）、`room`、`lecturer`、`color`、`planId`；只上一次的课有 `date`；改时间的课有 `replaces{id,date}`；每周课程取消某天记在 `skip[]`；考试 `kind:'exam'`；出席记录 `att{日期: present/absent}` |
| `settings` | `semester`（`name`、`start`、`end`、`breaks[]`、`attMin` 最低出席率）；`meta`（`lastBackup`、`snoozeUntil`） |

- 没登录时，同样的结构存在浏览器 `localStorage` 的 `planner-data`；介面偏好（语言、主题、时间格式等）存在 `planner-prefs`。
- 备份文件格式：`{ app: 'planner', version: 1, plans, tasks, classes, settings }`，导入时会逐项检查内容。

---

## 6. 已完成的功能

**计划与任务**
- 概览：逾期、今天、本周统计；全部计划的周或月日历；截止日期倒计时清单；全局搜索。
- 看板（拖动任务、拖动存储桶、自定义排序）、表格、日程、图表、成绩。
- 任务：存储桶、进度、优先级、开始与截止日期、负责人、标签、备注、清单、链接、重复任务。
- 多选（批量删除、批量完成），删除可撤销（10 秒内，或 Ctrl + Z）。
- 我的一天：每天挑任务，隔天自动清空，也会显示今天的课。
- 归档计划（可恢复）；计划设定可改名称、颜色、存储桶和标签名称；键盘快捷键（按 ? 查看）。

**课程表**
- 每周课程表（显示日期、周数、现在时间红线），可切换上下周。
- 补课（只上一次）、只改某一次的时间、只取消某一次。
- 学期设置：开始与结束日期、假期（周数不计算假期周），学期外不显示每周课程。
- 从图片导入课程表（本机文字识别，导入前可在表格里检查修改）；课程代码保留前面的字母（例如 C CS6314 会变成 CCS6314）。
- 考试：倒计时、日历红色标示、考前 3 天提醒。
- 出席记录：在“我的一天”或课程表标记，每科出席率，低于标准会提醒（默认 80%）。
- 为每门课一键建立计划并连接；计划页面显示每周上课时间、下次考试和出席率。
- 清空课程表（可撤销）。

**其他**
- Google 登录与云端同步（电脑和手机同步）。
- 可安装成 App、可离线打开；图标显示“逾期 + 今天到期”数量；每天第一次打开时提醒。
- 备份与还原（导出或导入 JSON），超过 30 天没备份会提醒。
- 中英文切换、浅色或深色、24 小时或 AM/PM（都在左下角“设置”里）。
- 介面：白色 + 淡粉 + 淡蓝。

---

## 7. 已知限制

- **图片识别**：截图的字太小会认不出来。要用学校系统的日历视图，放大网页后只截课程表那块。偶尔会把数字看错（例如 6 看成 5），导入前要检查。
- **输入时间的小框**是 Windows 自带的控件，会按电脑设定显示，不会跟着 24h 或 AM/PM 开关改变（只影响显示，不影响保存的值）。
- **没有真正的后台提醒**：浏览器不允许网页在关闭时发通知。可以用“导出到手机日历”这个待做功能来补。
- **Claude 版本的数据**和 GitHub 版本分开，不会同步。
- **免费额度**：Firestore 每天大约 5 万次读取、2 万次写入，几个人用完全够。

---

## 8. 待确认与下一步

**待确认**
- [ ] 手机（特别是 iPhone）安装和 Google 登录是否正常。
- [ ] 用“为每门课建立计划”整理现有作业。
- [ ] 输入真实的学期日期和假期。
- [ ] 加入期末考试（可以用 Show Exam Schedule 的截图）。

**之后可以做的功能（按推荐顺序）**
1. 导出到手机日历（.ics）：课程、考试、截止日期，用手机自带提醒。
2. 考试安排也支持从截图导入。
3. 整理计划页面的工具栏（搜索、筛选、多选、排序、分组），做法和课程表的菜单一样。
4. 复制任务或计划当模板。
5. 多选批量修改（截止日期、优先级、存储桶）。
6. 在日历上拖动任务改日期。
7. 预估时间与每周工作量、专注计时（番茄钟）。
8. 小组共享计划（需要改数据结构和 Firestore 规则，工作量较大）。

---

## 9. 新对话的开场提示词

复制下面这段贴到新对话：

```
我有一个自己的 Planner 网页 App，代码在 https://github.com/JewenTew/Planner 。
请先读仓库里的 docs/HANDOFF.md，了解项目现况、文件结构和修改流程，再帮我继续。
修改时请改 src/planner.html，用 python tools/build.py 打包，sw.js 的 CACHE 版本号加 1，
测试时不要连接我真实的 Firebase 数据，测好再推送到 GitHub。
这次我想做的是：（在这里写你想改或想加的功能）
```

提醒：新对话需要能使用 GitHub（clone 和 push 这个仓库）。如果新的电脑没有登录过 GitHub，第一次推送时会跳出 GitHub 登录窗口，请自己登录。
