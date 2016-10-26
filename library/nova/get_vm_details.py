#!/usr/bin/python

from ansible.module_utils.basic import *
import os
import subprocess
import ast

def get_value(data, key):
    data_lines = data.split('\n')
    return [x.split('|')[2].strip() for x in data_lines if key in x][0]

def get_vm_details(module):
    vm_id = module.params["vm_id"]
    cmd = "nova list --all-tenants|grep {}|grep ACTIVE".format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Check if VM id is correct and VM is active", "stderr": stderr}
    cmd = "nova show {}".format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Something went wrong", "stderr": stderr, "stdout": stdout}
    hypervisor_hostname = get_value(stdout, "OS-EXT-SRV-ATTR:hypervisor_hostname")
    vm_name_in_host = get_value(stdout, "OS-EXT-SRV-ATTR:instance_name")
    vm_name = get_value(stdout, " name ")
    ip_addresses = get_value(stdout, " network").split(',')
    net_name = [x.split('|')[1].split()[0].strip() for x in stdout.split('\n') if ' network' in x][0]
    sec_groups = get_value(stdout, "security_groups").split(',')
    return True, {
                    "hypervisor_hostname": hypervisor_hostname,
                    "vm_name_in_host": vm_name_in_host,
                    "vm_name": vm_name,
                    "ip_addresses": ip_addresses,
                    "sec_groups": sec_groups,
                    "network_name": net_name,
                 }


def main():
    fields = {
             "vm_id": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    result, msg = get_vm_details(module)
    if result:
        module.exit_json(changed=False, meta=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
