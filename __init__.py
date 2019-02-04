import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_snippet_panel.ini')
fn_icon = os.path.join(os.path.dirname(__file__), 'snip.png')

dir_py = app_path(APP_DIR_PY)
clips_folder=dir_py+os.sep+'cuda_snippet_panel'+os.sep+'clips'+os.sep

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

            
class Command:
    def callback_combo_change2(self, id_dlg, id_ctl, data='', info=''):  #really working on_dropdown_change
        p = dlg_proc(id_dlg, DLG_CTL_PROP_GET, name='listdrop')
        num = int(p['val'])
        heads=headers[num]
        syms=self.get_symbols_of_type(heads)
        syms2=[]
        for i in syms:
            syms2.append(i.split('=')[0] if '=' in i else i)
        dlg_proc(id_dlg,DLG_CTL_PROP_SET, name='listout', prop={
                  'items' : '\t'.join(syms2),
            })
        
    def get_symbols_of_type(self,symbol_type):
        global clips_folder
        files_list=os.listdir(clips_folder+symbol_type)
        files_list=[i for i in files_list if i.endswith('.txt')]
        retarr=[]
        fname = clips_folder+symbol_type+os.sep+i
        for i in files_list:
            try:
                f=open(fname ,'r', encoding='utf-16')
                for j in f.readlines():
                    retarr.append(j)
            except:
                f=open(fname, 'r', encoding='utf-8')
                for j in f.readlines():
                    retarr.append(j)
        return retarr
        return f.readlines() 
        
    def insert_symbol(self, id_dlg, id_ctl, data='', info=''):
        num=int(dlg_proc(h, DLG_CTL_PROP_GET, name='listout')['val'])
        global heads
        val=dlg_proc(h, DLG_CTL_PROP_GET, index=dropdown)
        global real_elements
        x,y,a,a=ed.get_carets()[0]
        i=real_elements[num]
        ed.insert(x,y,i.split('=')[1] if '=' in i else i)
        
    def __init__(self):
        global real_elements
        real_elements=[]
        global h
        h=self.create_menu()
        
    def set_items(self,h,name,items):
        dlg_proc(h,DLG_CTL_PROP_SET, name=name, prop={
              'items' : '\t'.join(items),
        })

    def config(self):
        file_open(fn_config)
    
    def create_menu(self):
        global headers
        global clips_folder
        headers = os.listdir(clips_folder)
        heads=[]    
        h=dlg_proc(0, DLG_CREATE)
        n=dlg_proc(h, DLG_CTL_ADD,'combo_ro')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name'             : 'listdrop',
            'align'            : ALIGN_TOP,
            'items'            : 'a\tb\tc',
            'act'              : True,
            'on_change'        : self.callback_combo_change2,#callback_combo_change2',
        })
        n=dlg_proc(h, DLG_CTL_ADD,'listbox')
        dlg_proc(h, DLG_CTL_PROP_SET, index=n, prop={
            'name'          : 'listout',
            'align'         : ALIGN_CLIENT,
            'items'         : 'ku\tka\tre\tku',
            'on_click_dbl'  : 'cuda_snippet_panel.insert_symbol',
        })
        # set height of list item
        #h_listbox = dlg_proc(h, DLG_CTL_HANDLE, name='listout')
        #listbox_proc(h_listbox, LISTBOX_SET_ITEM_H, index=18)
        global real_elements
        self.set_items(h,'listdrop',headers)
        self.set_items(h,'listout',self.get_symbols_of_type(headers[0]))
        real_elements=self.get_symbols_of_type(headers[0])
        return h

    def show_menu():
        id_dlg = self.create_menu()
        app_proc(PROC_SIDEPANEL_ADD_DIALOG, ('Snippet Panel', id_dlg, fn_icon) )
        app_proc(PROC_SIDEPANEL_ACTIVATE, title)
