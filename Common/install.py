from pywinauto.application import Application
import os
import win32gui,time
dir="H:\云pos安装包"
#root 所指的是当前正在遍历的这个文件夹的本身的地址等价于dir,dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录),files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)
for root,dirs,files in os.walk(dir):
    for file in files:
       print(os.path.join(root,file))
    real_path=input("请输入文件路径：")
    app = Application().start(real_path)
    window_title='安装 云POS'
    window_class='WixStdBA'
    ss=win32gui.FindWindow(window_class, window_title)
    app = Application().connect(handle=ss)
    dlg_spec=app.window(title='安装 云POS')
    dlg_spec.window(title='选择项').Click()
    dlg_spec.window(class_name='Edit').Click()
    dlg_spec.type_keys('H:\POSsystem')
    time.sleep(2)
    dlg_spec.window(title='确定').Click()
    dlg_spec.window(title='我同意许可条款和条件').Click()
    dlg_spec.window(title='安装').Click()
    dlg_spec.window(title='关闭').wait('ready',timeout=90)
    dlg_spec.window(title='关闭').Click()