import synacell.cmodule


def test_1() -> (int, str):
    """
    Test creating net in the memory space of the snn.dll

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """
    snn = synacell.cmodule.Snn()

    print(f"Net count = {snn.net_count()}")
    snn.create_net()
    print(f"Net count = {snn.net_count()}")

    if snn.net_count() == 1:
        return 0, "Success"
    else:
        return 1, f"Net count is {snn.net_count()}"
