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
    print "# ansible role defaults (yaml)"
    print "# original file: {0}".format(basename(fpath))
    print "# release: {0}".format(release)
    print "#"


def print_ansible_conf(parser, prefix, user_prefix):
    values = parser.values

    for section in values:           
        print '\n## [{0}] ##\n'.format(section)

        if len(values[section]['comments']) > 0:
            print_comments(values[section]['comments'], newline=2)

        for name, entry in values[section]['entries'].iteritems():
            if len(entry['comments']) > 0:
                print_comments(entry['comments'])

            if len(entry['value']) == 1:
                val = entry['value'][0]
                if val == '<None>':
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

            if user_prefix and not name.startswith(user_prefix):
                name = "{0}_{1}".format(user_prefix, name)

            #print "# config: {0}".format(name)

            if prefix:
                name = "{0}_{1}".format(prefix, name)

            print yaml.dump(dict([(name, val)]), indent=2, default_flow_style=False)


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

        print_ansible_conf(parser, prefix=prefix, user_prefix=user_prefix)