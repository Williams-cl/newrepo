from pywinauto.application import Application
from pykeyboard import PyKeyboard
from pathlib import Path
import win32gui,win32con,win32api,threading,time,random,pymysql
import pytest

def test_Ready_DataBase():
    #打开数据库连接  
    DB_Connect=pymysql.connect(host="",user="root",password="migrsoft",db="dxh_frontpos",port=13305)
    #使用cursor()方法获取操作游标cursor
    Cursor = DB_Connect.cursor()
    sql='update parameter set pvalue="http://pos.dianxiaohuo.top" where cname="服务器Url"'
    #使用execute()方法执行sql语句
    Cursor.execute(sql)
    #提交数据
    DB_Connect.commit()
    #显示修改结果
    Cursor.execute('select pvalue from parameter where cname="服务器Url"')
    data=Cursor.fetchall()
    print(data)
    #关闭游标和数据库链接
    Cursor.close()
    DB_Connect.close()
def test_Test_DataBase():
    #打开数据库连接  
    DB_Connect=pymysql.connect(host="",user="root",password="migrsoft",db="dxh_frontpos",port=13305)
    #使用cursor()方法获取操作游标cursor
    Cursor = DB_Connect.cursor()
    sql='update parameter set pvalue="http://pos.dxherp.net" where cname="服务器Url"'
    #使用execute()方法执行sql语句
    Cursor.execute(sql)
    #提交数据
    DB_Connect.commit()
    #显示修改结果
    Cursor.execute('select pvalue from parameter where cname="服务器Url"')
    data=Cursor.fetchall()
    print(data)
    #关闭游标和数据库链接
    Cursor.close()
    DB_Connect.close()
@pytest.mark.login_list(1)
def test_Next_Login():
    #启动程序
    app=Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    Dialog.wait('exists',timeout=30)
    Dialog.type_keys("{UP}")
    Dialog.type_keys("zzz")
    Dialog.type_keys("{DOWN}")
    Dialog.type_keys("111111")
    Dialog.type_keys("~")
#挂单10笔
@pytest.mark.login_list(2)
def test_Only_List():
    i=10
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    Dialog=app.window(title='云POS')
    #键盘操作
    input_pykeyword=PyKeyboard()
    while i!=0:
        i=i-1
        with open(r'C:\Users\drigon\Desktop\winpos自动化\winpos脚本\task2.0\TestData\dict.txt','r') as List:
            for list_number in List:
                input_pykeyword.type_string(list_number)
                Dialog.type_keys("~")
                time.sleep(random.uniform(0.1,0.5))
                Dialog.type_keys("~")
            List.close()
        time.sleep(random.uniform(1,2))
        win32api.keybd_event(65,0,0,0)
        win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0)
#关联会员
@pytest.mark.member_cash_pay(1)
@pytest.mark.member_card_pay(1)
@pytest.mark.member_savecent_pay(1)
def test_Relation_Member():
    #需要与其他def函数使用同种连接方式
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    #键盘操作
    input_pykeyword=PyKeyboard()
    Flag=1
    while Flag:
        try:
            #使用关联会员快捷键G
            win32api.keybd_event(71,0,0,0)
            win32api.keybd_event(71,0,win32con.KEYEVENTF_KEYUP,0)
            #判断关联会员窗口是否被关闭和可见，超时时间5s，超时后间隔3s再次重试
            Dialog.child_window(title="关联会员").wait('ready',timeout=5,retry_interval=3)
        except:
            print("关联会员出现延迟！！！")
            Dialog.child_window(title="关联会员").type_keys("{ESC}")
            continue
        else:
            Relation_Member=Dialog.child_window(title="关联会员")
            input_pykeyword.type_string('13000009997')
            time.sleep(random.uniform(1,2))
            #定位窗体，点击回车
            Relation_Member.type_keys("~")
            Flag=0
#录入商品
@pytest.mark.member_cash_pay(2)
@pytest.mark.member_card_pay(2)
@pytest.mark.member_savecent_pay(2)
@pytest.mark.save_pay(1)
@pytest.mark.entity_pay(1)
def test_Input_Goods():
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    Dialog=app.window(title='云POS')
    Dialog.type_keys("~")
    #键盘操作
    input_pykeyword=PyKeyboard()
    with open(r'C:\Users\drigon\Desktop\winpos自动化\winpos脚本\task2.0\dict.txt','r') as List:
        for list_number in List:
            input_pykeyword.type_string(list_number)
            Dialog.type_keys("~")
            time.sleep(random.uniform(0.1,0.5))
            Dialog.type_keys("~")
        List.close()
