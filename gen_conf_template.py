#!/usr/bin/env python

import sys

from config_parser import OSConfigParser, print_comments, var_namespace, show_header



def print_ini_jinja(parser, prefix, namespace):
    values = parser.values

    for section in values:
        print '\n[{0}]\n'.format(section)

        if len(values[section]['comments']) > 0:
            print_comments(values[section]['comments'], newline=1)

        for name, entry in values[section]['entries'].iteritems():
            if len(entry['comments']) > 0:
                print_comments(entry['comments'])

            var_name = name
            if section.lower() != 'default':
                var_name = "{0}_{1}".format(section.lower(), var_name)

            if namespace and not name.startswith(namespace):
                var_name = "{0}_{1}".format(namespace, var_name)

            var_name = "os_{0}".format(var_name)
            #if prefix:
            #    var_name = "{0}_{1}".format(prefix, var_name)

            print "{0}={{{{ {1} }}}}\n".format(name, var_name)


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
                    title="openstack config template", yaml=False)

        print_ini_jinja(parser, prefix=prefix, namespace=namespace)
