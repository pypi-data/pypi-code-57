import cv2
from pyprobar import bar
import matplotlib.pyplot as plt


def getFrame(filename, frameNum=10, W=(0, -1), H=(0, -1), gray=False):
    """ Get a specific frame in the video
    :param W: ROI W range
    :param H: ROI H range
    :return : (TotolFrameNum, fps, size), ROI
    """
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 获取视频尺寸
    TotolFrameNum = int(cap.get(7))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum)  # 设置要获取的帧号
    ret, frame = cap.read()
    if not gray:
        ROI = frame[H[0]:H[1], W[0]:W[1], :]
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ROI = frame[H[0]:H[1], W[0]:W[1]]

    cap.release()
    return (TotolFrameNum, fps, size), ROI


def resample(inputvideo,
             outputvideo,
             W=(0, -1),
             H=(0, -1),
             Time=None,
             samplerate=1,
             fps=None):
    """重采样，可指定视频对应采样率或fps、ROI(采样区域)、采样时长
    :param W: (宽度开始位置，宽度结束位置)
    :param H: (高度开始位置，高度结束位置)
    :param Time: 采样时长
    :param samplerate: 采样率，如设置0.1则表示对原视频每10帧采样一次
    :param fps: 如果设置了samplerate就不要再设置fps了, 它们二选一
    """
    cap = cv2.VideoCapture(inputvideo)
    FPS = cap.get(cv2.CAP_PROP_FPS)

    SIZE = [
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ]  # 获取视频尺寸

    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式

    TotolFrameNum = int(cap.get(7))  # == cv2.CV_CAP_PROP_FRAME_COUNT
    if Time is None:
        FrameNum = TotolFrameNum
    else:
        FrameNum = int(FPS * Time)
    print(f"原视频总帧：{TotolFrameNum}")
    if W == (0, -1):
        W = (0, int(SIZE[0]))
    else:
        SIZE[0] = W[1] - W[0]
    if H == (0, -1):
        H = (0, int(SIZE[1]))
    else:
        SIZE[1] = H[1] - H[0]

    step = round(1 / samplerate)
    if fps is None:
        fps = round(FPS * samplerate)
    else:
        step = round(FPS / fps)
    video = cv2.VideoWriter(outputvideo, fourcc, fps, tuple(SIZE))
    count = 0
    for idx in range(FrameNum):
        bar(idx, FrameNum)
        if idx % step != 0: continue
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)  # 为了均匀采样
        ret, frame = cap.read()
        ROI = frame[H[0]:H[1], W[0]:W[1], :]
        if not ret:
            break
        video.write(ROI)
        count += 1
    cap.release()
    print(f"总帧数：{count}")


def embedFrameInfo(inputvideo, outputvideo, fps=None):
    cap = cv2.VideoCapture(inputvideo)
    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS)

    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 获取视频尺寸

    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 编码格式

    video = cv2.VideoWriter(outputvideo, fourcc, fps, size)

    TotolFrameNum = int(cap.get(7))  # == cv2.CV_CAP_PROP_FRAME_COUNT
    for idx in range(TotolFrameNum):
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, f'current frame: {idx}', (50, 60),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2, 1)
        cv2.putText(frame, f'time: {idx/ fps:.2f} S', (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 255, 0), 2, 1)
        video.write(frame)
        bar(idx, TotolFrameNum)
        # cv2.imshow("zd1", frame)
        # if cv2.waitKey(int(10/fps)) & 0xFF == ord('q'): # 0xFF的使用：https://blog.csdn.net/i6223671/article/details/88924481
        #     # 实际上 任何一个整数与0xff做与运算，将会取得这个数最后八位
        #     break

    cap.release()
    # if show:
    #     cv2.destroyAllWindows()
