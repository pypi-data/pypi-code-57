testinfra_hosts = ['ansible://infrastructure1-host']


def test_internal_network(host):
    i2_host = host.get_host('ansible://infrastructure2-host',
                            ansible_inventory=host.backend.ansible_inventory)
    cmd = i2_host.run(r"hostname -I | sed -e 's/.*\(10.30.20.[0-9]*\).*/\1/'")
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    ip = cmd.stdout.strip()
    assert '10.30.20' in ip

    cmd = host.run(f"""
    set -xe
    ping -c 1 {ip}
    """)
    print(cmd.stdout)
    print(cmd.stderr)
    assert 0 == cmd.rc
    assert '1 packets transmitted' in cmd.stdout
