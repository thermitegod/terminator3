from os.path import exists
from argparse import ArgumentParser
import json

from configobj.configobj import ConfigObj, flatten_errors
from configobj.validate import Validator

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

def defaults_to_configspec():
    """Convert our tree of default values into a ConfigObj validation
        specification"""
    configspecdata = {}

    keymap = {
        'int': 'integer',
        'str': 'string',
        'bool': 'boolean',
    }

    section = {}
    for key in DEFAULTS['global_config']:
        keytype = DEFAULTS['global_config'][key].__class__.__name__
        value = DEFAULTS['global_config'][key]
        if keytype in keymap:
            keytype = keymap[keytype]
        elif keytype == 'list':
            value = 'list(%s)' % ','.join(value)

        keytype = '%s(default=%s)' % (keytype, value)

        if key == 'custom_url_handler':
            keytype = 'string(default="")'

        section[key] = keytype
    configspecdata['global_config'] = section

    section = {}
    for key in DEFAULTS['keybindings']:
        value = DEFAULTS['keybindings'][key]
        if value is None or value == '':
            continue
        section[key] = 'string(default=%s)' % value
    configspecdata['keybindings'] = section

    section = {}
    for key in DEFAULTS['profiles']['default']:
        keytype = DEFAULTS['profiles']['default'][key].__class__.__name__
        value = DEFAULTS['profiles']['default'][key]
        if keytype in keymap:
            keytype = keymap[keytype]
        elif keytype == 'list':
            value = 'list(%s)' % ','.join(value)
        if keytype == 'string':
            value = '"%s"' % value

        keytype = '%s(default=%s)' % (keytype, value)

        section[key] = keytype
    configspecdata['profiles'] = {}
    configspecdata['profiles']['__many__'] = section

    section = {}
    section['type'] = 'string'
    section['parent'] = 'string'
    section['profile'] = 'string(default=default)'
    section['command'] = 'string(default="")'
    section['position'] = 'string(default="")'
    section['size'] = 'list(default=list(-1,-1))'
    configspecdata['layouts'] = {}
    configspecdata['layouts']['__many__'] = {}
    configspecdata['layouts']['__many__']['__many__'] = section

    configspecdata['plugins'] = {}

    configspec = ConfigObj(configspecdata)
    return configspec

def main():
    parser=ArgumentParser()
    parser.add_argument('-i',dest='src',default=None,
                        action='store',type=str,required=True,
                        help='input file')
    parser.add_argument('-o',dest='dst',default=None,
                        action='store',type=str,required=True,
                        help='output file')
    ns=parser.parse_args()

    if exists(ns.dst):
        return print('{} already exists, do nothing.'.format(ns.dst))

    with open(ns.src,mode='rt') as f:
        configdata=ConfigObj(f,configspec=defaults_to_configspec())

    validator=Validator()
    configdata.validate(validator,preserve_errors=True)
    for k,v in configdata['keybindings'].items():
        if v=='None':
            configdata['keybindings'][k]=''

    with open(ns.dst,mode='wt') as f:
        json.dump(configdata,f,indent=4,separators=(',', ':'),sort_keys=True)
    return print('convert {} to {}'.format(ns.src,ns.dst))

if __name__=='__main__':
    main()
