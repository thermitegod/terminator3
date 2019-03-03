#!/usr/bin/env python2
#    Terminator - multiple gnome terminals in one window
#    Copyright (C) 2006-2010  cmsj@tenshu.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""Terminator by Chris Jones <cmsj@tenshu.net>"""

from terminatorlib.util import dbg
from terminatorlib.version import APP_NAME

# pylint: disable-msg=W0702
try:
    import gettext

    gettext.textdomain(APP_NAME)
    _translate = gettext.gettext
except:
    dbg("Using fallback _()")


    def _translate(text):
        """A _ function for systems without gettext. Effectively a NOOP"""
        return text


def _(s):
    return _translate(s) or ''
