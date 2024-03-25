FROM python:3.12.2-alpine

LABEL maintainer="Ldy <1187551003@qq.com>"

# 设置环境变量
# 防止Python生成.pyc文件
ENV PYTHONDONTWRITEBYTECODE 1
# 输出运行信息到终端
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /code

# 安装依赖
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install uwsgi -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制项目代码到工作目录
COPY . /code/