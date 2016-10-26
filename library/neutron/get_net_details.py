#!/usr/bin/python

from ansible.module_utils.basic import *
import os
import subprocess
import ast

def get_value(data, key):
    data_lines = data.split('\n')
    return [x.split('|')[2].strip() for x in data_lines if key in x][0]

def get_net_details(module):
    net_name = module.params["net_name"]
    cmd = "neutron net-show {}".format(net_name)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Check if network name is correct and has a unique name", "stderr": stderr}
    net_id = get_value(stdout, " id ").strip()
    net_type = get_value(stdout, "provider:network_type")
    seg_id = int(get_value(stdout, "provider:segmentation_id"))
    subnets = get_value(stdout, "subnets").split(',')
    seg_id_hex = hex(seg_id)
    cmd = "neutron dhcp-agent-list-hosting-net {}|grep -v '+'|grep -v 'id'|cut -d '|' -f3".format(net_id)
    #module.fail_json(msg={"cmd":cmd})
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        return False, {"rc":rc, "error": "Something went wrong", "stderr": stderr, "stdout": stdout}
    if 'xxx' in stdout:
        return False, {"error": "One of the dhcp agents is down.  Check if your network node is up and all the dhcp agents are running properly in the network node"}
    if stdout == '':
        return False, {"error": "No DHCP agents are running for the network.  Check the network node if dhcp agents are started properly"}
    net_nodes = stdout.split('\n')[:-1]
    return True, {
                  "network_id": net_id,
                  "network_type": net_type,
                  "segmentation_id": seg_id,
                  "subnets": subnets,
                  "seg_id_hex": seg_id_hex,
                  "network_nodes": net_nodes
                 }


def main():
    fields = {
             "net_name": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    result, msg = get_net_details(module)
    if result:
        module.exit_json(changed=False, meta=msg)
    else:
        module.fail_json(msg=msg)

if __name__ == '__main__':
    main()
