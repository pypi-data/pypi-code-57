from weditor_assistant import *

print('手机截屏工具 (C)opyright by Pactera_Fintech')
print('    用法，python %s {ios|android} [ip|设备号]' % sys.argv[0])
print('    在当前目录生成 2 个文件：fullscreen.png、halfscreen.png')
print('    在halfscreen.png上使用鼠标抠图，自动生存在当前目录，回车退出')
def get_image(device = None,device_type = 'android'):
    if len(sys.argv) >= 2:
        device_type = sys.argv[1].lower()
    if len(sys.argv) >= 3:
        device = sys.argv[2].lower()

    # 手机截屏
    screen_shot(device_type, device)

    # 抠图
    crop()

get_image()