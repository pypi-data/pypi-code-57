import socket
sock = None
AF_TYPE = socket.AF_INET
SOCK_TYPE = socket.SOCK_STREAM
gnc_path = '/tmp/gnc.socket'
host=socket.gethostbyname(socket.gethostname())
port=6677
address=(host,port)
n_listen=5
t_out = 15
#bufsize: standar: 128
buffsize = 64
# msg_limit = 512
HEADER = "MSG"
ENDER = "END"
uin = 6
char_code = "utf-8"
TEST_TEXT = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus interdum suscipit mi, viverra volutpat augue elementum eget. Vivamus et ligula in nisl tincidunt vestibulum. Nullam non bibendum libero, nec vulputate enim. Cras vulputate enim vitae purus porttitor, pharetra faucibus ipsum pulvinar. In id facilisis lacus, vitae vestibulum justo. Ut a porttitor sem, eu auctor mi. Proin erat lacus, tempus tincidunt mi et, ultricies consequat turpis. Fusce fringilla feugiat nunc, in ullamcorper tellus tincidunt et. Integer pretium mauris lorem, ac vulputate sem luctus quis. Maecenas vitae sapien sit amet dolor auctor molestie eu non eros.\
In iaculis ligula sagittis, tincidunt massa quis, commodo sapien. Fusce nibh tellus, varius laoreet rhoncus sit amet, sodales at nisl. Nulla eros sapien, laoreet quis accumsan quis, volutpat id orci. Aenean non mollis magna. Aliquam blandit, felis ac hendrerit blandit, mi justo convallis nulla, non mattis neque ipsum vitae ligula. Sed dapibus eleifend tellus, non rutrum risus cursus eget. Morbi cursus molestie iaculis. Phasellus blandit facilisis sollicitudin. Suspendisse porttitor, quam ac gravida luctus, diam nunc condimentum odio, in consequat justo lacus in magna. Ut ultrices, quam a aliquet lacinia, nibh purus pretium felis, quis malesuada est elit in dui. Cras sed felis ultricies, interdum risus eu, pretium turpis. Praesent aliquet placerat orci eu sollicitudin. Maecenas convallis euismod magna, et consequat enim porttitor et. Integer bibendum velit in suscipit placerat. Aliquam dui nunc, porta sit amet convallis sit amet, finibus vel orci.\
Vivamus suscipit urna vitae mi molestie aliquet. Duis porta eu mi nec dignissim. Mauris mi velit, accumsan vitae ipsum vel, posuere faucibus dolor. Curabitur interdum elit ac malesuada porttitor. Curabitur semper risus sed magna vestibulum egestas. Duis in velit volutpat, iaculis mi semper, dapibus risus. Vivamus dui augue, sodales non dui eget, rutrum molestie arcu. In hac habitasse platea dictumst.\
Nullam a purus id ex varius consequat. Sed in pellentesque dui. Vivamus enim augue, feugiat at euismod et, vulputate vel tortor. Quisque a enim augue. Pellentesque aliquet venenatis volutpat. Praesent viverra odio a euismod tincidunt. Aenean ut sagittis eros. Praesent lacus metus, blandit iaculis maximus non, elementum et augue. Nam lorem dui, tempus quis mollis nec, consectetur ac nisl. Nulla facilisi. Nam accumsan velit libero, sit amet placerat ex ultrices ac. Sed commodo luctus eros eu tincidunt. Suspendisse varius arcu dolor, ut ullamcorper metus malesuada in. Nunc ultrices mauris neque, a vulputate ante molestie nec.\
Nunc tristique eu nunc vitae mattis. Donec tincidunt et tellus vitae pellentesque. Quisque luctus enim sed facilisis maximus. Aliquam pulvinar lectus in dui ullamcorper malesuada. Duis elementum, dui sit amet pellentesque semper, sem ligula facilisis nisi, ut vehicula mauris elit in arcu. Sed facilisis facilisis nibh, nec sagittis tellus iaculis sit amet. Vivamus ante nisl, tempor sit amet nibh in, eleifend egestas quam. Praesent nec augue vitae tortor rutrum accumsan non ut nisi. Nulla et lacus ut libero venenatis iaculis vitae sit amet nisl. as"
