<!--
name: README.md
description: This file contains important information for the repository.
author: while-true-do.io
contact: hello@while-true-do.io
license: BSD-3-Clause
-->

<!-- github shields -->
[![Github (tag)](https://img.shields.io/github/tag/while-true-do/ansible-role-srv_pcp.svg)](https://github.com/while-true-do/ansible-role-srv_pcp/tags)
[![Github (license)](https://img.shields.io/github/license/while-true-do/ansible-role-srv_pcp.svg)](https://github.com/while-true-do/ansible-role-srv_pcp/blob/master/LICENSE)
[![Github (issues)](https://img.shields.io/github/issues/while-true-do/ansible-role-srv_pcp.svg)](https://github.com/while-true-do/ansible-role-srv_pcp/issues)
[![Github (pull requests)](https://img.shields.io/github/issues-pr/while-true-do/ansible-role-srv_pcp.svg)](https://github.com/while-true-do/ansible-role-srv_pcp/pulls)
<!-- travis shields -->
[![Travis (com)](https://img.shields.io/travis/com/while-true-do/ansible-role-srv_pcp.svg)](https://travis-ci.com/while-true-do/ansible-role-srv_pcp)
<!-- ansible shields -->
[![Ansible (min. version)](https://img.shields.io/badge/dynamic/yaml.svg?label=Min.%20Ansible%20Version&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwhile-true-do%2Fansible-role-srv_pcp%2Fmaster%2Fmeta%2Fmain.yml&query=%24.galaxy_info.min_ansible_version&colorB=black)](https://galaxy.ansible.com/while_true_do/srv_pcp)
[![Ansible (platforms)](https://img.shields.io/badge/dynamic/yaml.svg?label=Supported%20OS&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwhile-true-do%2Fansible-role-srv_pcp%2Fmaster%2Fmeta%2Fmain.yml&query=galaxy_info.platforms%5B*%5D.name&colorB=black)](https://galaxy.ansible.com/while_true_do/srv_pcp)
[![Ansible (tags)](https://img.shields.io/badge/dynamic/yaml.svg?label=Galaxy%20Tags&url=https%3A%2F%2Fraw.githubusercontent.com%2Fwhile-true-do%2Fansible-role-srv_pcp%2Fmaster%2Fmeta%2Fmain.yml&query=%24.galaxy_info.galaxy_tags%5B*%5D&colorB=black)](https://galaxy.ansible.com/while_true_do/srv_pcp)

# Ansible Role: srv_pcp

An Ansible Role to install and configure [Performance Co-Pilot](https://pcp.io/).

## Motivation

[Performance Co-Pilot](https://pcp.io/) is a system performance analysis
toolkit. The tool can be used for multiple purposes and supports lot's of
software via "Performance Metrics Domain Agents (pmda)".

## Description

This Role installs Performance Co-Pilot and configures it.

-   configure pmcd to collect logs as a "Collector Host"
-   configure pmlogger to fetch logs as a "Monitoring Host"

## Requirements

Used Modules:

-   [Ansible package_facts Module](https://docs.ansible.com/ansible/latest/modules/package_facts_module.html)
-   [Ansible package Module](https://docs.ansible.com/ansible/latest/modules/package_module.html)
-   [Ansible service_facts Module](https://docs.ansible.com/ansible/latest/modules/service_facts_module.html)
-   [Ansible service Module](https://docs.ansible.com/ansible/latest/modules/service_module.html)
-   [Ansible template Module](https://docs.ansible.com/ansible/latest/modules/template_module.html)

## Installation

Install from [Ansible Galaxy](https://galaxy.ansible.com/while_true_do/srv_pcp)
```
ansible-galaxy install while_true_do.srv_pcp
```

Install from [Github](https://github.com/while-true-do/ansible-role-srv_pcp)
```
git clone https://github.com/while-true-do/ansible-role-srv_pcp.git while_true_do.srv_pcp
```

## Usage

### Role Variables

```
---
# defaults file for while_true_do.srv_pcp

# Package Management
wtd_srv_pcp_package:
  - pcp
  - pcp-system-tools
# Extra pmda packages, to be installed
# Enabling the metrics is currently not supported.
wtd_srv_pcp_package_pmda: []
# State can be present|latest|absent
wtd_srv_pcp_package_state: "present"

# Service Management
wtd_srv_pcp_service:
  - pmcd
  - pmlogger
# State can be started|stopped
wtd_srv_pcp_service_state: "started"
# Enabled can be true|false
wtd_srv_pcp_service_enabled: true

# Firewalld Management
wtd_srv_pcp_firewall_service: "pmcd"
# State can be enabled|disabled
wtd_srv_pcp_firewall_service_state: "enabled"
# Define a zone, to be used
wtd_srv_pcp_firewall_service_zone: "public"

# Configuration Management
# 0 = permits remote connections, 1 = forbids remote connections
# You may have to enable proper firewall rules
wtd_srv_pcp_conf_pmcd_local: 1
wtd_srv_pcp_conf_pmcd_maxpending: 5
wtd_srv_pcp_conf_pmcd_root_agent: 1
wtd_srv_pcp_conf_pmcd_restart_agents: 1
wtd_srv_pcp_conf_pmcd_wait_timeout: 60

wtd_srv_pcp_conf_pmlogger_control_d: []
# Simple example with hostname
# - name: "labrat01"
#   host: "labrat01"
# IP example
# - name: "labrat01"
#   host: "192.168.0.100"
# FQDN Example
# - name: "labrat01.while-true-do.io"
#   host: "labrat01.while-true-do.io"
# Full Example
# - name: "labrat01"
#   host: "labrat01"
#   primary: "n"
#   socks: "n"
#   endtime: "24h10m"
```

### Example Playbook

Running Ansible
[Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
can be done in a
[playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html).

#### Simple

```
---
- hosts: all
  roles:
    - role: while_true_do.srv_pcp
```

#### Configure a Collector Host (remote accessible)

```
- hosts: all
  roles:
    - role: while_true_do.srv_pcp
      wtd_srv_pcp_conf_pmcd_local: 0
```

#### Configure a Monitor Host (to fetch from other hosts)

```
- hosts: all
  roles:
    - role: while_true_do.srv_pcp
      wtd_srv_pcp_conf_pmcd_local: 0
      wtd_srv_pcp_conf_pmlogger_control_d:
        - name: "labrat01"
          host: "labrat01.wtd.local"
        - name: "labrat02"
          host: "192.168.122.10"
        - name: "labrat03"
          host: "labrat03"
```

## Known Issues

1.  RedHat Testing is currently not possible in public, due to limitations
    in subscriptions.
2.  Some services and features cannot be tested properly, due to limitations
    in docker.

## Testing

Most of the "generic" tests are located in the
[Test Library](https://github.com/while-true-do/test-library).

Ansible specific testing is done with
[Molecule](https://molecule.readthedocs.io/en/stable/).

Infrastructure testing is done with
[testinfra](https://testinfra.readthedocs.io/en/stable/).

Automated testing is done with [Travis CI](https://travis-ci.com).

## Contribute

Thank you so much for considering to contribute. We are very happy, when somebody
is joining the hard work. Please fell free to open
[Bugs, Feature Requests](https://github.com/while-true-do/ansible-role-srv_pcp/issues)
or [Pull Requests](https://github.com/while-true-do/ansible-role-srv_pcp/pulls) after
reading the [Contribution Guideline](https://github.com/while-true-do/doc-library/blob/master/docs/CONTRIBUTING.md).

See who has contributed already in the [kudos.txt](./kudos.txt).

## License

This work is licensed under a [BSD-3-Clause License](https://opensource.org/licenses/BSD-3-Clause).

## Contact

-   Site <https://while-true-do.io>
-   Twitter <https://twitter.com/wtd_news>
-   Code <https://github.com/while-true-do>
-   Mail [hello@while-true-do.io](mailto:hello@while-true-do.io)
-   IRC [freenode, #while-true-do](https://webchat.freenode.net/?channels=while-true-do)
-   Telegram <https://t.me/while_true_do>
