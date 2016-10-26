#!/usr/bin/python

from ansible.module_utils.basic import *
import os
import subprocess
import ast

def find_failure(module):
    log = module.params["failure_message"]
    if "compute_task_build_instances" in log:
       return True, {"next": "Check nova compute logs for further details"}
    if "Failed to retrieve ports" in log:
       return True, {"next": "Might be a problem due to busy neutron server process, check for neutron server utilization"}
    if "Neutron error creating port on network" in log:
       return True, {"next": "Port creation failed, Check ovs log for any ServiceUnavailabe Error"}
    if "ServiceUnavailable" in log:
       return True, {"Neutron server is not responding"}
    else:
       return False, {"out": "Not Found"}

def main():
   fields = {
             "failure_message": {"required": True, "type": "str"}
    }
   module = AnsibleModule(argument_spec=fields)
   result, msg = find_failure(module)
   if result:
      module.exit_json(changed=False, msg=msg)
   else:
      module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
