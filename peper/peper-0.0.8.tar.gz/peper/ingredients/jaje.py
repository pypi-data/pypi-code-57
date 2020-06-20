from peper.bucket import add

class Jaje:
    @staticmethod
    def komad():
        return Jaje.komada(1)

    @staticmethod
    def komada(x):
        add("jaje", x)
        return "jaje" if x == 1 else f"{x} jajeta"