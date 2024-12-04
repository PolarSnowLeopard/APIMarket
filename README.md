# APIMarket

APIMarket是一个模拟API服务平台，主要用于为微服务推荐与基于LLM Agent工具调用的服务组合项目提供测试支持。

## 项目简介

本项目主要提供模拟API服务，用于：
- 用户信息查询和管理
- 基于OpenAI的教育经历描述生成
- 基于OpenAI的生活状态分析
- 邮件发送服务模拟
- 天气信息查询模拟
- 数学计算服务模拟

## 技术栈

- 后端：Python 3.9
- Web框架：Flask + Flask-RESTX
- API文档：Swagger/OpenAPI
- AI模型：OpenAI GPT-3.5

## 安装说明

1. 克隆项目

```bash
git clone https://github.com/PolarSnowLeopard/APIMarket.git
cd APIMarket
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建 `.env` 文件并配置以下变量：

```
OPENAI_API_KEY=your_openai_api_key
```

## 使用方法

1. 启动服务

```bash
python app.py
```

2. 访问API文档

```
http://localhost:5000/
```

## 项目结构

```
APIMarket/
├── app.py              # 主程序入口和API路由定义
├── tools.py           # 工具函数实现
├── mock_data.py       # 模拟数据定义
├── requirements.txt   # 项目依赖
├── .env              # 环境变量配置
└── Dockerfile        # Docker配置文件
```

## 可用的API接口

1. 用户相关：
   - `/api/get_user_id` - 根据昵称获取用户ID
   - `/api/get_user_info` - 根据用户ID获取用户信息

2. AI生成服务：
   - `/api/generate_education_description` - 生成院校与专业介绍
   - `/api/summarize_recent_life_status` - 总结用户近期生活状态

3. 功能服务：
   - `/api/send_email` - 发送邮件服务
   - `/api/get_weather` - 获取天气信息
   - `/api/calculate` - 数学计算服务

## Docker部署

1. 构建镜像

```bash
docker build -t apimarket .
```

2. 运行容器

```bash
sudo docker run -d \
--name APIMarket \
-p 5000:5000 \
--restart unless-stopped \
-v $(pwd)/.env:/app/.env \
api-market
```

## 如何添加新的模拟API

### 1. 在mock_data.py中添加模拟数据

```python
# mock_data.py

# 添加新的模拟数据
NEW_SERVICE_DATA = {
    "key1": {
        "field1": "value1",
        "field2": "value2"
    }
}
```

### 2. 在app.py中添加新的路由

```python
from flask import Flask, jsonify
from flask_restx import Api, Resource, fields

# 定义API模型
new_service_model = api.model('NewService', {
    'field1': fields.String(description='字段1的描述'),
    'field2': fields.String(description='字段2的描述')
})

# 添加新的路由
@ns.route('/new_service')
class NewService(Resource):
    @ns.expect(new_service_model)
    @ns.doc(description='新服务的描述')
    def post(self):
        try:
            data = request.json
            # 处理请求
            return jsonify({"result": "处理结果"})
        except Exception as e:
            api.abort(500, str(e))
```

### 3. 如果需要，在tools.py中添加辅助函数

```python
def process_new_service_data(data):
    """处理新服务的数据

    参数:
        data (dict): 输入数据

    返回:
        dict: 处理后的数据
    """
    # 处理逻辑
    return processed_data
```

### 最佳实践

1. 数据组织：
   - 在 `mock_data.py` 中使用常量定义模拟数据
   - 保持数据结构的一致性和可维护性

2. API设计：
   - 使用 Flask-RESTX 的装饰器添加完整的API文档
   - 实现适当的错误处理和异常捕获
   - 使用 Pydantic 模型进行数据验证
   - 返回统一的JSON响应格式

3. 代码质量：
   - 添加适当的注释和文档字符串
   - 遵循Python代码风格规范
   - 实现错误处理和日志记录

## 许可证

本项目采用 MIT 许可证

