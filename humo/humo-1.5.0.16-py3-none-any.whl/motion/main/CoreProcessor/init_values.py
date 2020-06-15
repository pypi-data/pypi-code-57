class Values:
    def __init__(self,data,**kwargs):
        self._ID = data["ID"]
        # each data
        self._device = data["device"][0]
        self._model = data["model"][0]
        self._marker = data["marker"][0]
        # header data
        self._deviceheader = [i.lower() for i in data["device"][1]]
        self._modelheader = [i.lower() for i in data["model"][1]]
        self._mkheader = [i.lower() for i in data["marker"][1]]
        self.deviceheader = data["device"][1]
        self.modelheader = data["model"][1]
        self.mkheader = data["marker"][1]
        # spep
        self._spep = data["spep"]
        if "cfg" in kwargs.keys():
            self.cfg = kwargs["cfg"]
        else:
            self.cfg = None
        # EMG name
        self._emg_name = data["EMG_name"]
        self._mvc = data["MMT"]
        self._MMTraw = data["rawMMT"]