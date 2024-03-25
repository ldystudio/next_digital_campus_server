FROM python:3.12.2-alpine

# 设置工作目录
WORKDIR /app

# 安装依赖
RUN pip install pysnowflake -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8910

# 运行 snowflake_start_server 命令
CMD ["snowflake_start_server", "--log_file_prefix=tmp/pysnowflake.log"]
