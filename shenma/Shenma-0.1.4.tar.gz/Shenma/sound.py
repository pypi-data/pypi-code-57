import wave
from pyaudio import PyAudio, paInt16
import matplotlib.pyplot as plt
import numpy as np
 
 
CHUNK = 1024 # wav文件是由若干个CHUNK组成的，CHUNK我们就理解成数据包或者数据片段。
FORMAT = paInt16 # 表示我们使用量化位数 16位来进行录音
CHANNELS = 2 #代表的是声道，1是单声道，2是双声道。
RATE = 16000 # 采样率 一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz,
                # 11.025kHz, 22.05kHz, 44.1kHz。
# RECORD_SECONDS = 5 # 录制时间这里设定了5秒
 
 
def save_wave_file(pa, filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    # wf.setsampwidth(sampwidth)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(data))
    wf.close()
 
 
def get_audio(filepath, RECORD_SECONDS):
	# filepath：保存路径及名称
	# RECORD_SECONDS：录制时长
    isstart = str(input("是否开始录音？ （是/否）")) #输出提示文本，input接收一个值,转为str，赋值给aa
    if isstart == str("是"):
        pa = PyAudio()
        stream = pa.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)
        print("*" * 10, "开始录音：请在{}秒内输入语音".format(RECORD_SECONDS))
        frames = []  # 定义一个列表
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  # 循环，采样率 44100 / 1024 * 5
            data = stream.read(CHUNK)  # 读取chunk个字节 保存到data中
            frames.append(data)  # 向列表frames中添加数据data
        #print(frames)
        print("*" * 10, "录音结束\n")
 
        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结
 
        save_wave_file(pa, filepath, frames)
    elif isstart == str("否"):
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(filepath)
 
 
def wav_time(filepath):
	# 音频时长计数器
	time_count = 0
	# 统计音频的时长
	with wave.open(filepath,'rb') as f:
            f = wave.open(filepath)
            time_count += f.getparams().nframes/f.getparams().framerate
	# 统计音频的时长
	print('该音频的时长为{}秒'.format(round(time_count)))

 
def play(filepath):
	print('开始播放')
	wav_time(filepath)
	wf = wave.open(filepath, 'rb')
	p = PyAudio()
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=
	wf.getnchannels(), rate=wf.getframerate(), output=True)

	# 读数据
	data = wf.readframes(CHUNK)

	# 播放流
	while len(data) > 0:
		stream.write(data)
		data = wf.readframes(CHUNK)

	stream.stop_stream() # 暂停播放/录制
	stream.close() # 终止播放

	p.terminate() # 终止portaudio会话
	wf.close()
	print('播放结束')
	
	
def sound_draw(filename):
	# 打开WAV文档
	#首先载入Python的标准处理WAV文件的模块，然后调用wave.open打开wav文件，注意需要使用"rb"(二进制模式)打开文件：
	f = wave.open(filename, "rb")
	#open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据：

	# 读取格式信息
	# (nchannels, sampwidth, framerate, nframes, comptype, compname)

	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]

	#getparams：一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采样频率,
	#采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息：
	#getnchannels, getsampwidth, getframerate, getnframes等方法可以单独返回WAV文件的特定的信息。

	# 读取波形数据
	str_data = f.readframes(nframes)
	#readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据（一大堆
	#bytes)，在Python中用字符串表示二进制数据：
	f.close()

	#将波形数据转换为数组
	#接下来需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组：
	wave_data = np.fromstring(str_data, dtype=np.short)
	#通过fromstring函数将字符串转换为数组，通过其参数dtype指定转换后的数据格式，由于我们的声音格式是以两个字节表示一个取
	#样值，因此采用short数据类型转换。现在我们得到的wave_data是一个一维的short类型的数组，但是因为我们的声音文件是双声
	#道的，因此它由左右两个声道的取样交替构成：LRLRLRLR....LR（L表示左声道的取样值，R表示右声道取样值）。修改wave_data
	#的sharp之后：
	wave_data.shape = -1, 2
	#将其转置得到：
	wave_data = wave_data.T
	#最后通过取样点数和取样频率计算出每个取样的时间：
	time = np.arange(0, nframes) * (1.0 / framerate)

	# 绘制波形
	plt.subplot(211) 
	plt.plot(time, wave_data[0])
	plt.subplot(212) 
	plt.plot(time, wave_data[1], c="g")
	plt.xlabel("time (seconds)")
	plt.show()