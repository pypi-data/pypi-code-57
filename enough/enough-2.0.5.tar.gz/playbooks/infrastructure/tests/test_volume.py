testinfra_hosts = ['ansible://infrastructure4-host']


def test_volume(host):
    cmd = host.run("""
    set -xe
    ! test -e /dev/mapper/spare
    lsblk | grep -E '(vda|sdb)'
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
