import os,time,random
os.chdir('../../')
os.chdir('TestCase/shangchaoban')
while True:
    i=random.randint(1,10)
    #关联会员现金支付
    if i<3:
        if os.path.exists("test_pay"):
            time.sleep(5)
        else:
            os.system('pytest test_pay.py -m member_cash_pay -s --alluredir ./report')
    #关联会员余额支付
    elif 2<i<5:
        if os.path.exists("test_pay"):
            time.sleep(5)
        else:
            os.system('pytest test_pay.py -m member_card_pay -s --alluredir ./report')
    #储值卡支付
    elif 4<i<8:
        if os.path.exists("test_pay"):
            time.sleep(5)
        else:
            os.system('pytest test_pay.py -m save_pay -s --alluredir ./report')
    #储值卡支付
    else:
        if os.path.exists("test_pay"):
            time.sleep(5)
        else:
            os.system('pytest test_pay.py -m entity_pay -s --alluredir ./report')
'''该功能存在积分卡问题，修复中
    #关联会员积分支付
    elif :
        if os.path.exists("test_pay"):
            time.sleep(5)
        else:
            os.system('pytest test_pay.py -m member_savecent_pay -s --alluredir ./report')
'''