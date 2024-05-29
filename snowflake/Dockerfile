FROM python:3.12.2-alpine

# 设置环境变量
# 防止Python生成.pyc文件
ENV PYTHONDONTWRITEBYTECODE 1
# 输出运行信息到终端
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add --update tzdata

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone

# 安装依赖
RUN pip install pysnowflake -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN touch /app/pysnowflask.log

# 运行 snowflake_start_server 命令
CMD ["snowflake_start_server", "--address=0.0.0.0", "--log_file_prefix=/app/pysnowflake.log"]