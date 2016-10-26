#!/usr/bin/python

from ansible.module_utils.basic import *
import os

def check_net_namespace(module):
    net_id = module.params["net_id"]
    cmd = "sudo ip netns list|grep {}".format(net_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        error_msg = "Missing network namespace on the network node for network {}".format(net_id)
        module.fail_json(msg={"rc":rc, "error": error_msg, "stderr": stderr})
    cmd = "sudo ps aux|grep {}|grep dnsmasq".format(net_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        error_msg = "DHCP service is not running for the network {}".format(net_id)
        module.fail_json(msg={"rc":rc, "error": error_msg, "stderr": stderr})
    module.exit_json(changed=False,meta={"stdout":stdout})    

def main():
    fields = {
             "net_id": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    check_net_namespace(module)

if __name__ == '__main__':
    main()
