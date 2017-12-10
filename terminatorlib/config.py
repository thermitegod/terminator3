#!/usr/bin/env python2
#    TerminatorConfig - layered config classes
#    Copyright (C) 2006-2010  cmsj@tenshu.net
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 2 only.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

"""Terminator by Chris Jones <cmsj@tenshu.net>

Classes relating to configuration

>>> DEFAULTS['global_config']['focus']
'click'
>>> config = Config()
>>> config['focus'] = 'sloppy'
>>> config['focus']
'sloppy'
>>> DEFAULTS['global_config']['focus']
'click'
>>> config2 = Config()
>>> config2['focus']
'sloppy'
>>> config2['focus'] = 'click'
>>> config2['focus']
'click'
>>> config['focus']
'click'
>>> config['geometry_hinting'].__class__.__name__
'bool'
>>> plugintest = {}
>>> plugintest['foo'] = 'bar'
>>> config.plugin_set_config('testplugin', plugintest)
>>> config.plugin_get_config('testplugin')
{'foo': 'bar'}
>>> config.plugin_get('testplugin', 'foo')
'bar'
>>> config.plugin_get('testplugin', 'foo', 'new')
'bar'
>>> config.plugin_get('testplugin', 'algo')
Traceback(most recent call last):
...
KeyError: 'ConfigBase::get_item: unknown key algo'
>>> config.plugin_get('testplugin', 'algo', 1)
1
>>> config.plugin_get('anothertestplugin', 'algo', 500)
500
>>> config.get_profile()
'default'
>>> config.set_profile('my_first_new_testing_profile')
>>> config.get_profile()
'my_first_new_testing_profile'
>>> config.del_profile('my_first_new_testing_profile')
>>> config.get_profile()
'default'
>>> config.list_profiles().__class__.__name__
'list'
>>> config.options_set({})
>>> config.options_get()
{}
>>> 

"""

import json
import platform
import os
from copy import copy
from terminatorlib import optionparse
from terminatorlib.borg import Borg
from terminatorlib.util import dbg, err, DEBUG, get_config_dir, dict_diff

from gi.repository import Gio

