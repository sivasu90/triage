#!/usr/bin/python

from ansible.module_utils.basic import *
import os

def run_and_validate_output(module, cmd, error_msg="Something went wrong"):
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        module.fail_json(msg={"rc":rc, "error": error_msg, "stderr": stderr})
    return stdout

def check_firewall_rules(module):
    tap_iface = module.params["tap_iface"]
    iface_id = tap_iface.split('-')[0].split('tap')[1]
    cmd = 'sudo iptables -S|grep {}|grep "sport 68"|grep "dport 67"|grep RETURN'.format(iface_id)
    stdout = run_and_validate_output(module, cmd, error_msg="Missing dhcp firewall rules on the compute node")
    cmd = 'sudo iptables -S|grep {}|grep "sport 67"|grep "dport 68"|grep DROP'.format(iface_id)
    stdout = run_and_validate_output(module, cmd, error_msg="Missing dhcp firewall rules on the compute node")
    module.exit_json(changed=False)

def main():
    fields = {
             "tap_iface": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    check_firewall_rules(module)

if __name__ == '__main__':
    main()
