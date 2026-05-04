# 本地测试

> 在本地测试已构建的 Imbrace SDK 包，模拟真实消费者安装的方式。

本指南允许测试**已构建的包**，方式与消费者从 npm 或 pip 安装完全相同 — 而非原始源码。在发布新版本前，或重现消费者报告的 bug 时使用。

## 前提条件

- TypeScript：Node 18+
- Python：Python 3.10+ 和 `pip`
- 如需从 Ansible 解密环境变量，需配置 AWS credentials（profile `imbrace`）

## 环境 URL

相同的 gateway base URL 适用于两个 SDK。在测试环境中设置一次：

| 环境       | `IMBRACE_BASE_URL` / `IMBRACE_GATEWAY_URL` |
| ---------- | ------------------------------------------ |
| develop    | `https://app-gateway.dev.imbrace.co`       |
| sandbox    | `https://app-gateway.sandbox.imbrace.co`   |
| stable     | `https://app-gatewayv2.imbrace.co`         |

## 凭证

从 Ansible 拉取实时凭证（或从 portal 粘贴）：

```bash
# 从 SDK repo 根目录
AWS_PROFILE=imbrace sops -d ansible/dev/secrets.enc.env | grep IMBRACE >> /tmp/imbrace.env
```

实时调用所需的最低配置：

| 变量          | 获取方式                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------- |
| `IMBRACE_API_KEY` | Imbrace Portal，或使用现有 access token 调用 `POST /private/backend/v1/third_party_token` |
| `IMBRACE_BASE_URL` | 上表中的某个 URL（未设置时默认 dev）                              |

Org context 已编码在 API key 中 — 不需要传递 organization id。

---

## TypeScript — 链接已构建的 dist

### 一次性设置

```bash
cd ts
npm install
npm run build
npm link        # 全局暴露 @imbrace/sdk
```

然后在测试目录：

```bash
cd ts/tests/local
npm link @imbrace/sdk
cp .env.example .env
# 填写 .env
```

### 运行测试

```bash
cd ts/tests/local
node test-local.mjs
```

- **未提供凭证** — 仅运行实例化 + 资源接口检查（无网络请求）。
- **设置了 `IMBRACE_API_KEY`** — 对 `IMBRACE_BASE_URL` 中的 gateway 运行完整实时 API 检查。

### SDK 更改的迭代流程

每次编辑都需要重新构建，链接才会使用新的 dist：

```bash
# 终端 1 — ts/
npm run dev          # tsc --watch

# 终端 2 — ts/tests/local
node test-local.mjs  # 随时重新运行
```

---

## Python — 从 wheel 或 editable 安装

### Editable 安装（最快迭代）

从 `py/` 目录：

```bash
cd py
pip install -e .
```

代码编辑无需重新安装即可生效。

### Wheel 安装（验证发布形状）

```bash
cd py
python -m build               # 生成 dist/imbrace-*.whl
pip install dist/imbrace-*.whl --force-reinstall
```

这可以发现 editable 安装隐藏的缺失文件、打包 bug 和导入路径问题。

### 运行测试

```bash
cd py
pip install -r tests/requirements.txt
python -m pytest tests/
```

镜像[完整流程指南](/zh-cn/sdk/full-flow-guide/)的全流程回归测试：

```bash
cd test-pip-pkg/py
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/test_guide_flow.py -v
```

该测试同时使用 `IMBRACE_API_KEY` 和 `IMBRACE_ACCESS_TOKEN` 运行，以覆盖两种 auth 模式。

---

## 切换环境

```bash
IMBRACE_BASE_URL=https://app-gateway.sandbox.imbrace.co node test-local.mjs
```

```bash
IMBRACE_BASE_URL=https://app-gateway.sandbox.imbrace.co python -m pytest tests/
```

---

## 故障排查

**`Cannot find package '@imbrace/sdk'`**（TypeScript）
在测试目录内重新运行 `npm link @imbrace/sdk`。如果删除并重新安装 `ts/` 中的 `node_modules`，链接可能会断开。

**`ERR_MODULE_NOT_FOUND`（dist 文件）**（TypeScript）
包尚未构建，或添加了新的源文件但未重新构建。在 `ts/` 中运行 `npm run build`。

**`ModuleNotFoundError: No module named 'imbrace'`**（Python）
包未安装在当前 venv 中。重新运行 `pip install -e .`（editable）或 `pip install dist/imbrace-*.whl`。

**实时调用返回 401 / 403**
凭证已过期、被撤销或错误。生成新的 API key：

```bash
curl -X POST https://app-gateway.dev.imbrace.co/private/backend/v1/third_party_token \
  -H "x-access-token: <your_existing_token>" \
  -H "Content-Type: application/json" \
  -d '{"expirationDays": 30}'
```

其他运行时错误，参阅[错误处理](/zh-cn/sdk/error-handling/)和[问题排查](/zh-cn/guides/troubleshooting/)。
