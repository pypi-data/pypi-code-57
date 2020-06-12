#_*_ coding:UTF-8 _*_

# 导入包
import labplusAI.lib.snowboydecoder as snowboydecoder
import sys
import signal
import os.path
import threading
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

'''
class Voice_wake_up():
	"""docstring for ClassName"""
	def __init__(self,model,fun,sensitivity):
		global interrupted 
		interrupted = False
		self.model = model
		self.fun = fun
		self.sensitivity = sensitivity

	def signal_handler(self ,signal, frame):
		global interrupted
		interrupted = True


	def interrupt_callback(self):
		global interrupted
		return interrupted

	#  回调函数，在这里实现
	def callbacks(self):
		global detector

    	# 语音唤醒后，提示ding两声
		snowboydecoder.play_audio_file()
		snowboydecoder.play_audio_file()

    	#  关闭snowboy功能
		detector.terminate()
    	#  开启语音识别
    	#recordMonitor.monitor()
		self.fun()
		#print('检测到热词')
    	# 打开snowboy功能
		self.wake_up()    # wake_up —> fun —> wake_up  递归调用

	# 热词唤醒    
	def wake_up(self):
		global detector
		model = self.model  #  唤醒词为 SnowBoy
    	# capture SIGINT signal, e.g., Ctrl+C
		signal.signal(signal.SIGINT, self.signal_handler)

    	# 唤醒词检测函数，调整sensitivity参数可修改唤醒词检测的准确性
		detector = snowboydecoder.HotwordDetector(model, sensitivity=self.sensitivity)
		print('Listening... please say wake-up word:SnowBoy')
		print('监听中... 请说唤醒词')
    	# main loop
    	# 回调函数 detected_callback=snowboydecoder.play_audio_file 
    	# 修改回调函数可实现我们想要的功能
		detector.start(detected_callback=self.callbacks,      # 自定义回调函数
                   	   interrupt_check=self.interrupt_callback,
                       sleep_time=0.03)
    	# 释放资源
		detector.terminate()


Voice_wake_up(model模型,fun回调函数,sensitivity)
model，语音模型
fun，自定义回调函数
sensitivity，识别敏感度
'''

class voiceup():
    def __init__(self):
        global interrupted
        interrupted = False
        self.ATTENTION = '冲锋舟'
        self.AHEAD = '向前'
        self.BACK = '向后'
        self.LEFT = '向左'
        self.RIGHT = '向右'
        self.STOP = '停止'
        global command_cfz
        global command_ahead
        global command_back
        global command_left
        global command_right
        global command_stop
        command_cfz = self.default_behavior
        command_ahead = self.default_behavior
        command_back = self.default_behavior
        command_left = self.default_behavior
        command_right = self.default_behavior
        command_stop = self.default_behavior
        self.models = None
        self.sensitivity = None
        self.listen_thread = None

    def signal_handler(self,signal, frame):
        global interrupted
        interrupted = True


    def interrupt_callback(self):
        global interrupted
        return interrupted

    def listening(self):
        detector = snowboydecoder.HotwordDetector(self.models, sensitivity=self.sensitivity)
        callbacks = [lambda: command_ahead(),
                    lambda: command_back(),
                    lambda: command_left(),
                    lambda: command_right(),
                    lambda: command_stop(),
                    lambda: command_cfz()]
        '''
        callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING),
                     lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DONG)]
        
        callbacks = [lambda: command_ahead(),
                    lambda: command_back(),
                    lambda: command_left(),
                    lambda: command_right(),
                    lambda: command_stop(),
                    lambda: command_cfz()]
        '''
        print('Listening... Press Ctrl+C to exit')
        # main loop  
        # make sure you have the same numbers of callbacks and models
        detector.start(detected_callback=callbacks,
                    interrupt_check=self.interrupt_callback, 
                    sleep_time=0.03)
        detector.terminate()
        
    def stop(self):
        if self.listen_thread is not None:
            print("Stopping...");
            stop_thread(self.listen_thread)
        
    def run(self):
        _path = os.path.abspath(os.path.dirname(__file__))
        self.models = [_path + '/resources/models/ahead.pmdl'
                  , _path + '/resources/models/back.pmdl'
                  ,_path + '/resources/models/left.pmdl'
                  , _path + '/resources/models/right.pmdl'
                  ,_path + '/resources/models/stop.pmdl'
                  , _path + '/resources/models/cfz.pmdl']
        #models = sys.argv[1:]
        #print(models)
        # capture SIGINT signal, e.g., Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

        self.sensitivity = [0.45]*len(self.models)
        #print(sensitivity)
        
        self.listen_thread = threading.Thread(target=self.listening)
        self.listen_thread.setDaemon(False)
        self.listen_thread.start()
        
    
    def command(self,command,fun):
        def c_ahead(f):
            global command_ahead
            command_ahead = f
        
        def c_back(f):
            global command_back
            command_back = f
        
        def c_left(f):
            global command_left
            command_left = f

        def c_right(f):
            global command_right
            command_right = f
        
        def c_stop(f):
            global command_stop
            command_stop = f
        
        def c_cfz(f):
            global command_cfz
            command_cfz = f

        command_switch = {
            '向前':c_ahead,
            '向后':c_back,
            '向左':c_left,
            '向右':c_right,
            '停止':c_stop,
            '冲锋舟':c_cfz,
        }
        #print(command)
        #print(command_switch.get(command))
        command_switch.get(command)(fun)

    
    def default_behavior(self):
        print('未定义行为！')


'''
def go_ahead():
    print('向前')

def go_back():
    print('向后')

def turn_left():
    print('向左')

def turn_right():
    print('向右')

def full_stop():
    print('立停！')

def yes_sir():
    print('冲锋舟！！！')


listener = voiceup()

listener.command(listener.AHEAD,go_ahead)
listener.command(listener.BACK,go_back)
listener.command(listener.RIGHT,turn_right)
listener.command(listener.LEFT,turn_left)
listener.command(listener.STOP,full_stop)
listener.command(listener.ATTENTION, yes_sir)

listener.run()
'''