DEFAULTS = {
        'global_config':   {
            'dbus'                  : True,
            'focus'                 : 'click',
            'handle_size'           : -1,
            'geometry_hinting'      : False,
            'window_state'          : 'normal',
            'borderless'            : False,
            'extra_styling'         : True,
            'tab_position'          : 'top',
            'broadcast_default'     : 'group',
            'close_button_on_tab'   : True,
            'hide_tabbar'           : False,
            'scroll_tabbar'         : False,
            'homogeneous_tabbar'    : True,
            'hide_from_taskbar'     : False,
            'always_on_top'         : False,
            'hide_on_lose_focus'    : False,
            'sticky'                : False,
            'use_custom_url_handler': False,
            'custom_url_handler'    : '',
            'disable_real_transparency' : False,
            'title_hide_sizetext'   : False,
            'title_transmit_fg_color' : '#ffffff',
            'title_transmit_bg_color' : '#c80003',
            'title_receive_fg_color' : '#ffffff',
            'title_receive_bg_color' : '#0076c9',
            'title_inactive_fg_color' : '#000000',
            'title_inactive_bg_color' : '#c0bebf',
            'inactive_color_offset': 0.8,
            'enabled_plugins'       : ['LaunchpadBugURLHandler',
                                       'LaunchpadCodeURLHandler',
                                       'APTURLHandler'],
            'suppress_multiple_term_dialog': False,
            'always_split_with_profile': False,
            'title_use_system_font' : True,
            'title_font'            : 'Sans 9',
            'putty_paste_style'     : False,
            'smart_copy'            : True,
        },
        'keybindings': {
            'zoom_in'          : '<Control>plus',
            'zoom_out'         : '<Control>minus',
            'zoom_normal'      : '<Control>0',
            'new_tab'          : '<Shift><Control>t',
            'cycle_next'       : '<Control>Tab',
            'cycle_prev'       : '<Shift><Control>Tab',
            'go_next'          : '<Shift><Control>n',
            'go_prev'          : '<Shift><Control>p',
            'go_up'            : '<Alt>Up',
            'go_down'          : '<Alt>Down',
            'go_left'          : '<Alt>Left',
            'go_right'         : '<Alt>Right',
            'rotate_cw'        : '<Super>r',
            'rotate_ccw'       : '<Super><Shift>r',
            'split_horiz'      : '<Shift><Control>o',
            'split_vert'       : '<Shift><Control>e',
            'close_term'       : '<Shift><Control>w',
            'copy'             : '<Shift><Control>c',
            'paste'            : '<Shift><Control>v',
            'toggle_scrollbar' : '<Shift><Control>s',
            'search'           : '<Shift><Control>f',
            'page_up'          : '',
            'page_down'        : '',
            'page_up_half'     : '',
            'page_down_half'   : '',
            'line_up'          : '',
            'line_down'        : '',
            'close_window'     : '<Shift><Control>q',
            'resize_up'        : '<Shift><Control>Up',
            'resize_down'      : '<Shift><Control>Down',
            'resize_left'      : '<Shift><Control>Left',
            'resize_right'     : '<Shift><Control>Right',
            'move_tab_right'   : '<Shift><Control>Page_Down',
            'move_tab_left'    : '<Shift><Control>Page_Up',
            'toggle_zoom'      : '<Shift><Control>x',
            'scaled_zoom'      : '<Shift><Control>z',
            'next_tab'         : '<Control>Page_Down',
            'prev_tab'         : '<Control>Page_Up',
            'switch_to_tab_1'  : '',
            'switch_to_tab_2'  : '',
            'switch_to_tab_3'  : '',
            'switch_to_tab_4'  : '',
            'switch_to_tab_5'  : '',
            'switch_to_tab_6'  : '',
            'switch_to_tab_7'  : '',
            'switch_to_tab_8'  : '',
            'switch_to_tab_9'  : '',
            'switch_to_tab_10' : '',
            'full_screen'      : 'F11',
            'reset'            : '<Shift><Control>r',
            'reset_clear'      : '<Shift><Control>g',
            'hide_window'      : '<Shift><Control><Alt>a',
            'group_all'        : '<Super>g',
            'group_all_toggle' : '',
            'ungroup_all'      : '<Shift><Super>g',
            'group_tab'        : '<Super>t',
            'group_tab_toggle' : '',
            'ungroup_tab'      : '<Shift><Super>t',
            'new_window'       : '<Shift><Control>i',
            'new_terminator'   : '<Super>i',
            'broadcast_off'    : '<Alt>o',
            'broadcast_group'  : '<Alt>g',
            'broadcast_all'    : '<Alt>a',
            'insert_number'    : '<Super>1',
            'insert_padded'    : '<Super>0',
            'edit_window_title': '<Control><Alt>w',
            'edit_tab_title'   : '<Control><Alt>a',
            'edit_terminal_title': '<Control><Alt>x',
            'layout_launcher'  : '<Alt>l',
            'next_profile'     : '',
            'previous_profile' : '', 
            'help'             : 'F1'
        },
        'profiles': {
            'default':  {
                'allow_bold'            : True,
                'audible_bell'          : False,
                'visible_bell'          : False,
                'urgent_bell'           : False,
                'icon_bell'             : True,
                'background_color'      : '#000000',
                'background_darkness'   : 0.5,
                'background_type'       : 'solid',
                'backspace_binding'     : 'ascii-del',
                'delete_binding'        : 'escape-sequence',
                'color_scheme'          : 'grey_on_black',
                'cursor_blink'          : True,
                'cursor_shape'          : 'block',
                'cursor_color'          : '',
                'cursor_color_fg'       : True,
                'term'                  : 'xterm-256color',
                'colorterm'             : 'truecolor',
                'font'                  : 'Mono 10',
                'foreground_color'      : '#aaaaaa',
                'show_titlebar'         : True,
                'scrollbar_position'    : "right",
                'scroll_background'     : True,
                'scroll_on_keystroke'   : True,
                'scroll_on_output'      : False,
                'scrollback_lines'      : 500,
                'scrollback_infinite'   : False,
                'exit_action'           : 'close',
                'palette'               : '#2e3436:#cc0000:#4e9a06:#c4a000:\
#3465a4:#75507b:#06989a:#d3d7cf:#555753:#ef2929:#8ae234:#fce94f:\
#729fcf:#ad7fa8:#34e2e2:#eeeeec',
                'word_chars'            : '-,./?%&#:_',
                'mouse_autohide'        : True,
                'login_shell'           : False,
                'use_custom_command'    : False,
                'custom_command'        : '',
                'use_system_font'       : True,
                'use_theme_colors'      : False,
                'encoding'              : 'UTF-8',
                'active_encodings'      : ['UTF-8', 'ISO-8859-1'],
                'focus_on_close'        : 'auto',
                'force_no_bell'         : False,
                'cycle_term_tab'        : True,
                'copy_on_selection'     : False,
                'rewrap_on_resize'      : True,
                'split_to_group'        : False,
                'autoclean_groups'      : True,
                'http_proxy'            : '',
                'ignore_hosts'          : ['localhost','127.0.0.0/8','*.local'],
            },
        },
        'layouts': {
                'default': {
                    'window0': {
                        'type': 'Window',
                        'parent': ''
                        },
                    'child1': {
                        'type': 'Terminal',
                        'parent': 'window0'
                        }
                    }
                },
        'plugins': {
        },
}

