from os.path import basename, splitext
from datetime import datetime
from collections import OrderedDict

import yaml

from oslo_config import iniparser


VERSION = 0.2.1


class OSConfigParser(iniparser.BaseParser):
    comment_called = False
    values = None
    section = ''
    comments = []
    commented = False

    def __init__(self):
        self.values = OrderedDict()

    def assignment(self, key, value):
        self.values.setdefault(self.section, {'comments': [], 'entries': {}})
        self.values[self.section]['entries'][key] = {
          'value': value,
          'comments': self.comments,
          'commented': self.commented
        }
        self.comments = []
        self.commented = False

    def new_section(self, section):
        self.section = section
        self.values[self.section] = {
            'comments': self.comments,
            'entries': OrderedDict()
        }
        self.comments = []

    def comment(self, comment):
        if len(comment) > 0 and comment[0].isalpha() and '=' in comment:
            self.commented = True
            self.parse([comment])
            self.comments = []
        else:
            if False and ' = ' in comment:
                self.commented = True
                try:
                    self.parse([comment[1:]])
                    self.comments = []
                    return
                except:
                    pass

            self.comments.append(comment.lstrip())

    def parse(self, lineiter):
        key = None
        value = []

        for line in lineiter:
            self.lineno += 1

            line = line.rstrip()
            if not line:
                # Blank line, ends multi-line values
                if key:
                    key, value = self._assignment(key, value)
                continue
            elif line.startswith((' ', '\t')):
                # Continuation of previous assignment
                if key is None:
                    self.error_unexpected_continuation(line)
                else:
                    value.append(line.lstrip())
                continue

            if key:
                # Flush previous assignment, if any
                key, value = self._assignment(key, value)

            if line.startswith('['):
                # Section start
                section = self._get_section(line)
                if section:
                    self.new_section(section)
            elif line.startswith(('#', ';')):
                self.comment(line[1:])
            else:
                key, value = self._split_key_value(line)
                if not key:
                    return self.error_empty_key(line)

        if key:
            # Flush previous assignment, if any
            self._assignment(key, value)


def show_header(fpath, namespace, prefix, desc='', yaml=True):
    date = datetime.strftime(datetime.today(), "%Y-%m-%d")

    print "#"
    print "# AUTOMATICALLY GENERATED ON {0}".format(date)
    print "# ansible-openstack-config-gen version: {0}".format(VERSION)
    print "#"
    if desc:
        print "# {0}".format(desc)
    print "# file: {0}".format(basename(fpath))
    print "# namespace: {0}".format(namespace)
    print "# prefix: {0}".format(prefix)
    print "#"
    if yaml:
        print "---"
    else:
        print ""


def print_comments(comments, newline=0):
    for cmt in comments:
        print '# {0}'.format(cmt)
    for x in range(newline):
        print "\n"


def var_namespace(fpath, name):
    ns = splitext(basename(fpath.lower()).replace('-', '_'))[0]
    if not ns.startswith(name):
        ns = "{0}_{1}".format(name, ns)
    return ns


def infer_type(comments):
    text = ' '.join(comments)
    if '(multi valued)' in text:
        return 'multi'
    if '(list value)' in text:
        return 'list'
    if '(integer value)' in text:
        return 'int'


def format_var_name(name):
    return name.replace('-', '_').lower()


def value_to_yaml(entry):
    value_type = infer_type(entry['comments'])

    def convert(val):
        if value_type == 'int' or value_type == 'multi':
            val = None
        elif value_type == 'list':
            val = []
        else:
            val = ''
        return val

    if len(entry['value']) == 1:
        val = entry['value'][0]

        if val.startswith('<') and val.endswith('>'):
            val = ''
        else:
            try:
                val = yaml.load(val)
                if val is None:
                    val = convert(val)
            except yaml.scanner.ScannerError:
                pass

        return val
    else:
        raise Exception("Cannot convert multiple values %s" % values)
