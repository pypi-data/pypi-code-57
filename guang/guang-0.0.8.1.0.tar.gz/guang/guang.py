import fire
import os
from guang.Utils.toolsFunc import path
from guang.cv.video import resample, embedFrameInfo
from guang.media.ffmpeg import *


def mie():
    origin_wd = os.getcwd()
    os.chdir(r"C:\Users\beidongjiedeguang\OneDrive\a_github\ScatteringLight")
    os.system("streamlit run app.py")
    os.chdir(origin_wd)


def lorenz():
    app_path = path(
        os.path.join(os.path.dirname(__file__), "app/compose/anim_demo.py"))
    os.system(f"streamlit run {app_path}")


def sawtooth():
    file_path = path(
        os.path.join(os.path.dirname(__file__), "app/compose/slider.py"))
    os.system(f"python {file_path}")


def geo():
    file_path = path(os.path.join(os.path.dirname(__file__), "geo/compose.py"))
    os.system(f"python {file_path}")


def fourier():
    app_path = os.path.join(os.path.dirname(__file__), "sci/fourier_app.py")
    os.system(f"streamlit run {app_path}")


def multi_cvt2wav(PATH1, PATH2, FORMAT='*', sr=16000, n_cpu=None):
    """
    :arg PATH1: Input folder path
    :arg PATH2: Output folder path
    :arg FORMAT: Input voice format,  default all files
    :arg sr: Sample rate, default:16000
    :arg n_cpu: Number of multiple processes
    """
    from guang.Voice.convert import multi_cvt2wav as cvt
    cvt(PATH1, PATH2, FORMAT, sr, n_cpu)


def upload(PAHT1="upload/", PATH2="/var/www/html/"):
    from syncnote import Cloud

    def download(
        remote_path: str,
        local_path: str,
        config_path:
        str = r"C:\Users\beidongjiedeguang\OneDrive\a_github\myWebsite\config.yaml"
    ):
        cloud = Cloud(config_path)
        cloud.remote_walk(remote_path)
        cloud.local_walk(local_path)
        cloud.download()

    def upload(
        local_path: str,
        remote_path: str,
        config_path:
        str = r"C:\Users\beidongjiedeguang\OneDrive\a_github\myWebsite\config.yaml"
    ):
        cloud = Cloud(config_path)
        cloud.remote_walk(remote_path)
        cloud.local_walk(local_path)
        cloud.upload()

    upload(PAHT1, PATH2)


func_list = [
    mie, lorenz, geo, sawtooth, multi_cvt2wav, fourier, embedFrameInfo,
    resample, resample_fps, av_speed, video_speed, audio_speed
]

func_dict = {}
for i in func_list:
    func_dict[i.__name__] = i


def main():
    fire.Fire(func_dict)


if __name__ == "__main__":
    main()