#现金支付
@pytest.mark.member_cash_pay(3)
def test_Cash_Pay():
    #需要与其他def函数使用同种连接方式
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    Flag=1
    while Flag:
        try:
            win32api.keybd_event(84,0,0,0)
            win32api.keybd_event(84,0,win32con.KEYEVENTF_KEYUP,0)
            Dialog.child_window(title="现金收款", control_type="Text").wait('exists',timeout=3,retry_interval=3)
        #现金收款界面异常则执行except
        except:
            print("现金收款界面疑似出现延迟！！！")
            log_object=open('D:\error.log','a')
            log_object.writelines(time.asctime(time.localtime(time.time())))
            log_object.writelines("现金收款界面疑似出现延迟！！！"+'\n')
            log_object.close()
            try:
                Pop_box=Dialog.child_window(title="正在计算促销,还不能结算")
                Pop_box.wait('exists',timeout=3)
            except:
                log_object=open('D:\error.log','a')
                log_object.writelines(time.asctime(time.localtime(time.time())))
                log_object.writelines("现金收款界面疑似出现延迟！！！"+'\n')
                log_object.close()
                continue
            else:
                Pop_box.type_keys("~")
                time.sleep(1)
        else:
            Pay=Dialog.child_window(title="现金收款", control_type="Text")
            Pay.type_keys("~")
            Flag=0
#会员余额支付
@pytest.mark.member_card_pay(3)
def test_Member_Card_Pay():
    #需要与其他def函数使用同种连接方式
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    Flag=1
    while Flag:
        try:
            #会员余额支付快捷键"Y"
            win32api.keybd_event(89,0,0,0)
            win32api.keybd_event(89,0,win32con.KEYEVENTF_KEYUP,0)
            Dialog.child_window(title="会员余额收款", control_type="Text").wait('exists',timeout=3,retry_interval=3)
        except:
            print("会员余额收款界面疑似出现延迟！！！")
            log_object=open('D:\error.log','a')
            log_object.writelines(time.asctime(time.localtime(time.time())))
            log_object.writelines("会员余额界面疑似出现延迟！！！"+'\n')
            log_object.close()
            try:
                Pop_box=Dialog.child_window(title="正在计算促销,还不能结算"+'\n')
                Pop_box.wait('exists',timeout=3)
            except:
                continue
            else:
                Pop_box.type_keys("~")
                time.sleep(1)
        else:
            Pay=Dialog.child_window(title="会员余额收款", control_type="Text")
            Pay.type_keys("~")
            Flag=0
