import webview
from api import API

if __name__ == '__main__':
    api = API()

    window = webview.create_window (
        '>>cbjk_auto_file_organizer//',
        './interface/index.html', 
        width = 1000,
        height = 730,
        resizable = True,
        js_api = api,
        frameless = True,
    )

    webview.start(gui="edgechromium", debug=True)