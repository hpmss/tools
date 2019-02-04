import sys
from pywinauto import application


if len(sys.argv) < 2:
    print("Input a youtube video name")
    sys.exit()

app = application.Application().start(r'C:\Users\lifkid-pc\AppData\Local\CocCoc\Browser\Application\browser.exe youtube.com')
app.window(title_re=".* Cốc Cốc").type_keys('%D')
