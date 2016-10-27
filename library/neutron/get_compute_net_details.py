#!/usr/bin/python

from ansible.module_utils.basic import *
import os
import ast
import yaml

def check_net_namespace(module):
    vm_id = module.params["vm_id"]
    cmd = '''sudo grep -i tap /var/lib/nova/instances/{}/libvirt.xml|cut -d '"' -f2'''.format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        error_msg = "Missing network interface on the VM {}".format(vm_id)
        module.fail_json(msg={"rc":rc, "error": error_msg, "stderr": stderr})
    tap_iface = stdout
    cmd = "sudo ovs-vsctl list-br"
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        error_msg = "Missing network interface on the VM {}".format(vm_id)
        module.fail_json(msg={"rc":rc, "error": error_msg, "stderr": stderr})
    ovs_bridges = stdout.split('\n')
    if 'br-int' not in ovs_bridges:
        module.fail_json(msg={"ConfigError":"br-int not found in ovs bridges on the compute"})
    net_details = ast.literal_eval(module.params["net_details"])
    '''
    if net_details['network_type'] in ['vxlan', 'gre']:
        if 'tun' not in ovs_bridges:
            module.fail_json(msg={"ConfigError":"Tunnel bridge not found in ovs bridges on the compute"})
    '''
    cmd = '''sudo grep -i tap /var/lib/nova/instances/{}/libvirt.xml|cut -d '"' -f2'''.format(vm_id)
    rc, stdout, stderr = module.run_command(cmd, use_unsafe_shell=True)
    if rc != 0:
        error_msg = "Missing network interface on the VM {}".format(vm_id)
        module.fail_json(msg={"rc":rc, "error": error_msg, "stderr": stderr})
    output = {
              "tap_interface": tap_iface,
              "ovs_bridges": ovs_bridges
             }
    module.exit_json(changed=False,meta=output)

def main():
    fields = {
             "vm_id": {"required": True, "type": "str"},
             "net_details": {"required": True, "type": "str"}
    }
    module = AnsibleModule(argument_spec=fields)
    check_net_namespace(module)

if __name__ == '__main__':
    main()
