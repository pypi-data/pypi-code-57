testinfra_hosts = ['ansible://infrastructure1-host']


def test_encrypted_volume(host):
    cmd = host.run("""
    set -xe
    test -e /dev/mapper/spare
    grep -q /srv /etc/fstab
    test ! -e /srv/docker
    test ! -e /srv/snap
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
