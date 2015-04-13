#!/usr/bin/env python

from os.path import basename
from datetime import datetime
import sys

from config_parser import OSConfigParser, print_comments


def show_header(fpath, release):
    date = datetime.strftime(datetime.today(), "%Y-%m-%d")

    print "#"
    print "# AUTOMATICALLY GENERATED ON {0}".format(date)
    print "# openstack config template (ini jinja2)"
    print "# original file: {0}".format(basename(fpath))
    print "# release: {0}".format(release)
    print "#"


def print_ini_jinja(parser, prefix, user_prefix):
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

            if user_prefix and not name.startswith(user_prefix):
                var_name = "{0}_{1}".format(user_prefix, var_name)

            if prefix:
                var_name = "{0}_{1}".format(prefix, var_name)

            print "{0}={{{{ {1} }}}}\n".format(name, var_name)


if __name__ == '__main__':
    fpath = sys.argv[1]
    user_prefix = sys.argv[2] if len(sys.argv) >= 3 else ''
    release = sys.argv[3] if len(sys.argv) >= 4 else ''

    parser = OSConfigParser()
    with open(fpath) as f:
        lines = [line.strip() for line in f.readlines()]
        parser.parse(lines)

        show_header(fpath, release)

        print_ini_jinja(parser, prefix="os", user_prefix=user_prefix)
