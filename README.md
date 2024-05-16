# next_digital_campus_server
Next数字校园系统是一套基于现代化信息技术的全新型校园管理系统
## 特色

* 模块化设计：采用模块化设计，根据不同功能需求实现自定义开发和集成，保证了系统的高可扩展性和灵活性。
* 安全可靠：采用多重安全认证、加密传输等措施，确保数据安全和系统稳定。
* 互动便捷：支持移动设备访问，能够随时随地进行信息交流和共享，提升用户使用体验。
* 数据分析：集成了多种数据分析和挖掘工具，通过数据分析和挖掘，提供更全面的学校管理信息支持。
* 教育教学：采用针对性设计，兼顾教育教学特色，提供更符合教师和学生需求的管理和学习功能。
* 在线沟通：提供实时的在线聊天和讨论功能，可通过系统内部的消息系统进行交流和协作，方便快捷地解决问题和分享信息。
## 使用前沿技术

- [Python 3.12](https://www.python.org/)
- [Mysql 8](https://www.mysql.com/)
- [Redis](https://redis.io/)
- [Django 4.2.8](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)

## 开发

### 开启雪花算法生成服务器

```shell
# 前台开启
snowflake_start_server --log_file_prefix=snowflake/pysnowflask.log

# 后台开启
nohup snowflake_start_server --log_file_prefix=snowflake/pysnowflask.log>/dev/null &

# 可选参数
# --address：本机的IP地址默认localhost
# --port：端口号
# --dc：数据中心唯一标识符默认为0
# --worker：工作者唯一标识符默认为0
# --log_file_prefix：日志文件所在位置
```

### 如何使用

```powershell
git clone https://github.com/ldystudio/next_digital_campus_server.git

cd next_digital_campus_server

# 创建虚拟环境，需要python3.10以上
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 填写配置
mv .env.cfg.example .env.cfg
# 数据迁移
python manage.py makemigrations
python manage.py migrate

# 运行
python manage.py runserver 8000
```

## 部署

> 将uwsgi + daphne+ supervisor + nginx组件使用Docker部署

查看docker-compose.yaml文件中相关容器挂载的路径，提前创建好文件夹，将conf文件夹下的相关xxx.conf文件移动到对应地方，conf文件中某些字段如ip地址、密码之类的字段还需进行修改。

进入项目文件夹下输入``docker-compose up -d``一键部署！

