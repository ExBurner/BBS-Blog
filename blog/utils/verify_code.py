import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO


def random_color():
    color = (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
    return color


def random_color2():
    color = (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
    return color


def random_char():
    random_num = str(random.randint(0, 9))
    random_low = chr(random.randint(97, 122))
    random_upper = chr(random.randint(65, 90))
    random_chars = random.choice([random_num, random_low, random_upper])
    return random_chars


def get_verify_code(request):
    """
    验证码
    """
    image = Image.new("RGB", (183, 40), (255, 255, 255))
    image_font = ImageFont.truetype("static/blog/font/Arial.ttf", 32)
    draw = ImageDraw.Draw(image)

    # 给每个坐标填充颜色,填充噪点
    for x in range(183):
        for y in range(40):
            draw.point((x, y), fill=random_color())

    verify_code_str = ""
    for i in range(5):
        random_chars = random_char()
        verify_code_str += random_chars
        draw.text((20+i*30, 0), random_chars, font=image_font, fill=random_color2())
    image = image.filter(ImageFilter.BLUR)  # 模糊处理
    # 放到磁盘中，但是速度比较慢，推荐放在内存中
    # with open("verify_code.png", "wb") as f:
    #     image.save(f)
    #
    # with open("verify_code.png", "rb") as f:
    #     data = f.read()
    request.session["verify_code_str"] = verify_code_str
    f = BytesIO()
    image.save(f, "png")
    data = f.getvalue()

    return data
