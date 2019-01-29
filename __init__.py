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
        clips_folder='py/cuda_symbol_inserter/clips/'
        headers = os.listdir(clips_folder)
        def get_symbols_of_type(symbol_type):
            #os.chdir(symbol_type)
            f=open(clips_folder+symbol_type+'/List.txt','r', encoding='utf-16')
            #f.read()
            #os.chdir('..')
            return f.readlines()
        
        #print(get_symbols_of_type(headers[0]))
            
        h=dlg_proc(0, DLG_CREATE)
            
        def show_list_by_num(data):
            print('abc')
            pass    
            
        dropdown=dlg_proc(h, DLG_CTL_ADD,'combo_ro')
        dlg_proc(h, DLG_CTL_PROP_SET, index=dropdown, prop={
            'name'             : 'list',
            'align'            : ALIGN_TOP,
            'items'            : 'a\tb\tc',
            'val'              : 2,
            'on_change'        : show_list_by_num,
        })
        
        outlist=dlg_proc(h, DLG_CTL_ADD,'listbox')
        dlg_proc(h, DLG_CTL_PROP_SET, index=outlist, prop={
            'name'   : 'list',
            'align'  : ALIGN_CLIENT,
            'items'  : 'ku\tka\tre\tku'
        })
        
        def set_items(h,lst,items):
            s=''
            for num,value in enumerate(items):
                if num>0:
                    s+='\t'
                s+=value
            dlg_proc(h,DLG_CTL_PROP_SET, index=lst, prop={
                'items' : s,
                'on_change':show_list_by_num,
            })
        set_items(h,dropdown,headers)
        set_items(h,outlist,get_symbols_of_type(headers[0]))
        return h

    def show_menu(self):
        print('test_sidepanel')
        title = 'Insert symbols'
        id_dlg = self.create_menu()
        icon_name = 'project.png'

        app_proc(PROC_SIDEPANEL_ADD_DIALOG, (title, id_dlg, icon_name) )
        app_proc(PROC_SIDEPANEL_ACTIVATE, title)
        
    def show_menu_tmp(self):
        print('showing menu')
