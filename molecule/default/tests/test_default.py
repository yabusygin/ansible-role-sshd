"""Test role."""

import os
import textwrap

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_sshd_config(host):
    """Test /etc/ssh/sshd_config file content."""
    actual = host.file("/etc/ssh/sshd_config").content_string
    expect = textwrap.dedent(
        """\
        # SSH transport

        ListenAddress 0.0.0.0:22
        ListenAddress [::]:22
        Protocol 2
        VersionAddendum none
        DebianBanner no
        HostKey /etc/ssh/ssh_host_rsa_key
        HostKey /etc/ssh/ssh_host_ecdsa_key
        HostKey /etc/ssh/ssh_host_ed25519_key
        RekeyLimit 1G 1h
        ClientAliveInterval 1m
        ClientAliveCountMax 3

        # User authentication and authorization

        LoginGraceTime 60s
        MaxAuthTries 3
        MaxStartups 10:30:20
        StrictModes yes
        Banner none
        AuthenticationMethods publickey password
        PubkeyAuthentication yes
        AuthorizedKeysFile %h/.ssh/authorized_keys
        PasswordAuthentication yes
        PermitEmptyPasswords no
        HostbasedAuthentication no
        ChallengeResponseAuthentication no
        KbdInteractiveAuthentication no
        GSSAPIAuthentication no
        KerberosAuthentication no
        UsePAM yes
        PermitRootLogin no

        # SSH connection

        PermitTTY yes
        AcceptEnv LANG LC_*
        PrintLastLog no
        PrintMotd no
        PermitUserEnvironment no
        PermitUserRC yes
        X11Forwarding yes
        X11UseLocalhost yes
        AllowTcpForwarding no
        AllowStreamLocalForwarding no
        AllowAgentForwarding no
        PermitTunnel no
        Subsystem sftp internal-sftp

        # Logging

        LogLevel INFO
        SyslogFacility AUTH

        # Daemon

        PidFile none

        # TCP transport

        TCPKeepAlive no

        # Conditional blocks

        Match All
            PasswordAuthentication no
        """,
    )
    assert expect == actual


def test_sshd_process(host):
    """Test that sshd process exists."""
    expect = "/usr/sbin/sshd -D"
    actual = host.process.get(comm="sshd").args
    assert expect == actual
