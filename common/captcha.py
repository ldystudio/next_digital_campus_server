import random
import string

from PIL import Image
from captcha.image import ImageCaptcha
from django.conf import settings


def generate_captcha():
    # 定义图片对象
    image = ImageCaptcha(fonts=[str(settings.BASE_DIR / 'static/fonts/actionj.ttf')])
    # 获取字符串
    captcha_text = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    # 生成图像
    captcha_image = Image.open(image.generate(captcha_text))
    # 存储图片
    return captcha_text, captcha_image