class Config(object):
    """Class to provide a slightly richer config API above ConfigBase"""
    base = None
    profile = None
    system_mono_font = None
    system_prop_font = None
    system_focus = None
    inhibited = None
    
    def __init__(self, profile='default'):
        self.base = ConfigBase()
        self.set_profile(profile)
        self.inhibited = False

    def __getitem__(self, key, default=None):
        """Look up a configuration item"""
        return self.base.get_item(key, self.profile, default=default)

    def __setitem__(self, key, value):
        """Set a particular configuration item"""
        return self.base.set_item(key, value, self.profile)

    def get_profile(self):
        """Get our profile"""
        return self.profile

    def set_profile(self, profile, force=False):
        """Set our profile (which usually means change it)"""
        options = self.options_get()
        if not force and options and options.profile and profile == 'default':
            dbg('overriding default profile to %s' % options.profile)
            profile = options.profile
        dbg('Config::set_profile: Changing profile to %s' % profile)
        self.profile = profile
        if profile not in self.base.profiles:
            dbg('Config::set_profile: %s does not exist, creating' % profile)
            self.base.profiles[profile] = copy(DEFAULTS['profiles']['default'])

    def add_profile(self, profile):
        """Add a new profile"""
        return self.base.add_profile(profile)

    def del_profile(self, profile):
        """Delete a profile"""
        if profile == self.profile:
            # FIXME: We should solve this problem by updating terminals when we
            # remove a profile
            err('Config::del_profile: Deleting in-use profile %s.' % profile)
            self.set_profile('default')
        if profile in self.base.profiles:
            del(self.base.profiles[profile])
        options = self.options_get()
        if options and options.profile == profile:
            options.profile = None
            self.options_set(options)

    def rename_profile(self, profile, newname):
        """Rename a profile"""
        if profile in self.base.profiles:
            self.base.profiles[newname] = self.base.profiles[profile]
            del(self.base.profiles[profile])
            if profile == self.profile:
                self.profile = newname

    def list_profiles(self):
        """List all configured profiles"""
        return self.base.profiles.keys()

    def add_layout(self, name, layout):
        """Add a new layout"""
        return self.base.add_layout(name, layout)

    def replace_layout(self, name, layout):
        """Replace an existing layout"""
        return self.base.replace_layout(name, layout)

    def del_layout(self, layout):
        """Delete a layout"""
        if layout in self.base.layouts:
            del(self.base.layouts[layout])

    def rename_layout(self, layout, newname):
        """Rename a layout"""
        if layout in self.base.layouts:
            self.base.layouts[newname] = self.base.layouts[layout]
            del(self.base.layouts[layout])

    def list_layouts(self):
        """List all configured layouts"""
        return self.base.layouts.keys()

    def get_system_prop_font(self):
        """Look up the system font"""
        if self.system_prop_font is not None:
            return self.system_prop_font

    def get_system_mono_font(self):
        """Look up the system font"""
        if self.system_mono_font is not None:
            return self.system_mono_font

    def get_system_focus(self):
        """Look up the system focus setting"""
        if self.system_focus is not None:
            return self.system_focus

    def save(self):
        """Cause ConfigBase to save our config to file"""
        if self.inhibited is True:
            return True
        else:
            return self.base.save()

    def inhibit_save(self):
        """Prevent calls to save() being honoured"""
        self.inhibited = True

    def uninhibit_save(self):
        """Allow calls to save() to be honoured"""
        self.inhibited = False

    def options_set(self, options):
        """Set the command line options"""
        self.base.command_line_options = options

    def options_get(self):
        """Get the command line options"""
        return self.base.command_line_options

    def plugin_get(self, pluginname, key, default=None):
        """Get a plugin config value, if doesn't exist
            return default if specified
        """
        return self.base.get_item(key, plugin=pluginname, default=default)

    def plugin_set(self, pluginname, key, value):
        """Set a plugin config value"""
        return self.base.set_item(key, value, plugin=pluginname)

    def plugin_get_config(self, plugin):
        """Return a whole config tree for a given plugin"""
        return self.base.get_plugin(plugin)

    def plugin_set_config(self, plugin, tree):
        """Set a whole config tree for a given plugin"""
        return self.base.set_plugin(plugin, tree)

    def plugin_del_config(self, plugin):
        """Delete a whole config tree for a given plugin"""
        return self.base.del_plugin(plugin)

    def layout_get_config(self, layout):
        """Return a layout"""
        return self.base.get_layout(layout)

    def layout_set_config(self, layout, tree):
        """Set a layout"""
        return self.base.set_layout(layout, tree)

