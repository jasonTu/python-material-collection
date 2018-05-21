#! /usr/bin/env python
# coding: utf-8

"""Recover if user can use password in recently used for 5."""
import re
import os
import sys


PASSWD_FILE = '/etc/pam.d/passwd'
REG_REUSE_PWD = r'.*remember=(?P<number>\d+).*'
REPLACE_CONF = 'password required pam_unix.so remember=5 use_authtok md5 shadow'
REUSE_NUM = 5


def check_reuse_password():
    """Check reuse password."""
    with open(PASSWD_FILE) as fp:
        content = fp.read()
    ret = re.search(REG_REUSE_PWD, content)
    if not ret:
        return True
    number = int(ret.group('number'))
    return number < REUSE_NUM


def recover_reuse_password():
    """Recover reues password times."""
    ret = re.sub(
        REG_REUSE_PWD, REPLACE_CONF, open(PASSWD_FILE).read(), flags=re.M
    )
    with open(PASSWD_FILE, 'w+') as fp:
        fp.write(ret)


if __name__ == '__main__':
    ret = check_reuse_password()
    if ret:
        recover_reuse_password()
        sys.exit(0)
    else:
        sys.exit(1)
