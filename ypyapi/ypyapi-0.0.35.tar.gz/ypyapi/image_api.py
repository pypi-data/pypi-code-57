#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/5/13 0:20
# @Author : yangpingyan@gmail.com
from PIL import Image
from io import BytesIO


def image_compress_from_url(content, format):
    img = Image.open(BytesIO(content))
    image_buffer = BytesIO()
    img.save(image_buffer, format=format, optimize=True,quality=70)

    # image_buffer.getvalue()
    return image_buffer

if __name__ == '__main__':
    print("Mission start!")
    import oss2

    image_url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1590131254623&di=b054d4e65e3a2dbe4f4ae2d70da72cbe&imgtype=0&src=http%3A%2F%2Fa3.att.hudong.com%2F14%2F75%2F01300000164186121366756803686.jpg'
    image_buffer = image_compress_from_url(image_url)
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth_oss = oss2.Auth('LTAI4GKCdWtFaJw4smNFGBHe', '9dzDhv2UIOxyg8wzHvlZ09Cm0mZv1J')
    # auth_oss = oss2.Auth('LTAInD7pdwSHtTEx', 'To2pqcUO25fZcp6wwRxlb3VIqx9vtG')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket_oss = oss2.Bucket(auth_oss, 'http://oss-accelerate.aliyuncs.com', 'xinxindaipai')
    # bucket_oss = oss2.Bucket(auth_oss, 'http://oss-cn-hangzhou.aliyuncs.com', 'yiqizu-test')

    # with g_oss_lock:
    bucket_oss.put_object('mercari_img/test.jpg', image_buffer.getvalue())
    bucket_oss.put_object('mercari_img/test.png', image_buffer.getvalue())
    bucket_oss.get_object_to_file(f'mercari_img/test.jpg', rf'C:\Users\Administrator\Downloads\test.jpg')
    bucket_oss.get_object_to_file(f'mercari_img/test.png', rf'C:\Users\Administrator\Downloads\test.png')

    print("Mission complete!")

