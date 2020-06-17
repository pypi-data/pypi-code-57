from gnsocket.gn_socket import GNCSocket
from gnsocket.conf.socket_conf import TEST_TEXT
import sys
import asyncio

from networktools.ssh import bridge, kill
from networktools.ports import used_ports, get_port

if __name__ == "__main__":
    mode = 'client'
    gs = GNCSocket(mode=mode)
    up=used_ports()
    (port, up)=get_port(up)
    host_port=6677
    host='10.54.217.15'
    user='geodesia'
    ssh_bridge=bridge(port, host_port, host, user)
    address=('localhost',port)
    print(address)
    gs.set_address(address)
    loop = asyncio.get_event_loop()
    gs.set_loop(loop)
    # gs.accept()
    msg = TEST_TEXT

    # Testing message generator
    print("Status " + gs.status)
    for m in gs.generate_msg(msg):
        print(m.decode('utf-8'))
    # gs.send_msg(msg)
    # print(gs.conn)
    # Testing communicate
    # gs.accept()
    # print(gs.conn)
    async def send_msg(loop):
        try:
            await asyncio.sleep(5)
            await gs.create_client()
        except Exception as x:
            print("Error al crear cliente: %s " %x)
            raise x
        while True:
            await asyncio.sleep(1)
            try:
                msg=''
                while not msg=='<END>':
                    msg=await gs.recv_msg()
                    if msg != '<END>' and msg is not None:
                        print(msg)
                    if msg == '<END>':
                        break

                this_msg = input("->")
                #
                if this_msg != "":
                    print("SEND :", this_msg)
                    await gs.send_msg(this_msg)
                    await gs.send_msg('<END>')

                    print("Ya enviado: " + this_msg)
                    if this_msg == "DONE":
                        print("Cerrando server")
            except KeyboardInterrupt as k:
                kill(ssh_bridge)
                if gs.writer.can_write_eof():
                    gs.writer.write_eof()
                print("Cerrando con kb")
                gs.close()
                sys.exit()
            except Exception as exec:
                print("Error en conexion a puerto mediante bridge")
                kill(ssh_bridge)
                raise exec
    #try:
    loop.run_until_complete(send_msg(loop))
    #except Exception as exec:
    #    print("Error %s " % exec)
    #    kill(ssh_bridge)
    loop.close()
    print("-" * 20)
    print("Apagando")
    print("Listo!")
