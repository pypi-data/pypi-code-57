from datetime import datetime as dt

def log(container_name, text):
    with open("%s.log" %container_name, "a+") as ifile:
        ifile.write("\n[%s] %s: %s" %(container_name, dt.now(), text))
