# from datetime import datetime
# from snowflake import SnowflakeGenerator
# import pytz
# snowflake_generator = SnowflakeGenerator(instance=0, epoch=0)
# for i in range(10):
#     print(next(snowflake_generator), len(str(next(snowflake_generator))))
# print(round(datetime.now(pytz.timezone('Asia/Shanghai')).timestamp()*1000))

# import datetime
#
# # 指定时间
# specified_time = datetime.datetime.now()
#
# # Epoch开始时间点（参考值）
# epoch_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
#
# # 计算时间差并换算成毫秒
# delta_time = specified_time - epoch_time
# timestamp_ms = delta_time.total_seconds() * 1000
#
# # 输出时间戳
# print(int(timestamp_ms),len(str(int(timestamp_ms))))
