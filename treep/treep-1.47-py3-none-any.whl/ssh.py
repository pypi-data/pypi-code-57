from .process_calls import execute


def authenticity_of_host_is_established(host):

    command = 'ssh '+str(host)+' -o "BatchMode yes"'

    out = execute(command)

    if "Host key verification failed" in out:
        return False

    return True


def get_host(git_url):

    git_url = git_url.strip()
    
    if git_url.startswith("https"):
        return None

    host = git_url
    if host.startswith("git@"):
        host = host[4:]

    else:
        return None
        
    if ":" in host:
        index = host.rfind(':')
        host = host[:index]

    host = host.strip()
    return host
