def name():
    return ('I, the son of my father, Ragib.')


def rm():
    pass


def ls(file_extension='', tree=False):
    if file_extension:
        if type(file_extension) is str:
            print('Files with {} extention')
        elif (type(file_extension) is list) or (type(file_extension) is tuple):
            print('Files with {} extentions'.format(file_extension))
        else:
            raise Exception("file_extension parameter should be either a string or a list or a tuple")

def cat():
    pass

def cd():
    pass

def touch():
    pass

def mkdir():
    pass

# get()
# soup()