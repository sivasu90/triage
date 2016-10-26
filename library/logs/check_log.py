#!/usr/bin/python

from ansible.module_utils.basic import *
import os
import subprocess
import ast

def get_failure(req_lines):
    Failure = []
    ERROR = []
    lines = req_lines.split('\n')
    for x in lines:
        if "Failed" in x:
           Failure.append(x)
        elif "ERROR" in x:
           ERROR.append(x)
    return Failure,ERROR            

def check_log(module):
    req_id = module.params["req_id"]
    path = module.params["log_path"]
    cmd = "grep -ir {} {}".format(req_id,path)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc": rc, "error": "No logs present for the req-id provided", "req-id": req_id}
    else:
        Failure, ERROR = get_failure(stdout)
        return True, {"Failure_message": Failure, "Error": ERROR}

def main():
    fields = {
             "req_id": {"required": True, "type": "str"},
             "log_path": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    result, msg = check_log(module)
    if result:
        module.exit_json(changed=False, meta=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
