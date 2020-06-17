import asyncio

from gnc.client_manager import GNCManager, qread


class RemoteManager(GNCManager):
    def __init__(self,*args,**kwargs):
        super(RemoteManager,self).__init__(*args,**kwargs)
        self.name=kwargs['name']
        self.passw=kwargs['passw']
        self.q_n2t=kwargs['n2t']
        self.q_t2n=kwargs['t2n']

    async def recv_msg(self):
        """
        Receive msg from network and transform to terminal
        """
        reader=self.reader
        end=self.end
        msg = await qread(reader,end)
        #Transform msg to engine format
        pass

    async def send_msg(self, msg):
        """
        Receive msg from terminal and transform to network
        """
        writer=self.writer
        #read queue from engine

        #transform msg from engine to network server format
        pass
