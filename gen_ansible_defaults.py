#!/usr/bin/env python

from datetime import datetime
import sys

import yaml

from config_parser import OSConfigParser, print_comments, var_namespace, \
                          show_header, infer_type



def print_ansible_conf(parser, prefix, namespace):
    values = parser.values

    for section in values:           
        print '\n## [{0}] ##\n'.format(section)

        if len(values[section]['comments']) > 0:
            print_comments(values[section]['comments'], newline=2)

        for name, entry in values[section]['entries'].iteritems():
            if len(entry['comments']) > 0:
                print_comments(entry['comments'])

            value_type = infer_type(entry['comments'])

            if len(entry['value']) == 1:
                val = entry['value'][0]

                if val == '<None>':
                    if value_type == 'int':
                        val = None
                    elif value_type == 'multi':
                        val = []
                    else:
                        val = ''
                else:
                    try:
                        val = yaml.load(val)
                        if val is None:
                            val = ''
                    except yaml.scanner.ScannerError:
                        pass

            if section.lower() != 'default':
                name = "{0}_{1}".format(section.lower(), name)

            if namespace and not name.startswith(namespace):
                name = "{0}_{1}".format(namespace, name)

            #print "# config: {0}".format(name)

            if prefix:
                name = "{0}_{1}".format(prefix, name)

            if val is not None:
                conf_line = yaml.dump(dict([(name, val)]), indent=2, default_flow_style=False)
            else:
                conf_line = "{0}: \n".format(name)

            deprecated = False
            if not deprecated:
                print conf_line
            else:
                print "#{0}".format(conf_line)


if __name__ == '__main__':
    fpath = sys.argv[1]
    namespace = sys.argv[2] if len(sys.argv) >= 3 else ''
    prefix = sys.argv[3] if len(sys.argv) >= 4 else ''

    parser = OSConfigParser()
    with open(fpath) as f:
        lines = [line.strip() for line in f.readlines()]
        parser.parse(lines)

        namespace = var_namespace(fpath, namespace)

        full_namespace = "{0}_{1}".format(prefix, namespace) if prefix else namespace
        show_header(fpath, full_namespace,
                    title="ansible defaults (yaml)")

        print_ansible_conf(parser, prefix=prefix, namespace=namespace)