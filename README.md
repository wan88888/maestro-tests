# maestro-tests

[Maestro](https://maestro.mobile.dev/) E2E 测试集合，按平台与 App 分目录存放。

## 目录结构

```
maestro-tests/
├── android/
│   ├── textnum/
│   │   ├── login.yaml              # 子 flow：Google 登录
│   │   ├── call.yaml
│   │   └── message.yaml
│   ├── esimnum/
│   │   ├── login.yaml
│   │   ├── add_creditcard.yaml
│   │   └── user_purchase.yaml
│   ├── editor/                     # Vidma 视频编辑器
│   │   ├── new_project.yaml        # 主编排：新建项目编辑导出全流程
│   │   ├── ailab.yaml              # 主编排：AI Lab 六项生成全量回归
│   │   ├── run_*.yaml              # 单场景入口（含 launchApp）
│   │   ├── wait_for_success.yaml   # 子 flow：等成功文案 + 偶发关评星
│   │   ├── dismiss_rating_if_visible.yaml
│   │   ├── generate_once.yaml      # credit → 生成 → 等成功
│   │   ├── export_and_play.yaml
│   │   └── ailab/                  # 场景步骤（无 launchApp，供编排复用）
│   ├── downloader/                 # Downloader（每站点独立 flow）
│   │   ├── download_dailymotion_video.yaml
│   │   ├── download_tiktok_video.yaml
│   │   └── play_download_video.yaml
│   ├── recorder/                   # Vidma 录屏
│   │   ├── record_flow1.yaml       # 主编排：通知栏开始/停止
│   │   ├── new_record.yaml         # 主编排：App 内开始/停止
│   │   ├── open_notification.yaml  # 子 flow：上滑展开通知栏
│   │   ├── notification_tap.yaml   # 子 flow：重试开通知栏 + 点按钮
│   │   ├── browse_tiktok.yaml
│   │   └── ...
│   └── sauce/
│       └── login.yaml
├── ios/
│   ├── esimnum/
│   │   └── checkout.yaml
│   └── sauce/
│       └── login.yaml
└── web/
    └── sauce/
        └── login.yaml
```

## 用例一览

路径为 `{platform}/{app}/{scenario}.yaml`，**文件名只写场景名**，App 与平台由目录区分。

| 路径 | 说明 |
|------|------|
| `android/textnum/call.yaml` | TextNum — 拨号 + 挂断 + 历史记录 |
| `android/textnum/message.yaml` | TextNum — 发短信/图片 + 历史记录 |
| `android/textnum/login.yaml` | TextNum — Google 登录子 flow |
| `android/esimnum/user_purchase.yaml` | eSIMnum Android — 购买套餐（支持 `COUNTRY`） |
| `android/esimnum/login.yaml` | eSIMnum — Google 登录子 flow |
| `android/esimnum/add_creditcard.yaml` | eSIMnum — Stripe 测试卡填写子 flow |
| `android/sauce/login.yaml` | Swag Labs Android 冒烟 |
| `ios/esimnum/checkout.yaml` | eSIMnum Safari — 结账页未登录拦截 |
| `ios/sauce/login.yaml` | Swag Labs iOS 冒烟 |
| `web/sauce/login.yaml` | Sauce Demo 网站冒烟 |
| `android/editor/new_project.yaml` | Vidma — 新建项目编辑导出全流程 |
| `android/editor/ailab.yaml` | Vidma — AI Lab 六项生成全量回归 |
| `android/editor/run_text_to_video.yaml` 等 | Vidma — AI Lab 单场景调试入口 |
| `android/downloader/download_dailymotion_video.yaml` | Downloader — Dailymotion 内置 Tab 下载 |
| `android/downloader/download_tiktok_video.yaml` | Downloader — TikTok 复制链接下载 |
| `android/downloader/play_download_video.yaml` | Downloader — 播放已下载视频 |
| `android/recorder/record_flow1.yaml` | Vidma 录屏 — 通知栏开始/停止全流程 |
| `android/recorder/new_record.yaml` | Vidma 录屏 — App 内开始/停止全流程 |

同目录下多个 `login.yaml`（如 `android/textnum/login.yaml` 与 `android/sauce/login.yaml`）**不会混用**：`runFlow` 的 `file` 相对于当前 flow 所在目录解析。

## 运行方式

需已安装 [Maestro CLI](https://maestro.mobile.dev/getting-started/installing-maestro)（本地验证版本 2.6.1）。

### TextNum（Android）

```bash
maestro test android/textnum/call.yaml
maestro test android/textnum/message.yaml
maestro test android/textnum/login.yaml
```

`call.yaml` / `message.yaml` 在出现「Log in / Sign up」时执行同目录 `login.yaml`。

### eSIMnum（Android App）

```bash
maestro test android/esimnum/user_purchase.yaml
maestro test -e COUNTRY="Japan" android/esimnum/user_purchase.yaml
```

### eSIMnum（iOS Safari）

```bash
maestro test ios/esimnum/checkout.yaml
```

### Sauce Labs 演示

```bash
maestro test android/sauce/login.yaml
maestro test ios/sauce/login.yaml
maestro test -p web web/sauce/login.yaml
```

Web 测试可用 `--screen-size 1920x1080` 固定视口。

### Vidma Editor（Android）

```bash
# 新建项目全流程（含导出播放、重命名）
maestro test android/editor/new_project.yaml

# AI Lab 全量回归（单会话连续跑 6 个场景）
maestro test android/editor/ailab.yaml

# 单场景调试
maestro test android/editor/run_text_to_video.yaml
maestro test android/editor/run_image_to_video.yaml
maestro test android/editor/run_text_to_image.yaml
maestro test android/editor/run_image_to_image.yaml
maestro test android/editor/run_ai_kiss.yaml
maestro test android/editor/run_ai_group.yaml

# 按 tag 筛选（Maestro 2.x）
maestro test --include-tags text-to-image android/editor/ailab/
```

| Flow | 说明 |
|------|------|
| `new_project.yaml` | 新建项目 → 特效/音频/文字/贴纸/滤镜 → 导出播放 → 重命名 |
| `ailab.yaml` | 连续跑 text/image to video、text/image to image、ai_kiss、ai_group |
| `generate_once.yaml` | 点 credit 生成，经 `after_credit.yaml` 等待成功 |
| `wait_for_success.yaml` | 等成功文案；评星偶发遮挡时循环 `back` 关闭 |
| `export_and_play.yaml` | 导出并播放，成功文案 `Video Saved,Enjoy!!!` |
| `ailab/*.yaml` | 各 AI 场景步骤，带 `tags` 可筛选 |

`ailab/` 下为场景步骤（假设已在 AI Lab 内）；`run_*.yaml` 含 `launchApp` 可单独执行。

### Downloader（Android）

每个站点独立维护，无公共配置层。

```bash
maestro test android/downloader/download_dailymotion_video.yaml
maestro test android/downloader/download_tiktok_video.yaml
maestro test android/downloader/play_download_video.yaml
```

| Flow | 说明 |
|------|------|
| `download_dailymotion_video.yaml` | 内置 Dailymotion Tab，WebView 选视频后下载（`androidWebViewHierarchy: devtools`） |
| `download_tiktok_video.yaml` | 跳转 TikTok，`Share.*` 复制链接，回 App 解析 |
| `play_download_video.yaml` | 打开下载列表，播放已下载项 |

### Vidma Recorder（Android）

录屏全流程：启动 App → 配置画质 → 开始录制 → 切 TikTok 滑动浏览 → 停止录制 → 关闭结果页 → 清理。

```bash
# 通知栏开始/停止（含 configure_recording）
maestro test android/recorder/record_flow1.yaml

# App 内开始/停止（跳过画质配置）
maestro test android/recorder/new_record.yaml
```

| Flow | 说明 |
|------|------|
| `record_flow1.yaml` | 通知栏 Record/Stop + 画质配置 + TikTok 浏览 |
| `new_record.yaml` | App 内 `ivRecorder` 开始、`Stop` 结束 |
| `launch_recorder.yaml` | 启动并授予全部权限 |
| `configure_recording.yaml` | 内录麦克风 + 1080P / 高画质 / 120FPS |
| `open_notification.yaml` | 上滑一次展开通知栏（原子手势） |
| `notification_tap.yaml` | 重试开通知栏（最多 5 次）直到 `Record`/`Stop` 可见并点击 |
| `browse_tiktok.yaml` | 切 TikTok，上滑 5 次浏览 feed |
| `start_via_notification.yaml` / `stop_via_notification.yaml` | 通知栏开始/停止 |
| `start_in_app.yaml` / `stop_in_app.yaml` | App 内开始/停止 |
| `finish_with_close.yaml` | 关闭录制结果页 |
| `teardown.yaml` | 关闭 TikTok 与录屏 App |

子 flow 无 `launchApp`，由主编排 `runFlow` 串联；`notification_tap.yaml` 通过 `BUTTON_TEXT` 环境变量区分 Record/Stop。

## 编写约定

1. **文件命名**：`{scenario}.yaml`，目录已表达平台与 App。
2. **目录命名**：全小写（`textnum/`、`esimnum/`）。
3. **子 flow 引用**：`runFlow` 的 `file` 相对于当前 flow 所在目录；跨目录用 `../`（如 `ailab/` → `../generate_once.yaml`）。
4. **长流程拆分**：主编排只做 `runFlow`；重复步骤（确认、关面板、生成、评星）抽成子 flow。
5. **条件步骤**：用 `when` / `optional: true` 跳过登录、Cookie、评星等可选 UI。
6. **重试与等待**：原子手势放子 flow（如 `open_notification.yaml`），重试与成功条件放上层（如 `notification_tap.yaml`、`wait_for_success.yaml`）。
7. **长耗时等待**：慢加载用 `extendedWaitUntil`（如 WebView `completeLoadView`）；`tapOn` 默认只等约 7–10 秒，不宜替代长等待。
8. **正则选择器**：`text` / 字符串 shorthand 默认按正则匹配（如 TikTok `Share.*`）。
9. **Web 视口**：无最大化选项，用 `--screen-size 1920x1080` 固定视口。

## 依赖与前提

- **TextNum**：设备已登录 Google 账号；拨号/短信需真机或具备相应能力的模拟环境。
- **eSIMnum**：Android 需 Google 登录；Stripe 使用测试卡 `4242…`（见 `add_creditcard.yaml`）；iOS 为 Safari 打开 `esimnum.com`。
- **Vidma Editor**：真机或模拟器已安装 `vidma.video.editor.videomaker`；AI 生成/导出可能耗时较长；评星弹窗偶发，会遮挡成功文案。
- **Downloader**：已安装 `free.video.downloader.converter.music`；TikTok 需安装且可正常使用；Dailymotion 为 WebView，UI 变更时需单独维护。
- **Vidma Recorder**：已安装 TikTok（`com.zhiliaoapp.musically`）；需允许录屏、麦克风等权限；部分机型展开通知栏需多次上滑（flow 内已重试）。
- **Sauce Demo**：账号 `standard_user` / `secret_sauce`（已写在 flow 中）。
