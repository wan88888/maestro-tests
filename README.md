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

## 编写约定

1. **文件命名**：`{scenario}.yaml`，目录已表达平台与 App。
2. **目录命名**：全小写（`textnum/`、`esimnum/`）。
3. **子 flow 引用**：`runFlow` 的 `file` 只写同目录文件名（如 `login.yaml`）。
4. **条件步骤**：用 `when` 跳过登录、Cookie 等可选 UI。
5. **Web 视口**：无最大化选项，用 `--screen-size 1920x1080` 固定视口。

## 依赖与前提

- **TextNum**：设备已登录 Google 账号；拨号/短信需真机或具备相应能力的模拟环境。
- **Sauce Demo**：账号 `standard_user` / `secret_sauce`（已写在 flow 中）。
