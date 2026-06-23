# maestro-tests

[Maestro](https://maestro.mobile.dev/) E2E 测试集合，按 App 与平台分目录存放。

## 目录结构

```
maestro-tests/
├── android/
│   ├── textnum/                        # TextNum App（Android）
│   │   ├── textnum_login.yaml          # 子 flow：Google 登录
│   │   ├── call_test.yaml
│   │   └── message_test.yaml
│   └── sauce/                          # Sauce Labs 演示（Android）
│       └── android_sauce_login.yaml
├── ios/
│   └── sauce/
│       └── ios_sauce_login.yaml
└── web/
    └── sauce/
        └── web_sauce_login.yaml
```

## 命名约定

所有 flow 文件使用 `{app}_{purpose}.yaml`，**不再使用通用的 `login.yaml`**，避免跨目录重名：

| 文件 | 目标 |
|------|------|
| `android/textnum/textnum_login.yaml` | TextNum — Google 登录子 flow |
| `android/sauce/android_sauce_login.yaml` | Swag Labs Android — `com.swaglabsmobileapp` |
| `ios/sauce/ios_sauce_login.yaml` | Swag Labs iOS — `com.saucelabs.SwagLabsMobileApp` |
| `web/sauce/web_sauce_login.yaml` | Sauce Demo 网站 — `https://www.saucedemo.com` |

## 子 flow 不会混用

Maestro 解析 `file: xxx.yaml` 时，路径**相对于当前 flow 文件所在目录**，不会在项目内全局搜索。

| 引用方 | 实际加载的文件 |
|--------|----------------|
| `android/textnum/call_test.yaml` → `textnum_login.yaml` | `android/textnum/textnum_login.yaml` |
| `android/textnum/message_test.yaml` → `textnum_login.yaml` | `android/textnum/textnum_login.yaml` |

Sauce 各平台的 login flow 均为独立文件，互不引用。

## 运行方式

需已安装 [Maestro CLI](https://maestro.mobile.dev/getting-started/installing-maestro)。

### TextNum（Android）

```bash
maestro test android/textnum/call_test.yaml
maestro test android/textnum/message_test.yaml
maestro test android/textnum/textnum_login.yaml
```

`call_test.yaml` / `message_test.yaml` 使用 `launchApp`（不清除状态）。仅当界面出现「Log in / Sign up」时才执行 `textnum_login.yaml`。

### Sauce Labs 演示（冒烟）

```bash
maestro test android/sauce/android_sauce_login.yaml
maestro test ios/sauce/ios_sauce_login.yaml
maestro test web/sauce/web_sauce_login.yaml
```

## 编写约定

1. **文件命名**：`{app}_{purpose}.yaml`（如 `textnum_login.yaml`、`android_sauce_login.yaml`）。
2. **目录命名**：全小写（如 `textnum/`，不用 `TextNum/`）。
3. **相对路径引用**：`runFlow` 的 `file` 只写同目录文件名。
4. **条件登录**：主 flow 用 `when: visible: "Log in / Sign up"` 包裹登录子 flow，支持已登录态复跑。

## 依赖与前提

- **TextNum**：设备已登录 Google 账号；拨号/短信测试需真机或具备相应能力的模拟环境。
- **Sauce Demo**：使用标准账号 `standard_user` / `secret_sauce`（已写在 flow 中）。

## 关于目录大小写

Git 区分路径大小写，macOS 默认文件系统不区分。若远程仓库显示 `TextNum/` 而本地是 `textnum/`，需用 `git mv` 两步重命名后提交，远程才会更新：

```bash
git mv android/TextNum android/textnum_tmp
git mv android/textnum_tmp android/textnum
```
