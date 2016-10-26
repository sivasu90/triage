#!/usr/bin/python

from ansible.module_utils.basic import *
import subprocess
import ast
def get_vm_details(module):
    vm_id = module.params["vm_id"]
    cmd = "nova list --all-tenants|grep {}|grep ACTIVE".format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Check if VM id is correct and active", "stderr": stderr}
    cmd = "nova show {}|grep hypervisor_hostname|cut -d '|' -f3|xargs".format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Something went wrong", "stderr": stderr, "stdout": stdout}
    hypervisor_hostname = stdout.strip()
    return True, {vm_id: {
                    "hypervisor_hostname": hypervisor_hostname }}

def main():
    fields = {
             "vm_id": {"required": True, "type": "str"},
    }
    module = AnsibleModule(argument_spec=fields)
    result, msg = get_vm_details(module)
    if result:
        module.exit_json(changed=False, meta=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':  
    main()
