testinfra_hosts = ['ansible://infrastructure5-host']


def test_no_volume(host):
    cmd = host.run("""
    set -xe
    ! lsblk | grep -E '(vda|sdb)'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
