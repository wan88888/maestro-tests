# maestro-tests

[Maestro](https://maestro.mobile.dev/) E2E 测试集合，按平台与 App 分目录存放。

## 目录结构

```
maestro-tests/
├── android/
│   ├── textnum/
│   │   ├── login.yaml           # 子 flow：Google 登录
│   │   ├── call.yaml
│   │   └── message.yaml
│   ├── esimnum/
│   │   ├── login.yaml
│   │   ├── add_creditcard.yaml
│   │   └── user_purchase.yaml
│   ├── editor/                     # Vidma 视频编辑器
│   │   ├── new_project.yaml        # 主编排：新建项目全流程
│   │   ├── ailab.yaml              # 主编排：AI Lab 全量回归
│   │   ├── setup_project.yaml      # 子 flow
│   │   ├── add_effect.yaml
│   │   ├── generate_once.yaml
│   │   ├── after_credit.yaml
│   │   ├── run_text_to_video.yaml  # 单场景入口（含 launchApp）
│   │   └── ailab/                  # 场景步骤（无 launchApp，供编排复用）
│   │       ├── text_to_video.yaml
│   │       └── ...
│   ├── downloader/                 # Downloader（独立 flow，无公共骨架）
│   │   ├── download_dailymotion_video.yaml
│   │   ├── download_tiktok_video.yaml
│   │   └── play_download_video.yaml
│   └── sauce/
│       └── login.yaml
├── ios/
│   ├── esimnum/
│   │   └── checkout.yaml
│   └── sauce/
│       └── login.yaml
└── web/
    ├── esimnum/
    │   └── checkout.yaml
    └── sauce/
        └── login.yaml
```

## 命名约定

路径为 `{platform}/{app}/{scenario}.yaml`，**文件名只写场景名**，App 与平台由目录区分。

| 路径 | 说明 |
|------|------|
| `android/textnum/call.yaml` | TextNum — 拨号 + 挂断 + 历史记录 |
| `android/textnum/message.yaml` | TextNum — 发短信/图片 + 历史记录 |
| `android/textnum/login.yaml` | TextNum — Google 登录子 flow |
| `android/esimnum/user_purchase.yaml` | eSIMnum Android — 购买套餐（支持 `COUNTRY`） |
| `android/sauce/login.yaml` | Swag Labs Android 冒烟 |
| `ios/esimnum/checkout.yaml` | eSIMnum Safari — 结账页未登录拦截 |
| `ios/sauce/login.yaml` | Swag Labs iOS 冒烟 |
| `web/esimnum/checkout.yaml` | eSIMnum Web — 结账页未登录拦截 |
| `web/sauce/login.yaml` | Sauce Demo 网站冒烟 |
| `android/editor/new_project.yaml` | Vidma — 新建项目编辑导出全流程 |
| `android/editor/ailab.yaml` | Vidma — AI Lab 六项生成全量回归 |
| `android/downloader/download_dailymotion_video.yaml` | Downloader — Dailymotion 内置 Tab 下载 |
| `android/downloader/download_tiktok_video.yaml` | Downloader — TikTok 复制链接下载 |
| `android/downloader/play_download_video.yaml` | Downloader — 播放已下载视频 |

同目录下多个 `login.yaml`（如 `android/textnum/login.yaml` 与 `android/sauce/login.yaml`）**不会混用**：`runFlow` 的 `file` 相对于当前 flow 所在目录解析。

## 运行方式

需已安装 [Maestro CLI](https://maestro.mobile.dev/getting-started/installing-maestro)。

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

### eSIMnum（Web）

```bash
maestro test -p web --screen-size 1920x1080 web/esimnum/checkout.yaml
maestro test -p web -e COUNTRY="Japan" web/esimnum/checkout.yaml
```

Web 搜索结果用 `css` 定位，见 `checkout.yaml`。

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

### Vidma Editor（Android）

```bash
# 新建项目全流程
maestro test android/editor/new_project.yaml

# AI Lab 全量回归（单会话连续跑 6 个场景）
maestro test android/editor/ailab.yaml

# 单场景调试
maestro test android/editor/run_text_to_video.yaml
maestro test android/editor/run_image_to_video.yaml

# 按 tag 筛选（Maestro 2.x）
maestro test --include-tags text-to-image android/editor/ailab/
```

`ailab/` 下为场景步骤（假设已在 AI Lab 内）；`run_*.yaml` 含 `launchApp` 可单独执行。

### Downloader（Android）

当前为**独立 flow**，每个站点单独维护，暂无公共骨架（`common/`、`download_site.yaml`、`sites.yaml` 已移除）。

```bash
maestro test android/downloader/download_dailymotion_video.yaml
maestro test android/downloader/download_tiktok_video.yaml
maestro test android/downloader/play_download_video.yaml
```

| Flow | 说明 | 状态 |
|------|------|------|
| `download_dailymotion_video.yaml` | App 内置 Dailymotion Tab，选视频后 list 下载 | 待设备验证 |
| `download_tiktok_video.yaml` | 跳转 TikTok 复制链接，回 App 解析 | 待设备验证 |
| `play_download_video.yaml` | 打开下载列表播放已下载项 | 待设备验证 |

Top100 其余站点用例尚未纳入；后续可按站点逐步新增 `download_*_video.yaml`。

## 编写约定

1. **文件命名**：`{scenario}.yaml`，目录已表达平台与 App。
2. **目录命名**：全小写（`textnum/`、`esimnum/`）。
3. **子 flow 引用**：`runFlow` 的 `file` 相对于当前 flow 所在目录；跨目录用 `../`（如 `ailab/` → `../generate_once.yaml`）。
4. **长流程拆分**：主编排只做 `runFlow`；重复步骤（确认、关面板、生成、评星）抽成子 flow。
5. **条件步骤**：用 `when` 跳过登录、Cookie、评星等可选 UI。
6. **Web 视口**：无最大化选项，用 `--screen-size 1920x1080` 固定视口。

## 依赖与前提

- **TextNum**：设备已登录 Google 账号；拨号/短信需真机或具备相应能力的模拟环境。
- **Downloader**：真机或模拟器已安装 `free.video.downloader.converter.music`；WebView 站点 UI 易变，各 flow 需单独维护与验证。
- **Sauce Demo**：账号 `standard_user` / `secret_sauce`（已写在 flow 中）。
