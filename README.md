# 儿童绘本生成器 📚

基于 AI 的儿童绘本故事和插图生成应用。

## 功能特点

- 🎨 AI 生成儿童故事
- 🖼️ 自动生成配套插图
- 👶 按年龄段定制内容
- 📖 多种故事风格选择

## 技术栈

- **后端**: Python + FastAPI
- **AI**: OpenAI API / 通义千问
- **图像处理**: Pillow

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入 API Key
```

### 启动服务

```bash
python main.py
# 或
uvicorn main:app --reload
```

访问 http://localhost:8000 查看 API 文档。

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 健康检查 |
| `/health` | GET | 健康状态 |
| `/api/generate-story` | POST | 生成故事 |

## 项目结构

```
kids-story-generator/
├── main.py              # 应用入口
├── requirements.txt     # 依赖列表
├── README.md           # 项目说明
└── .env.example        # 环境变量示例
```

## 开发计划

- [ ] 实现故事生成逻辑
- [ ] 集成 AI 绘图 API
- [ ] 添加用户系统
- [ ] 支持导出 PDF/EPUB

## License

MIT