#会员积分支付
@pytest.mark.member_savecent_pay(3)
def test_Member_Savecent_Pay():
    #需要与其他def函数使用同种连接方式
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    Flag=1
    while Flag:
        try:
            #会员积分支付快捷键"X"
            win32api.keybd_event(88,0,0,0)
            win32api.keybd_event(88,0,win32con.KEYEVENTF_KEYUP,0)
            Dialog.child_window(title="积分收款", control_type="Text").wait('exists',timeout=3,retry_interval=3)
            Pay=Dialog.child_window(title="积分收款", control_type="Text")
            Pay.type_keys("~")
            Dialog.child_window(title="等待顾客输入密码或扫手机动态码").wait('exists',timeout=3,retry_interval=2)
        except:
            print("会员积分支付界面疑似出现延迟！！！")
            log_object=open('D:\error.log','a')
            log_object.writelines(time.asctime(time.localtime(time.time())))
            log_object.writelines("会员积分收款界面疑似出现延迟！！！"+'\n')
            log_object.close()
            #操作alt+f4关闭积分支付界面，由于积分界面有两个所以推出两次
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(115,0,0,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(115,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(18,0,0,0)
            win32api.keybd_event(115,0,0,0)
            win32api.keybd_event(18,0,win32con.KEYEVENTF_KEYUP,0)
            win32api.keybd_event(115,0,win32con.KEYEVENTF_KEYUP,0)
            try:
                Pop_box=Dialog.child_window(title="正在计算促销,还不能结算"+'\n')
                Pop_box.wait('exists',timeout=3)
            except:
                continue
            else:
                Pop_box.type_keys("~")
                time.sleep(1)
        else:
            Save_Pay=Dialog.child_window(title="等待顾客输入密码或扫手机动态码")
            Save_Pay.type_keys("123456")
            Save_Pay.type_keys("~")
            Flag=0
#储值卡支付
@pytest.mark.save_pay(2)
def test_Save_Pay():
    #需要与其他def函数使用同种连接方式
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    Flag=1
    while Flag:
        try:
            #储值卡支付快捷键"X"
            win32api.keybd_event(35,0,0,0)
            win32api.keybd_event(35,0,win32con.KEYEVENTF_KEYUP,0)
            time.sleep(2)
            Dialog.child_window(title="储值卡收款", control_type="Text").wait('exists',timeout=3,retry_interval=3)
            Pay=Dialog.child_window(title="储值卡收款", control_type="Text")
            #储值卡账号输入
            Pay.type_keys("10000")
            Pay.type_keys("~")
            time.sleep(2)
            Pay.type_keys("~")
            #储值卡支付密码弹出窗体
            Save_Dialog=Dialog.child_window(title="等待顾客输入密码或扫手机动态码", control_type="Text")
            Save_Dialog.wait('ready',timeout=3,retry_interval=3)
            Save_Dialog.type_keys("~")
            #储值卡密码输入
            Save_Dialog.type_keys("123456")
        except:
            print("储值卡支付界面疑似出现延迟！！！")
            Save_Dialog.type_keys("{ESC}")
            Pay.type_keys("{ESC}")
            log_object=open('D:\error.log','a')
            log_object.writelines(time.asctime(time.localtime(time.time())))
            log_object.writelines("储值卡收款界面疑似出现延迟！！！"+'\n')
            log_object.close()
            try:
                #如果出现大批量促销商品，会触发该保护策略
                Pop_box=Dialog.child_window(title="正在计算促销,还不能结算"+'\n')
                Pop_box.wait('exists',timeout=3)
            except:
                continue
            else:
                Pop_box.type_keys("~")
                time.sleep(1)
        else:
            Save_Dialog.type_keys("~")
            Flag=0
#实体优惠券支付
@pytest.mark.entity_pay(2)
def test_Entity_Pay():
    #需要与其他def函数使用同种连接方式
    Application(backend="uia").start(r"H:\POSsystem\qxsaas.exe")
    app=Application(backend="uia").connect(path=r"H:\POSsystem\qxsaas.exe")
    #判断窗体是否形成句柄
    Dialog=app.window(title='云POS')
    #将文件路径使用Path函数增添到某个变量中
    p=Path(r'C:\Users\drigon\Desktop\winpos自动化\winpos脚本\task2.0\TestData\entity_coupons.txt')
    #使用Path方式打开优惠券字典表
    with p.open() as f:
        #将p目录下的文件按行全部读取到ss中形成列表
        ss=f.readlines()
        #将列表中字符串按个取出
        for line in ss:
            try:
                #实体券支付快捷键"Z"
                win32api.keybd_event(90,0,0,0)
                win32api.keybd_event(90,0,win32con.KEYEVENTF_KEYUP,0)
                #优惠券收款窗体等待
                Dialog.child_window(title="优惠券收款", control_type="Text").wait('exists',timeout=3,retry_interval=3)
                Pay=Dialog.child_window(title="优惠券收款", control_type="Text")
                #输入优惠券号
                Pay.type_keys(line)
                #进行优惠券支付操作
                Pay.type_keys("~")
                time.sleep(2)
                Pay.type_keys("~")
            except:
                print("实体券支付界面出现异常！！！")
                log_object=open('D:\error.log','a')
                log_object.writelines(time.asctime(time.localtime(time.time())))
                log_object.writelines("现金收款界面疑似出现延迟！！！"+'\n')
                log_object.close()
            else:
                #由于每次都读取字典表中第一行,所以删除读取到优惠券字典表中的第一行数据即可
                ss=ss[:0]+ss[1:]
                p.write_text(''.join(ss))
                #关闭优惠券字典表
                f.close()
            break