# 量化投研助手 RAG 系统

基于RAG（检索增强生成）技术的量化投研智能助手系统。

## 项目结构

```
quant_assistant/
├── backend/                 # 后端服务
│   ├── api/                # API接口
│   ├── core/               # 核心功能
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   └── utils/              # 工具函数
├── data/                   # 数据目录
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后的数据
│   └── vector_store/      # 向量存储
├── frontend/              # 前端应用
│   ├── src/              # 源代码
│   ├── public/           # 静态资源
│   └── tests/            # 测试文件
├── ml/                    # 机器学习模块
│   ├── models/           # 模型定义
│   ├── training/         # 训练脚本
│   └── evaluation/       # 评估脚本
├── scripts/              # 工具脚本
├── tests/                # 测试目录
├── docs/                 # 文档
├── docker/               # Docker配置
└── config/               # 配置文件
```

## 环境要求

- Python 3.8+
- Node.js 16+
- Docker
- Milvus
- Neo4j
- MySQL
- Redis

## 快速开始

1. 克隆项目
```bash
git clone [项目地址]
cd quant_assistant
```

2. 安装依赖
```bash
# 后端依赖
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

3. 启动服务
```bash
# 启动后端服务
python backend/main.py

# 启动前端服务
cd frontend
npm run dev
```

## 开发指南

详细的开发指南请参考 [docs/development.md](docs/development.md)

## 贡献指南

请参考 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License

