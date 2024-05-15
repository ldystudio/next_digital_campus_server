FROM python:3.12.2-alpine

LABEL maintainer="Ldy <1187551003@qq.com>"

# 设置环境变量
# 防止Python生成.pyc文件
ENV PYTHONDONTWRITEBYTECODE 1
# 输出运行信息到终端
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE server.settings
# 设置工作目录
WORKDIR /code

# 修改Alpine的镜像源并安装mysqlclient和uwsgi的依赖
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add --update gcc python3-dev mysql-dev musl-dev tzdata \
    && apk add --no-cache linux-headers

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo "Asia/Shanghai" > /etc/timezone

# 安装依赖
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install uwsgi supervisor

# 复制项目代码到工作目录
COPY . /code/
