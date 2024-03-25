FROM python:3.12.2-alpine

# 设置环境变量
# 防止Python生成.pyc文件
ENV PYTHONDONTWRITEBYTECODE 1
# 输出运行信息到终端
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip install pysnowflake -i https://pypi.tuna.tsinghua.edu.cn/simple

ADD pysnowflask.log /app

# 运行 snowflake_start_server 命令
CMD ["snowflake_start_server", "--log_file_prefix=/app/pysnowflake.log"]