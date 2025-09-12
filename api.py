import webview
import core

class API:
    def __init__(self):
        self.maximized = False

    def close_window(self):
        webview.windows[0].destroy()

    def minimize_window(self):        
        webview.windows[0].minimize()

    def restore_window(self):
        if not self.maximized:
            webview.windows[0].maximize()
            self.maximized = True
        else:            
            webview.windows[0].restore()
            self.maximized = False

    def abrir_pasta(self):
        return webview.windows[0].create_file_dialog(
            webview.FOLDER_DIALOG,            
        )
    
    def pesquisa_simples(self, pasta):
        pesquisa = core.FileSearch(pasta)
        pesquisa.run()
        arquivos = pesquisa.get_results(to_dict = True)
        return arquivos
    
    def log(self, msg):
        print(msg)
    
    def apply_filter(self, dir, filters):
        pesquisa = core.FileSearch(dir, **filters)
        pesquisa.run()
        arquivos = pesquisa.get_results(to_dict = True)
        return arquivos
    
    def files_from_dict(self, filelist):
        instanced_files = []

        for file in filelist:
            instanced_files.append(core.Arquivo(file["path"]))
        
        return core.FileGroup(instanced_files)

    def move_all(self, filelist, destination):
        files = self.files_from_dict(filelist)

        files.mover_todos(destination)

    def copy_all(self, filelist, destination):
        files = self.files_from_dict(filelist)

        files.copiar_todos(destination)

    def delete_all(self, filelist):
        files = self.files_from_dict(filelist)

        files.excluir_todos()


