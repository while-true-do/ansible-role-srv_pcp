import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_pcp_package(host):
    pkg_pcp = host.package('pcp')
    pkg_sys = host.package('pcp-system-tools')
    assert pkg_pcp.is_installed
    assert pkg_sys.is_installed


def test_pcp_service(host):
    srv_pmcd = host.service('pmcd')
    srv_pmlo = host.service('pmlogger')
    assert srv_pmcd.is_running
    assert srv_pmcd.is_enabled
    assert srv_pmlo.is_running
    assert srv_pmlo.is_enabled


def test_pmcd_env(host):
    file = host.file('/etc/sysconfig/pmcd')
    assert file.exists
    assert file.contains('PMCD_LOCAL=0')
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0o644'


def test_pmlogger_control_d(host):
    file = host.file('/etc/pcp/pmlogger/control.d/labrat01')
    assert file.exists
    assert file.contains('labrat01')
    assert file.user == 'root'
    assert file.group == 'root'
    assert oct(file.mode) == '0o644'
