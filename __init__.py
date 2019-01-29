import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_symbol_inserter.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

class Command:
    
    def __init__(self):

        global option_int
        global option_bool
        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):

        ini_write(fn_config, 'op', 'option_int', str(option_int))
        ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        file_open(fn_config)
        
    def run(self):
        s = '''
        file lines count: {cnt}
        option_int: {i}
        option_bool: {b}
        '''.format(
             cnt = ed.get_line_count(),
             i = option_int,
             b = option_bool,
             )
        msg_box(s, MB_OK)
        
    def create_menu(self):
        h=dlg_proc(0, DLG_CREATE)
        dlg_proc(h, DLG_PROP_SET, prop={      # creates an empty dialog
            'cap': 'main dlg',
            'x': 100,
            'y': 50,
            'w': 400,
            'h': 300,
            'w_min': 200,
            'h_min': 300,
            'border': DBORDER_SIZE,
            'topmost': True,
            })

     
        p=dlg_proc(h, DLG_CTL_ADD,'button')
        dlg_proc(h, DLG_PROP_SET, index=p, prop={
            'name' : 'list',
            'cap'  : 'sybol type',
            'x'    : 10,  
            'y'    : 30, 
            'w'    : 50,
            'tag'  : 'some_tag',
        })

        #nfocus = dlg_proc(h, DLG_CTL_FIND, 'edit1')
        #dlg_proc(h, DLG_CTL_FOCUS, index=nfocus)
        return h

    def show_menu(self):
        print('test_sidepanel')
        title = 'Side dialog'
        id_dlg = self.create_menu()
        icon_name = 'project.png'

        app_proc(PROC_SIDEPANEL_ADD_DIALOG, (title, id_dlg, icon_name) )
        app_proc(PROC_SIDEPANEL_ACTIVATE, title)
        
    def show_menu_tmp(self):
        print('showing menu')
