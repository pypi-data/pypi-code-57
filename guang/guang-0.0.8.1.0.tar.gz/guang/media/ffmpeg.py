import os
import cv2


def resample_fps(inputname, fps, outname):
    """保持视频总时长不变，控制fps"""
    os.system(f"ffmpeg -i {inputname} -r {fps} {outname}")


def av_speed(inputvideo, outvideo, speed=None, cut_frame=True):
    """改变原视频播放速率为原来的speed倍。这将改变原视频时长。(both video and audio)
    :param inputvideo: 输入video文件名
    :param speed: 以删除帧的方式实现对 原视频的speed倍数(更快速度)
    :param cut_frame: 以更改fps实现对原视频的speed倍数播放(更高质量)，fps=60封顶

    """
    cap = cv2.VideoCapture(inputvideo)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    fps = FPS if cut_frame is True else FPS * speed
    fps = min(60, fps)
    os.system(
        f"""ffmpeg -i {inputvideo} -r {fps} -filter_complex "[0:v]setpts={1/speed}*PTS[v];[0:a]atempo={speed}[a]" -map "[v]" -map "[a]" {outvideo}"""
    )


def video_speed(inputvideo, outvideo, speed, cut_frame=True):
    """仅仅改变了video播放速率的视频，其音频速率保持不变，播放时长超过音频时长后部分为静音。
    :param: speed : Play at `speed` times the speed of the input file

    """
    cap = cv2.VideoCapture(inputvideo)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    fps = FPS if cut_frame is True else FPS * speed

    os.system(
        f"""ffmpeg -i {inputvideo} -r {fps} -filter:v "setpts={1/speed}*PTS" {outvideo}"""
    )


def audio_speed(inputname, outname, speed):
    """仅仅改变音频速度
    :param speed : Play at `speed` times the speed of the input file
    """
    os.system(
        f"""ffmpeg -i {inputname} -filter:a "atempo={speed}" {outname}""")
