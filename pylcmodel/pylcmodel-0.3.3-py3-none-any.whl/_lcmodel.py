import pylcmodel.namelist as namelist

import paramiko
import sys
import os


# these are the result files produced by running LCModel
output_file_types = ("FILPS", "FILTAB", "FILCSV", "FILCOO", "FILPRI")


def run_lcm_remote(input_config_dict, control_namelist):
    config_dict = {
        "keep_remote_files": False
    }
    config_dict.update(input_config_dict)
    # there are some config values that we absolutely require, and some where
    # we can make intelligent guesses
    # obviously we definitely require the hostname of the remote computer we
    # are trying to connect to, and the username we will be logging in with
    if "hostname" not in config_dict:
        raise KeyError("hostname of LCModel computer not given in config file")
    if "user" not in config_dict:
        raise KeyError("user for LCModel computer not given in config file")
    if "port" not in config_dict:
        # assume default port of 22
        config_dict["port"] = "22"

    auth_keywords = ["password", "key_filename", "passphrase"]

    auth_kwargs = {key: config_dict[key] for key in auth_keywords if key in config_dict}

    # this is enough config to try and make a connection to the remote system
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    client.connect(config_dict["hostname"],
                   int(config_dict["port"]),
                   config_dict["user"],
                   **auth_kwargs
                   )

    sftp = client.open_sftp()

    if "remote_dir" not in config_dict:
        # ask the sftp for the current folder, which should be the home, then
        # create a pylcmodel folder inside it
        sftp.chdir(".")
        home_path = sftp.getcwd()
        config_dict["remote_dir"] = os.path.join(home_path, "pylcmodel")
        print("Warning: no remote_dir parameter in .pylcmodel configuration, "
        "remote files will be stored in {}".format(config_dict["remote_dir"]))
    if "lcmodel_path" not in config_dict:
        print("Warning: no lcmodel path in .pylcmodel configuration, "
        "searching for location of executable.")
        # first check if LCModel is in the path somewhere
        stdin, stdout, stderr = client.exec_command("command -v lcmodel")# >/dev/null 2>&1")
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            config_dict["lcmodel_path"] = "lcmodel"
            print("Ok: lcmodel found in path")
        # if it isn't in the path, look in the default location
        sftp.chdir(".")
        home_path = sftp.getcwd()
        proposed_lcmodel_path = os.path.join(home_path, ".lcmodel/bin/lcmodel")
        stdin, stdout, stderr = client.exec_command("[ -x {} ]".format(proposed_lcmodel_path))
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            config_dict["lcmodel_path"] = proposed_lcmodel_path
            print("Ok: lcmodel found at {}".format(config_dict["lcmodel_path"]))


    # define a simple helper function to convert a local path to a remote one
    def to_remote(local_path):
        filename = os.path.basename(os.path.abspath(local_path))
        return os.path.join(config_dict["remote_dir"], filename)

    remote_path_list = []
    def transfer_file(key):
        local_path = os.path.abspath(control_namelist[key])
        remote_path = to_remote(local_path)
        control_namelist[key] = remote_path
        sftp.put(local_path, remote_path)
        remote_path_list.append(remote_path)

    # there are three files we might need to transfer to the remote machine
    # 1) FILRAW is required, and is on the local machine
    # 2) FILH2O is not required, but is on the local machine if present
    # 3) FILBAS is required, but might be already on the remote
    transfer_file("FILRAW")
    if "FILH2O" in control_namelist:
        transfer_file("FILH2O")
    if "FILBAS" in control_namelist:
        if os.path.isfile(os.path.abspath(control_namelist["FILBAS"])):
            transfer_file("FILBAS")

    # change the paths for writing output to match the remote system
    # also build a map of paths to copy the results back after running
    output_files = []
    for output_type in output_file_types:
        if output_type in control_namelist:
            local_path = os.path.abspath(control_namelist[output_type])
            remote_path = to_remote(local_path)
            control_namelist[output_type] = remote_path
            output_files.append((local_path, remote_path))
            remote_path_list.append(remote_path)

    # write our modified namelist out as a remote control file
    remote_control_path = os.path.join( "foo.control")
    with sftp.open(remote_control_path, 'w') as fout:
        fout.write(namelist.dumps('LCMODL', control_namelist))

    # we can finally run the actual LCModel command now
    lcm_command = "{0} < {1}".format(config_dict["lcmodel_path"],
                                     remote_control_path)
    stdin, stdout, stderr = client.exec_command(lcm_command)

    exit_status = stdout.channel.recv_exit_status()
    print("exited with status: {}".format(exit_status))
    result = stdout.read().decode()
    err = stderr.read().decode()

    sys.stdout.write(result)
    sys.stderr.write(err)

    for local_path, remote_path in output_files:
        sftp.get(remote_path, local_path)

    if not config_dict["keep_remote_files"]:
        for remote_file in remote_path_list:
            sftp.remove(remote_file)

    client.close()

    return exit_status


def patch_crypto_be_discovery():
    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]

patch_crypto_be_discovery()
