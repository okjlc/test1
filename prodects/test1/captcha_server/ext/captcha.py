# -*- coding: utf-8 -*-
import os
import random
import base64
import StringIO
from PIL import Image, ImageDraw, ImageFilter, ImageFont


file_path = os.path.abspath(os.path.dirname(__file__))


class Captcha(object):
    size = (120, 30)
    mode = 'RGB'
    bg_color = (255, 255, 255)
    fg_color = (0, 0, 255)
    font_size = 18
    font_type = "Font/arial.ttf"
    length = 4
    n_line = (1, 2)
    point_chance = 2
    letters = "abcdefhjkmnpqrstuvwxy"
    uppers = letters.upper()
    numbers = ''.join(map(str, range(3, 10)))
    init_chars = ''.join((letters, uppers, numbers))
    chars = init_chars
    width, height = size

    def __init__(self):
        self.img = Image.new(self.mode, self.size, self.bg_color)
        self.draw = ImageDraw.Draw(self.img)

    def create(self, chars=None, draw_lines=True):
        """
        生成验证码
        chars 默认是None, 验证码生成随机字符串。
        如果赋值 chars, 验证码将生成指定字符。

        """
        if draw_lines:
            self.get_lines()
        if draw_lines:
            self.get_points()
        if chars is not None and len(chars) == 4:
            try:
                chars = str(chars)
            except:
                raise TypeError('chars is must string and len is 4!')
        else:
            chars = self.get_character()
        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500,
                  ]
        img = self.img.transform(self.size, Image.PERSPECTIVE, params)
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)

        mstream = StringIO.StringIO()
        img.save(mstream, "PNG")
        image = mstream.getvalue()
        b = base64.b64encode(image)
        return img, b, chars

    def get_lines(self):
        """
        绘制干扰线
        """
        line_num = random.randint(*self.n_line)

        for i in range(line_num):
            begin = (random.randint(0, self.size[0]),
                     random.randint(0, self.size[1]))
            end = (random.randint(0, self.size[0]),
                   random.randint(0, self.size[1]))
            self.draw.line([begin, end], fill=(0, 0, 0))

    def get_points(self):
        """
        绘制干扰点
        """
        chance = min(100, max(0, int(self.point_chance)))

        for w in xrange(self.width):
            for h in xrange(self.height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    self.draw.point((w, h), fill=(0, 0, 0))

    def get_character(self):
        """
        绘制验证码字符
        """
        c_chars = random.sample(self.chars, self.length)
        chars = '%s' % ' '.join(c_chars)
        font = ImageFont.truetype(file_path + "/" + self.font_type,
                                  self.font_size)
        font_width, font_height = font.getsize(chars)

        self.draw.text(((self.width - font_width) / 3,
                        (self.height - font_height) / 3),
                       chars, font=font, fill=self.fg_color)
        return chars


def create_captcha(chars=None):
    return Captcha().create(chars)
