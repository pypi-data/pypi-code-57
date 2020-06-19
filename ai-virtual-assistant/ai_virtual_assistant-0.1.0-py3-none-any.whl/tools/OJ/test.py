# import socket
# serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serv.bind(('127.0.0.1', 8080))
# serv.listen(5)
# while True:
#     conn, addr = serv.accept()
#     from_client = ''
#     while True:
#         data = conn.recv(4096)
#         if not data: break
#         from_client += data.decode('utf-8')
#         print (from_client)
#         conn.send("I am SERVER<br>")
#     conn.close()
#     print ('client disconnected')


s = 'failed'

print(f'I am {s}')

# import socket
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(('0.0.0.0', 8082))
# client.send("I am CLIENT<br>")
# from_server = client.recv(4096)
# client.close()
# print (from_server.decode('utf-8'))