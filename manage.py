#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import snowflake.client
from requests.exceptions import ConnectionError


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        snowflake_stats = snowflake.client.get_stats()
        print(f'本机雪花算法workerID：{snowflake_stats["worker"]}')
    except ConnectionError:
        raise ConnectionError('连接不到生成雪花算法服务器，请检查服务器是否启动，命令详见README')

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
