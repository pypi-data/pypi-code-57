class statusRecorder:
    def __init__(self):
        pass

    def record2txt(self, fileName, content):
        with open(fileName, "w") as f:
            f.write(content)
