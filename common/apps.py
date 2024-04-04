import snowflake.client
from django.apps import AppConfig
from requests.exceptions import ConnectionError

from server.local_settings import DATABASES


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"

    def ready(self):
        try:
            snowflake.client.setup(
                DATABASES.get("default").get("HOST") or "localhost", 8910
            )
            snowflake_stats = snowflake.client.get_stats()
            print(f'本机雪花算法workerID：{snowflake_stats["worker"]}')
        except ConnectionError:
            raise ConnectionError("连接不到生成雪花算法服务器，请检查服务器是否启动，命令详见README")
