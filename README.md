# next_digital_campus_server
Next数字校园后端

### 开启雪花算法生成服务器
```shell
# 前台开启
snowflake_start_server --log_file_prefix=tmp/pysnowflask.log

# 后台开启
nohup snowflake_start_server --log_file_prefix=tmp/pysnowflask.log>/dev/null &

# 可选参数
# --address：本机的IP地址默认localhost
# --port：端口号
# --dc：数据中心唯一标识符默认为0
# --worker：工作者唯一标识符默认为0
# --log_file_prefix：日志文件所在位置
```
