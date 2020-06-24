# passwordless entrance to clusters:
# $ ssh-keygen # (leave it without password)
# $ ssh-copy-id -i /Users/admin/.ssh/id_rsa ulisesrosasp@login.colonialone.gwu.edu
# $ ssh ulisesrosasp@login.colonialone.gwu.edu # (test it)
# source: https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login

import os
import sys
import json
import shutil
import subprocess

run_string = lambda a: subprocess.Popen(a.split()).communicate()
# run_string = lambda a: print(a.split())

def str_gather(json_file): 
    
    with open(json_file, 'r') as f:
        params = json.load(f)   
    
    from_str = "scp -q -o LogLevel=QUIET -i {key1} -r {userid1}@{host1}:{path1}/{d}{globs} {local_d}"
    to_str   = "scp -q -o LogLevel=QUIET -i {key2} -r {d} {userid2}@{host2}:{path2}"

    to_params   = params['to']
    from_params = params['from']
    
    return (
        from_str.format(
            key1    = from_params['key'],
            userid1 = from_params['userid'],
            host1   = from_params['host'],
            path1   = from_params['path'],
            d       = "{d}",
            globs   = "{globs}",
            local_d = "{local_d}"
        ),
        to_str.format(
            key2    = to_params['key'],
            userid2 = to_params['userid'],
            host2   = to_params['host'],
            path2   = to_params['path'],
            d       = "{d}"
        )
    )
def run_downlist(glob_patt, frc, directory):
    
    if glob_patt:
        if not os.path.isdir(directory):
            os.mkdir(directory)
            
        for g in glob_patt:
            run_string(
                frc.format(
                    d       = directory,
                    local_d = directory,
                    globs   = "/" + g.strip()
                )
            )
    else:        
        run_string(
            frc.format(
                d       = directory,
                local_d = ".",
                globs   = ""
            )
        )
        
def write_rest(dirs, out, done):
#     out   = "rest_" + file
    out_l = sorted(set(dirs) - set(done))
    
    with open(out, 'w') as f:
        f.writelines( out_l )
