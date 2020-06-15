from aip import AipSpeech

# 创建SpeechClient
def SpeechClient(APP_ID, API_KEY, SECRET_KEY):
	client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
	return client


# 读取wav文件
def read_wav(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()