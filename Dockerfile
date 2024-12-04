# 使用官方 Python 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到工作目录
COPY . /app

# 安装所需的 Python 包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 默认的端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 运行 Flask 应用
CMD ["flask", "run"]