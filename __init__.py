import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_snippet_panel.ini')

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
        global outlist
        dlg_proc(id_dlg,DLG_CTL_PROP_SET, name='listout', prop={
                  'items' : '\t'.join(syms2),
            })
        
    def get_symbols_of_type(self,symbol_type):
        global clips_folder
        f=open(clips_folder+symbol_type+os.sep+'List.txt','r', encoding='utf-16')
        files_list=os.listdir(clips_folder+symbol_type)
        files_list=[i for i in files_list if i.endswith('.txt')]
        retarr=[]
        for i in files_list:
            f=open(clips_folder+symbol_type+os.sep+i,'r', encoding='utf-16')
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
        
    def set_items(self,h,lst,items):
        s=''
        for num,value in enumerate(items):
            if num>0:
                s+='\t'
            s+=value
            dlg_proc(h,DLG_CTL_PROP_SET, index=lst, prop={
                  'items' : s,
            })
    def config(self):
        file_open(fn_config)
    
    def create_menu(self):
        global headers
        global clips_folder
        headers = os.listdir(clips_folder)
        heads=[]    
        h=dlg_proc(0, DLG_CREATE)
        global dropdown, outlist
        dropdown=dlg_proc(h, DLG_CTL_ADD,'combo_ro')
        dlg_proc(h, DLG_CTL_PROP_SET, index=dropdown, prop={
            'name'             : 'listdrop',
            'align'            : ALIGN_TOP,
            'items'            : 'a\tb\tc',
            'act'              : True,
            'on_change'        : self.callback_combo_change2,#callback_combo_change2',
        })
        global outlist
        outlist=dlg_proc(h, DLG_CTL_ADD,'listbox')
        dlg_proc(h, DLG_CTL_PROP_SET, index=outlist, prop={
            'name'          : 'listout',
            'align'         : ALIGN_CLIENT,
            'items'         : 'ku\tka\tre\tku',
            'on_click_dbl'  : 'cuda_snippet_panel.insert_symbol',
        })
        global real_elements
        self.set_items(h,dropdown,headers)
        self.set_items(h,outlist,self.get_symbols_of_type(headers[0]))
        real_elements=self.get_symbols_of_type(headers[0])
        return h

    def show_menu(self):
        title = 'Insert symbols'
        id_dlg = self.create_menu()
        icon_name = 'project.png'
        app_proc(PROC_SIDEPANEL_ADD_DIALOG, (title, id_dlg, icon_name) )
        app_proc(PROC_SIDEPANEL_ACTIVATE, title)
