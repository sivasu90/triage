#!/usr/bin/python

from ansible.module_utils.basic import *
import os
def check_env_vars(module):
    min_env_vars = ["OS_USERNAME", "OS_PASSWORD", "OS_PROJECT_NAME", "OS_AUTH_URL"]
    missing_vars = []
    for var in min_env_vars:
        if var not in os.environ:
            missing_vars.append(var)
    if len(missing_vars) > 0:
        msg = {"error": "Missing env_vars {}. Source missing environment variables".format(missing_vars)}
        module.fail_json(msg=msg)
    if "OS_IDENTITY_API_VERSION" in os.environ and "OS_IDENTITY_API_VERSION" == "3":
        domain_vars = ["OS_PROJECT_DOMAIN_NAME", "OS_PROJECT_DOMAIN_ID", "OS_USER_DOMAIN_NAME", "OS_USER_DOMAIN_ID", "OS_DOMAIN_NAME", "OS_DOMAIN_ID"]
        if len([x for x in domain_vars if x in os.environ]) == 0:
            msg = {"error": "Missing env_vars Source any of the vars{}".format(domain_vars)}
            module.fail_json(msg=msg)
    module.exit_json(changed=False, meta="Env variables validated")

def main():
    module = AnsibleModule(argument_spec={})
    check_env_vars(module)

if __name__ == '__main__':
    main()
