import synacell.cmodule


def test_1() -> (int, str):
    """
    Test creating net in the memory space of snn.dll.
    net1 is deleted throuh the api, net2 is deleted throgh Net method and on net3
    destructor is called when this function exits. The destructor call on net3
    can be seen in the log file.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    api = synacell.cmodule.SnnAPI
    net1 = api.new_net()
    net2 = api.new_net()
    net3 = api.new_net()
    api.delete_net(net1)
    net2.delete()

    if net1.ptr is None and net2.ptr is None:
        return 0, "Success"
    else:
        return 1, f"Net id not deleted"


def test_2() -> (int, str):
    """
    Test creating net wit parts in snn.dll. Changing part parameters

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData")
    params = net.get_params(0)
    if params != 'id=0,type=CellData,file=,pos=0,dataSize=0,sampleRate=0':
        return 1, "Add part params error"
    net.set_params(0, "pos=120")
    params = net.get_params(0)
    if params != 'id=0,type=CellData,file=,pos=120,dataSize=0,sampleRate=0':
        return 2, "Set params error"
    return 0, "Success"


def test_3() -> (int, str):
    """
    Run net on wav data. Gather output.

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=../data/audio/happy/0227998e_nohash_1.wav")
    params = net.get_params(0)
    if params != ("id=0,type=CellData,file=../data/audio/happy/0227998e_nohash_1.wav," +
                  "pos=0,dataSize=14118,sampleRate=16000"):
        return 1, "Add part params error"
    net.set_recorder(0, "id=0,value=vo,beg=0,size=1000")
    net.reset()
    net.run(14118, 1.0/16000.0)
    record = net.get_record(0)
    if record.size() == 1000:
        return 0, "Success"
    else:
        return 1, "Record data loading error"


def run_all():
    test_li = [test_1, test_2, test_3]

    for i in range(len(test_li)):
        val, msg = test_li[i]()
        if val == 0:
            print(f"Test {i} passed")
        else:
            print(f"Test {i} failed with error message: {msg}")
        print(f"Log:\n{synacell.cmodule.SnnAPI.get_log()}")
        synacell.cmodule.SnnAPI.clear_log()


if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    run_all()
