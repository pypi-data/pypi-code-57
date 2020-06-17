def catlist(catfile):
    """
    Returns a dictionary containing the categories and items read from
    the file passed as argument
    """
    fulldata={}
    rawfile=u''

    # Just make sure the parameters are sane
    if type(catfile) is not str:
        raise TypeError('File name must be a string')
    if type(catfile) is str and len(catfile)==0:
        raise ValueError('File name can not be empty')

    # Open file read-only and reads all lines
    try:
        with open(catfile,'r') as _file:
            rawfile = _file.readlines()
    except OSError:
        print("Could not open file {}".format(catfile), file=sys.stderr)
        raise

    # just in case someone tries to read a file without any valid category
    # or with lines before the first true category, puts the lines on a
    # default category
    cur_category='uncategorized'
    for lin in rawfile:
        # let's skip blank line. first strip all spaces, left and right
        lin=lin.rstrip().lstrip()
        # decide what to do. If a category line is well formed, create it, otherwise
        # add the line to an existing one
        if len(lin)==0 or lin[0]=='#': continue
        if lin[0]=='[' and lin[-1]==']':
            cur_category=lin[1:-1]
            # what happens if the category already exists ?
            if not fulldata.get(cur_category):
                fulldata[cur_category]=[]
        else:
            if not fulldata.get(cur_category):
                fulldata[cur_category]=[lin]
            else:
                fulldata[cur_category].append(lin)

    return fulldata
