#!/usr/bin/env python

from datetime import datetime
import sys

import yaml

from config_parser import OSConfigParser, print_comments, show_header, \
                          format_var_name, value_to_yaml


def print_ansible_conf(parser, prefix, namespace):
    values = parser.values

    for section in values:
        print '\n## [{0}] ##\n'.format(section)

        if len(values[section]['comments']) > 0:
            print_comments(values[section]['comments'], newline=2)

        for name, entry in values[section]['entries'].iteritems():
            if len(entry['comments']) > 0:
                print_comments(entry['comments'])

            val = value_to_yaml(entry)

            section = format_var_name(section)

            if section.lower() != 'default':
                name = "{0}_{1}".format(section.lower(), name)

            if namespace and not name.startswith(namespace):
                name = "{0}_{1}".format(namespace, name)

            if prefix:
                name = "{0}_{1}".format(prefix, name)

            name = format_var_name(name)

            if val is not None:
                conf_line = yaml.dump(dict([(name, val)]), indent=2,
                                      default_flow_style=False)
            else:
                conf_line = "{0}: \n".format(name)

            deprecated = False
            if not deprecated:
                print conf_line
            else:
                print "#{0}".format(conf_line)

    print """
## [CUSTOM] ##
#
# This is a hash of custom value configs to append to conf file
# Format: (json)
# {
#     'section': {
#         'name': 'value'
#     }
# }
    """
    print "{0}_{1}: {2}".format(prefix, namespace, '{}')


if __name__ == '__main__':
    fpath = sys.argv[1]
    namespace = sys.argv[2] if len(sys.argv) >= 3 else ''
    prefix = sys.argv[3] if len(sys.argv) >= 4 else ''
    desc = sys.argv[4] if len(sys.argv) >= 5 else ''

    parser = OSConfigParser()
    with open(fpath) as f:
        lines = [line.strip() for line in f.readlines()]
        parser.parse(lines)

        show_header(fpath, namespace, prefix, desc)

        print_ansible_conf(parser, prefix=prefix, namespace=namespace)
