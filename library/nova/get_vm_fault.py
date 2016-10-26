#!/usr/bin/python

from ansible.module_utils.basic import *
import os
import subprocess
import ast

def get_value(data, key):
    data_lines = data.split('\n')
    f = [x.split('|')[2].strip() for x in data_lines if key in x][0]
    fault = f+'"}'
    return fault

def get_vm_fault(module):
    vm_id = module.params["vm_id"]
    cmd = "nova show {}".format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Something went wrong", "stderr": stderr, "stdout": stdout}
    fault = get_value(stdout, "fault")
    if "No valid host was found" in fault:
       return True, {"msg": "Requested resource not available, Change the selected flavor to lesser size"}
    if "Timed out waiting for a reply" in fault:
       return True, {"msg": "Failed due to overloaded nova services, try again"}
    else:
       return False,{"msg": "Fault reason cannot be found, check in logs for details"}

def main():
    fields = {
             "vm_id": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    result, msg = get_vm_fault(module)
    if result:
        module.exit_json(changed=False, msg=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