class ConfigBase(Borg):
    """Class to provide access to our user configuration"""
    loaded = None
    whined = None
    sections = None
    global_config = None
    profiles = None
    keybindings = None
    plugins = None
    layouts = None
    command_line_options = None
    config_filename = None

    def __init__(self):
        """Class initialiser"""

        Borg.__init__(self, self.__class__.__name__)

        self.prepare_attributes()
        self.command_line_options = optionparse.options
        self.load()

    def prepare_attributes(self):
        """Set up our borg environment"""
        if self.loaded is None:
            self.loaded = False
        if self.whined is None:
            self.whined = False
        if self.sections is None:
            self.sections = ['global_config', 'keybindings', 'profiles',
                             'layouts', 'plugins']
        if self.global_config is None:
            self.global_config = copy(DEFAULTS['global_config'])
        if self.profiles is None:
            self.profiles = {}
            self.profiles['default'] = copy(DEFAULTS['profiles']['default'])
        if self.keybindings is None:
            self.keybindings = copy(DEFAULTS['keybindings'])
        if self.plugins is None:
            self.plugins = {}
        if self.layouts is None:
            self.layouts = {}
            for layout in DEFAULTS['layouts']:
                self.layouts[layout] = copy(DEFAULTS['layouts'][layout])

    def get_default_config(self,defaultconfig={}):
        """Convert our tree of default values into a ConfigObj validation
        specification"""

        defaultconfig['global_config']={}
        defaultconfig['global_config'].update(DEFAULTS['global_config'])

        defaultconfig['keybindings']={}
        defaultconfig['keybindings'].update(DEFAULTS['keybindings'].items())

        defaultconfig['profiles']={}
        defaultconfig['profiles'].update(DEFAULTS['profiles'])

        defaultconfig['layouts']={}
        defaultconfig['layouts'].update(DEFAULTS['layouts'])

        defaultconfig['plugins']={}

        if DEBUG == True:
            with open(os.path.join(os.environ.get('TMPDIR','/tmp'),
                                   'terminator_configspec_debug.txt'),
                      mode='wt') as f:
                json.dump(defaultconfig,f,
                          indent=4,separators=(',', ':'),sort_keys=True)

    def load(self):
        """Load configuration data from our various sources"""
        if self.loaded is True:
            dbg('ConfigBase::load: config already loaded')
            return

        self.config_filename=self.command_line_options.config or os.path.join(get_config_dir(), 'config.json')

        dbg('load config file: %s' % self.config_filename)

        configdata={}
        self.get_default_config(configdata)
        try:
            with open(self.config_filename,mode='rt') as f:
                configdata.update(json.load(f))
        except FileNotFoundError as ex:
            err('ConfigBase::load: Unable to load %s (%s)' % (self.config_filename, ex))

        for section_name in self.sections:
            section=getattr(self,section_name)
            section.update(configdata.get(section_name,()))

            #set default profile options
            if section_name=='profiles':
                for profile in section.values():
                    for k,v in DEFAULTS['profiles']['default'].items():
                        if k not in profile:
                            profile[k]=v

            #set default layout options
            if section_name=='layouts':
                for layouts in section.values():
                    for k,v in DEFAULTS['layouts']['default'].items():
                        if k not in layouts:
                            profile[k]=v

        self.loaded = True

    def reload(self):
        """Force a reload of the base config"""
        self.loaded = False
        self.load()
        
    def save(self):
        """Save the config to a file"""
        dbg('ConfigBase::save: saving config')

        configdata={}
        for section_name in self.sections:
            configdata[section_name]=getattr(self,section_name)

        config_dir=os.path.dirname(self.config_filename)
        os.makedirs(config_dir,exist_ok=True)
        try:
            with open(self.config_filename,mode='wt') as f:
                json.dump(configdata,f,
                          indent=4,separators=(',', ':'),sort_keys=True)
        except Exception as ex:
            err('ConfigBase::save: Unable to save config: %s' % ex)

    def get_item(self, key, profile='default', plugin=None, default=None):
        """Look up a configuration item"""
        if profile not in self.profiles:
            # Hitting this generally implies a bug
            profile = 'default'

        if key in self.global_config:
            dbg('ConfigBase::get_item: %s found in globals: %s' %
                    (key, self.global_config[key]))
            return self.global_config[key]
        elif key in self.profiles[profile]:
            dbg('ConfigBase::get_item: %s found in profile %s: %s' % (
                    key, profile, self.profiles[profile][key]))
            return self.profiles[profile][key]
        elif key == 'keybindings':
            return self.keybindings
        elif plugin and plugin in self.plugins and key in self.plugins[plugin]:
            dbg('ConfigBase::get_item: %s found in plugin %s: %s' % (
                    key, plugin, self.plugins[plugin][key]))
            return self.plugins[plugin][key]
        elif default:
            return default
        else:
            raise KeyError('ConfigBase::get_item: unknown key %s' % key)

    def set_item(self, key, value, profile='default', plugin=None):
        """Set a configuration item"""
        dbg('ConfigBase::set_item: Setting %s=%s (profile=%s, plugin=%s)' %
                (key, value, profile, plugin))

        if key in self.global_config:
            self.global_config[key] = value
        elif key in self.profiles[profile]:
            self.profiles[profile][key] = value
        elif key == 'keybindings':
            self.keybindings = value
        elif plugin is not None:
            if plugin not in self.plugins:
                self.plugins[plugin] = {}
            self.plugins[plugin][key] = value
        else:
            raise KeyError('ConfigBase::set_item: unknown key %s' % key)

        return True

    def get_plugin(self, plugin):
        """Return a whole tree for a plugin"""
        if plugin in self.plugins:
            return self.plugins[plugin]

    def set_plugin(self, plugin, tree):
        """Set a whole tree for a plugin"""
        self.plugins[plugin] = tree

    def del_plugin(self, plugin):
        """Delete a whole tree for a plugin"""
        if plugin in self.plugins:
            del self.plugins[plugin]

    def add_profile(self, profile):
        """Add a new profile"""
        if profile in self.profiles:
            return False
        self.profiles[profile] = copy(DEFAULTS['profiles']['default'])
        return True

    def add_layout(self, name, layout):
        """Add a new layout"""
        if name in self.layouts:
            return False
        self.layouts[name] = layout
        return True

    def replace_layout(self, name, layout):
        """Replaces a layout with the given name"""
        if not name in self.layouts:
            return False
        self.layouts[name] = layout
        return True

    def get_layout(self, layout):
        """Return a layout"""
        if layout in self.layouts:
            return self.layouts[layout]
        else:
            err('layout does not exist: %s' % layout)

    def set_layout(self, layout, tree):
        """Set a layout"""
        self.layouts[layout] = tree

