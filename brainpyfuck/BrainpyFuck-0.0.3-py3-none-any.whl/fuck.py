class BrainF():
    def __init__(self,code,*,print_memory=True, input_func=None, print_func=None):
        self.code=code
        self.memory=[0]
        self.MemoryIdx=0
        self.CodeIdx=0
        self.print_memory=print_memory
        if print_memory and not print_func:
            raise BrainF.InitializeError('a print function is expected.')
        self.print_func=print_func
        self.input_func=BrainF.input_in_ASCII if input_func is None else input_func

    #no self???
    def check(func):
        def wrap(self):
            rep=func(self)
            if self.MemoryIdx>=len(self.memory):
                self.memory.append(0)
            if self.MemoryIdx<0:
                raise MemoryError(f'index {self.MemoryIdx} is not valid')
            if not 0<=self.memory[self.MemoryIdx]<=255:#value out of range
                self.memory[self.MemoryIdx]=0
            return rep
        return wrap
    def move2Right(func):
        def wrap(self):
            rep=func(self)
            self.CodeIdx+=1
            return rep
        return wrap

    def run(self):
        while True:
            self.read()
            print(self.memory)
            if self.CodeIdx >= len(self.code):
                return
    def read(self,inp='\0'):
        now=self.code[self.CodeIdx]
        if now == '>':
            return self.greaterThan()
        elif now=='<':
            return self.lessThan()
        elif now=='+':
            return self.add()
        elif now=='-':
            return self.minus()
        elif now=='[':
            return self.loop()
        elif now==']':
            return self.close_loop()
        elif now==',':
            return self.input()
        elif now=='.':
            return self.output()
        else:
            return self.comment()

    @move2Right
    @check
    def greaterThan(self):
        self.MemoryIdx +=1

    @move2Right
    @check
    def lessThan(self):
        self.MemoryIdx -= 1

    @move2Right
    @check
    def add(self):
        self.memory[self.MemoryIdx] += 1

    @move2Right
    @check
    def minus(self):
        self.memory[self.MemoryIdx] -= 1

    @check
    def loop(self):
        if self.memory[self.MemoryIdx]:
            self.CodeIdx+=1
        else:
            self.CodeIdx=self.skipLoop()

    @check
    def close_loop(self):
        self.CodeIdx = self.backLoop()

    def skipLoop(self):
        now=1
        for i in range(self.CodeIdx+1,len(self.code)):
            if self.code[i]=='[':
                now += 1
            elif self.code[i] == ']':
                now -= 1
            if not now or i==len(self.code)-1:
                return i+1
    def backLoop(self):
        now=1
        for i in range(self.CodeIdx-1,-1,-1):
            if self.code[i]==']':
                now += 1
            elif self.code[i] == '[':
                now -= 1
            if not now:#'[' at code[0 or more]
                return i
            elif i==0: #'[' is not found
                raise MemoryError('] does not have a matching "["')

    @check
    def input(self):
        a=self.input_func()
        #print(a)
        if type(a)!=int or (a<0 or a>255):
            raise BrainF.InputError('input is invalid.')
        self.memory[self.MemoryIdx]=a
        self.CodeIdx += 1


    @check
    def output(self):
        self.CodeIdx += 1
        return self.memory[self.MemoryIdx]

    @move2Right
    def comment(self):
        pass
    def print(self):
        self.print_func(self.memory,self.MemoryIdx)

    def __iter__(self):
        self.memory=[0]
        self.MemoryIdx=0
        self.CodeIdx=0
        while self.CodeIdx < len(self.code):
            try:
                msg = self.read()
                if type(msg)==int:
                    msg=chr(msg)
                else:
                    msg=''
            except BrainF.InputError as string:
                print(string)
                continue
            yield msg
            if self.print_memory:
                self.print()
    @staticmethod
    def input_in_ASCII():
        return ord(input())



    class MemoryError(Exception):
        pass

    class InputError(Exception):
        pass
    class InitializeError(Exception):
        pass


def prettyprint(memory,pointer_idx):
    try:
        #raise ImportError('test installaion!!!')
        from colored import fg, bg, attr
    except:
        import subprocess, sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'colored'])
        from colored import fg, bg, attr
    print()
    for i in range(len(memory)):
        if i==pointer_idx:
            color=bg('red')
        else:
            color=""
        print(color+'[ '+str(memory[i])+' ]'+attr(0),end=' ')
    print()