import os
currPath = os.path.dirname(os.path.abspath(__file__))


def menu(target=None, saveas=None, returnStr=False):
    """
    menu() to display all options
    3 parameters - target and saveAs
    target - use it if you already know the option
    saveAs - if u want to save the code somewhere, specify file name
    returnStr - if saveAs is false and returnStr is true, u can guess what it does
    """
    stuff = dict(enumerate([file for file in os.listdir(os.path.join(currPath, "h2comp")) if file.endswith(".py")], 1))
    if target is None:
        print("what do u want?")
        for k, v in stuff.items():
            print(f"{k}:{v}")
        target = ""
        while target not in stuff.keys():
            target = int(input("enter a valid key: "))
        
    with open(currPath + f"/h2comp/{stuff[target]}") as f:
        if saveas is None:
            if returnStr:
                return f.read()
            else:
                print(f.read())
        else:
            with open(saveas, "w") as f2:
                f2.write(f.read())


if __name__ == "__main__":
    menu()
    print(os.listdir(os.path.join(currPath, "h2comp")))