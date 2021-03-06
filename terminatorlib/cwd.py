#!/usr/bin/env python3
# Terminator by Chris Jones <cmsj@tenshu.net>
# GPL v2 only
"""cwd.py - function necessary to get the cwd for a given pid on various OSes

>>> cwd = get_default_cwd()
>>> cwd.__class__.__name__
'str'
>>> func = get_pid_cwd()
>>> func.__class__.__name__
'function'

"""

import os
import platform

from terminatorlib.util import dbg, err


def get_default_cwd():
    """Determine a reasonable default cwd"""
    cwd = os.getcwd()
    if not os.path.exists(cwd) or not os.path.isdir(cwd):
        cwd = os.path.expanduser('~')

    return cwd


def get_pid_cwd():
    """Determine an appropriate cwd function for the OS we are running on"""
    func = lambda pid: None
    system = platform.system()

    if system == 'Linux':
        dbg('Using Linux get_pid_cwd')
        func = linux_get_pid_cwd
    elif system == 'FreeBSD':
        from terminatorlib import freebsd
        func = freebsd.get_process_cwd
        dbg('Using FreeBSD get_pid_cwd')
    elif system == 'SunOS':
        dbg('Using SunOS get_pid_cwd')
        func = sunos_get_pid_cwd
    else:
        dbg(f'Unable to determine a get_pid_cwd for OS: {system}')

    return func


def proc_get_pid_cwd(pid, path):
    """Extract the cwd of a PID from proc, given the PID and the /proc path to
    insert it into, e.g. /proc/%s/cwd"""
    try:
        cwd = os.path.realpath(path % pid)
    except Exception as ex:
        err(f'Unable to get cwd for PID {pid}: {ex}')
        cwd = '/'

    return cwd


def linux_get_pid_cwd(pid):
    """Determine the cwd for a given PID on Linux kernels"""
    return proc_get_pid_cwd(pid, '/proc/%s/cwd')


def sunos_get_pid_cwd(pid):
    """Determine the cwd for a given PID on SunOS kernels"""
    return proc_get_pid_cwd(pid, '/proc/%s/path/cwd')

# vim: set expandtab ts=4 sw=4:
