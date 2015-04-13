#!/usr/bin/env python

from os.path import basename
from datetime import datetime
import sys

import yaml

from config_parser import OSConfigParser, print_comments


def show_header(fpath, release):
    date = datetime.strftime(datetime.today(), "%Y-%m-%d")

    print "#"
    print "# AUTOMATICALLY GENERATED ON {0}".format(date)
    print "# ansible dynamic variables (yaml)"
    print "# original file: {0}".format(basename(fpath))
    print "# release: {0}".format(release)
    print "#"


def print_ansible_dyn_defaults(parser, prefix, user_prefix):
    values = parser.values

    for section in values:           
        for name, entry in values[section]['entries'].iteritems():

            var_name = name

            if section.lower() != 'default':
                var_name = "{0}_{1}".format(section.lower(), var_name)

            if user_prefix and not var_name.startswith(user_prefix):
                var_name = "{0}_{1}".format(user_prefix, var_name)

            tmpl_name = "os_{0}".format(var_name)

            os_release_var_name = "{0}_{1}".format(prefix, var_name)

            print "{0}: \"{{{{ {1} | default({2}) }}}}\"".format(tmpl_name, var_name, os_release_var_name)
            print ""


if __name__ == '__main__':
    fpath = sys.argv[1]
    user_prefix = sys.argv[2] if len(sys.argv) >= 3 else ''
    release = sys.argv[3] if len(sys.argv) >= 4 else ''

    parser = OSConfigParser()
    with open(fpath) as f:
        lines = [line.strip() for line in f.readlines()]
        parser.parse(lines)

        show_header(fpath, release)

        prefix = "os_{0}".format(release)

        print_ansible_dyn_defaults(parser, prefix=prefix, user_prefix=user_prefix)
