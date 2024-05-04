import random


def generate_floating_number():
    """生成带有正负号的随机百分比字符串"""
    return f"{random.choice(['+', '-'])}{(random.random() * 10):.1f}%"


def generate_random_data(length, start=80, end=130):
    """生成指定长度的随机数据"""
    return [random.randint(start, end) for _ in range(length)]


def generate_chart(
    title, describe, sub_describe, number_range, data_length, date_range=(80, 130)
):
    """生成图表字典"""
    chart = {
        "title": title,
        "describe": describe,
        "subDescribe": sub_describe,
        "number": random.randint(*number_range),
        "floating": generate_floating_number(),
        "data": generate_random_data(data_length, date_range[0], date_range[1]),
    }
    return chart
