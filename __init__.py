from pathlib import Path
from cudatext import *
import os, requests, re

class Command:

    def __init__(self):
        pass
    
    def _open_wiki(self, prefer_local_wiki=True):
        dir = Path(app_path(APP_DIR_PY))
        fn = str(dir / __name__ / 'cudatext_api.wiki')
        
        if prefer_local_wiki and os.path.isfile(fn):
            file_open(fn)
        else:
            self.open_from_github()
            
    def fetch_wiki_text_from_github(self):
        url = 'https://raw.githubusercontent.com/Alexey-T/CudaText/master/app/readme/wiki/cudatext_api.wiki'
        response = requests.get(url)
        
        page_text = None
        if response.status_code == 200:
            page_text = response.text
        else:
            print(f'NOTE: {__name__}: Failed to retrieve page. Status code: {response.status_code}')
        return page_text
    
    def set_editor_text(self, text):
        ed.set_text_all(text)
        ed.set_prop(PROP_MODIFIED, False)
        ed.set_prop(PROP_TAB_TITLE, 'CudaText API wiki')
        ed.set_prop(PROP_LEXER_FILE, 'WikidPad')
    
    def open_from_github(self):
        page_text = self.fetch_wiki_text_from_github()

        if page_text is not None:
            file_open('')
            self.set_editor_text(page_text)
        
    def _cmd_jump_to_section(self, prefer_local_wiki=True):
        dir = Path(app_path(APP_DIR_PY))
        fn = str(dir / __name__ / 'cudatext_api.wiki')
        
        page_text = None
        if prefer_local_wiki and os.path.isfile(fn):
            local = True
            dir = Path(app_path(APP_DIR_PY))
            with open(dir / __name__ / 'cudatext_api.wiki') as f:
                page_text = f.read()
        else:
            local = False
            page_text = self.fetch_wiki_text_from_github()
            
        if page_text is None:
            return
            
        items = []
        for line in page_text.splitlines():
            pattern = r'^=+[^=]+=+$'
            matches = re.findall(pattern, line)
            if matches:
                items.append(line) 
        if not items:
            return
            
        res = dlg_menu(DMENU_LIST, items)
        if res is not None:
            if local:
                file_open(fn)
            else:
                file_open('')
                self.set_editor_text(page_text)
            pos = ed.action(EDACTION_FIND_ONE, '^{}$'.format(items[res]), 'r')
            if pos:
                def sub(*args, **kwargs):
                    ed.set_caret(*pos[:2])
                timer_proc(TIMER_START_ONE, sub, 50)

    def cmd_open_wiki(self):
        self._open_wiki(prefer_local_wiki=True)
    
    def cmd_jump_to_section(self):
        self._cmd_jump_to_section(prefer_local_wiki=True)

