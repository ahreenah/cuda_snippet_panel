import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_symbol_inserter.ini')

option_int = 100
option_bool = True

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

            
class Command:
    def callback_combo_change2(self, id_dlg, id_ctl, data='', info=''):  #really working on_dropdown_change
        p = dlg_proc(id_dlg, DLG_CTL_PROP_GET, name='listdrop')
        num = int(p['val'])
        #print(index)
        #syms=self.get_symbols_of_type(int(index))
        #global heads
        #global headers
        heads=headers[num]
        print(heads)
        syms=self.get_symbols_of_type(heads)
        print(syms)
        global outlist
        dlg_proc(h,DLG_CTL_PROP_SET, index=outlist, prop={
                  'items' : '1\t2\t3'],
                  #'on_change':show_list_by_num,
            })#self.set_items(h,outlist,syms )
        print (num)
        #global real_elements
        #
        #real_elements=self.get_symbols_of_type(heads)
        #self.set_items(h,outlist,self.get_symbols_of_type(heads) )
        
    def get_symbols_of_type(self,symbol_type):
        clips_folder='py/cuda_symbol_inserter/clips/'
        f=open(clips_folder+symbol_type+'/List.txt','r', encoding='utf-16')
        return f.readlines() 
    def show_list_by_num(self, id_dlg, id_ctl, data='', info=''):
        global dropdown, outlist
        print(dlg_proc(h, DLG_PROP_GET, index=dropdown, name='listdrop'))
        num=int(dlg_proc(h, DLG_CTL_PROP_GET, index=dropdown)['val'])
        print('now num is: '+str(num))
        global heads
        global headers
        heads=headers[num]
        print (num)
        global real_elements
        
        real_elements=self.get_symbols_of_type(heads)
        self.set_items(h,outlist,self.get_symbols_of_type(heads) )
        pass    
           
    def insert_symbol(self, id_dlg, id_ctl, data='', info=''):
        num=int(dlg_proc(h, DLG_CTL_PROP_GET, index=outlist)['val'])
        global heads
        val=dlg_proc(h, DLG_CTL_PROP_GET, index=dropdown)
        print('inserting... '+str(num))
        global real_elements
        print(str(real_elements[num]))
        x,y,a,a=ed.get_carets()[0]
        ed.insert(x,y,real_elements[num][0])
        #print(heads)
        #print('tmp: '+str(dlg_proc(h,LOG_GET_LINES_LIST,index=outlist)))
        pass    
    def __init__(self):
        global real_elements
        real_elements=[]
        global option_int
        global option_bool
        global h
        h=self.create_menu()
        option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))
    def set_items(self,h,lst,items):
        s=''
        for num,value in enumerate(items):
            if num>0:
                s+='\t'
            s+=value
            dlg_proc(h,DLG_CTL_PROP_SET, index=lst, prop={
                  'items' : s,
                  #'on_change':show_list_by_num,
            })
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
        global headers
        headers = os.listdir(clips_folder)
        heads=[]    
        h=dlg_proc(0, DLG_CREATE)
            
        global dropdown, outlist
            
        dropdown=dlg_proc(h, DLG_CTL_ADD,'combo_ro')
        dlg_proc(h, DLG_CTL_PROP_SET, index=dropdown, prop={
            'name'             : 'listdrop',
            'align'            : ALIGN_TOP,
            'items'            : 'a\tb\tc',
            #'val'              : 2,
            'act'              : True,
            #'on_click'         : 'cuda_symbol_inserter.show_list_by_num',
            'on_change'        : self.callback_combo_change2,#callback_combo_change2',
        })
        global outlist
        outlist=dlg_proc(h, DLG_CTL_ADD,'listbox')
        dlg_proc(h, DLG_CTL_PROP_SET, index=outlist, prop={
            'name'          : 'listout',
            'align'         : ALIGN_CLIENT,
            'items'         : 'ku\tka\tre\tku',
            'on_click_dbl'  : 'cuda_symbol_inserter.insert_symbol',
        })
        

        
        global real_elements

        self.set_items(h,dropdown,headers)
        self.set_items(h,outlist,self.get_symbols_of_type(headers[0]))
        real_elements=self.get_symbols_of_type(headers[0])
        print('re: '+str(real_elements))
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
