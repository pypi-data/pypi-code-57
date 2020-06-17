import multiprocessing
import time
import asyncio


class multiProcess(multiprocessing.Process):
    def __init__(self, num):
        multiprocessing.Process.__init__(self)
        self.count = 0
        self.num = num

    def run(self) -> None:
        print("进程%s" % self.num)
        loop = asyncio.get_event_loop()
        coros = []
        for i in range(100):
            a = multiRoutine(i)
            coros.append(a.doLogic(i))
        loop.run_until_complete(asyncio.gather(*coros))


class multiRoutine():
    def __init__(self, num):
        self.count = 0
        self.num = num

    def logic(self):
        print("协程%s" % self.num)

    async def doLogic(self, num):
        self.logic()


class main:
    def newProcess(self):
        for i in range(4):
            process = multiProcess(i)
            process.start()
            process.join()


if __name__ == "__main__":
    a = main()
    a.newProcess()
