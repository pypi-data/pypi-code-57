a=123
print('hello world')

def get_a():
	a='a'
	return a
def get_b():
	a='b'
	return a
def get_c():
	a='c'
	return a
def get_abc():
	a=get_a()+get_b()+get_c()
	return a
