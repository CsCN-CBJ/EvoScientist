# 部署指南

## 环境要求

- Python 3.11+（< 3.14）
- 推荐 [uv](https://docs.astral.sh/uv/) 或 conda 管理依赖

## 安装

### 快速安装

```bash
uv tool install EvoScientist
```

### 从源码安装（开发）

```bash
git clone https://github.com/EvoScientist/EvoScientist.git
cd EvoScientist
uv sync --dev
uv run pre-commit install
```

### 通道可选依赖

```bash
uv pip install "EvoScientist[telegram]"    # Telegram
uv pip install "EvoScientist[discord]"     # Discord
uv pip install "EvoScientist[slack]"       # Slack
uv pip install "EvoScientist[wechat]"      # WeChat
uv pip install "EvoScientist[feishu]"      # Feishu
uv pip install "EvoScientist[qq]"          # QQ
uv pip install "EvoScientist[all-channels]" # 全部通道
```

## 配置

```bash
EvoSci onboard  # 交互式配置向导
```

或手动设置环境变量：

```bash
export ANTHROPIC_API_KEY="sk-..."
export TAVILY_API_KEY="tvly-..."
```

## 启动

```bash
EvoSci                     # 交互式 TUI
EvoSci --ui cli            # 经典 CLI
EvoSci -p "问题"           # 单次查询
EvoSci serve               # 无头模式（仅通道）
EvoSci --workdir /path     # 指定工作目录
EvoSci --auto-approve      # 自动批准命令
```

## Docker 部署

### Webhook 通道（需公网 IP）

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install evoscientist[feishu,wechat]
EXPOSE 9000 9001
CMD ["EvoSci", "serve"]
```

```bash
docker build -t evoscientist .
docker run -d -p 9000:9000 -p 9001:9001 \
  -e EVOSCIENTIST_CHANNEL_ENABLED="feishu,wechat" \
  -e EVOSCIENTIST_FEISHU_APP_ID="cli_xxx" \
  evoscientist
```

### Polling/WebSocket 通道（无需公网 IP）

```bash
docker run -d \
  -e EVOSCIENTIST_CHANNEL_ENABLED="telegram" \
  -e EVOSCIENTIST_TELEGRAM_BOT_TOKEN="123456:ABC-xxx" \
  evoscientist
```

## 健康检查

```bash
curl http://localhost:8080/healthz
```

## 常见问题

### MCP 服务器连接失败

启动时不会阻塞，失败的服务器被跳过并输出警告。检查 `mcp.yaml` 配置和 `npx` 是否可用。

### WeChat API 错误 60020

在企业微信管理后台的「可信 IP」列表中添加服务器公网 IP。

### Token 刷新失败

飞书/微信/钉钉 Token 自动刷新（2h TTL，5 分钟安全余量）。检查网络和代理设置。

### Webhook 通道收不到消息

确保 webhook URL 公网可达。本地开发可使用 `ngrok http 9000`。
