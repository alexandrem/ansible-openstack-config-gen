#!/usr/bin/env python

from datetime import datetime
import sys

import yaml

from config_parser import OSConfigParser, print_comments, var_namespace



def show_header(fpath):
    date = datetime.strftime(datetime.today(), "%Y-%m-%d")

    print "#"
    print "# AUTOMATICALLY GENERATED ON {0}".format(date)
    print "#"
    print "# This file remaps all os_* variables for the"
    print "# current service release."
    print "#"
    print "# Don't touch it and don't override the variables"
    print "# here in your playbook group vars."
    print "#"
    print "# You must always use the os_cfg_* variables."
    print "#"


def print_ansible_dyn_defaults(parser, prefix, namespace):
    values = parser.values

    for section in values:           
        for name, entry in values[section]['entries'].iteritems():
            print ""
            
            var_name = name

            if section.lower() != 'default':
                var_name = "{0}_{1}".format(section.lower(), var_name)

            if namespace and not var_name.startswith(namespace):
                var_name = "{0}_{1}".format(namespace, var_name)

            tmpl_name = "os_tmpl_{0}".format(var_name)

            os_release_var_name = "{0}_{1}".format(prefix, var_name)

            # end user variables are prefixed with cfg_
            user_var_name = "os_cfg_{0}".format(var_name)

            print "{0}: \"{{{{ {1} | default({2}) }}}}\"".format(tmpl_name,
                                                                 user_var_name,
                                                                 os_release_var_name)


if __name__ == '__main__':
    fpath = sys.argv[1]
    namespace = sys.argv[2] if len(sys.argv) >= 3 else ''
    prefix = sys.argv[3] if len(sys.argv) >= 4 else ''

    parser = OSConfigParser()
    with open(fpath) as f:
        lines = [line.strip() for line in f.readlines()]
        parser.parse(lines)

        namespace = var_namespace(fpath, namespace)

        show_header(fpath)

        print_ansible_dyn_defaults(parser, prefix=prefix, namespace=namespace)