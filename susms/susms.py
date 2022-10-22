from operator import truediv
import pywebio.input
from pywebio.input import *
from pywebio.output import *
from pywebio import *
from pywebio.session import *
from pywebio.pin import *
import pywebio.platform
import random
import time
deploy = "MICROTECH_USER"
admin_password = "admin"
class GetError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
def index():
    put_markdown(f"## 欢迎使用速推[SUSMS] 隐私短信验证平台[OEM VERSION FOR CHINA]，速推为以下用户授权提供副本：{deploy}")
    put_link("点我注册速推用户", app='register')
def register():
    put_button("点此注册速推", onclick=lambda: getuser(), color='success', outline=True)
    put_link("速推消息控制台", app='smsconsole')
def getuser():
    sunumber = random.randint(1000000000, 9999999999)
    savenum = open(f"sms/{sunumber}.user", "w")
    #savenum.write(str(sunumber))
    put_success(f"注册成功！您的速推号是:{sunumber}，请保管好您的速推号，不要泄露给他人")
def smsconsole():
    put_markdown(f"## 欢迎使用速推消息控制台[Authorize: {deploy} OEM]")
    sunumber = pywebio.input.input("请输入您的速推号：")
    try:
        sms = open(f"sms/{sunumber}.user", "r")
        put_button("清空消息列表", onclick=lambda: [sms.write(""),toast("清空消息列表成功！")], color='warning', outline=True)
        put_markdown(f"""
## 速推消息列表：
您的可读消息：
____________________________________________________
{sms.read()}
____________________________________________________
        """)
        while True:
            userinput = input_group("发送其他消息给其他速推号【严禁垃圾信息！】",[
            pywebio.input.input('请输入您要发送的速推号：', name='number'),
            pywebio.input.input('请输入您要发送的内容：', name='password', type=NUMBER)])   
            sendnumber = userinput['number']
            sendcontent = userinput['content']
            writesms = open(f"sms/{sendnumber}.user", "a+")
            writesms.write(sendcontent)
            writesms.write('\n')
    except:
        put_error(f"系统找不到此用户或此用户没有任何消息\nDebug INFO:{sendnumber}.user")
def loginerror():
    try:
        raise GetError("Disconnect from server")
    except:
        put_error("用户名或密码或Google Authenticator（仅设定）错误！三秒跳转主页，请重试！")
        time.sleep(3)
        put_link("重试", './premiumpanel')   
        go_app('#', new_window=False)
# 定义函数
def listusers(rootdir):
    import os
    _files = []
	# 列出文件夹下所有的目录与文件
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
		# 构造路径
        path = os.path.join(rootdir, list[i])
		# 判断路径是否为文件目录或者文件
		# 如果是目录则继续递归
        if os.path.isdir(path):
            _files.extend(listusers(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def admin():
    adminpassword = pywebio.input.input("请输入管理员超级验证密码：")
    if admin_password != adminpassword:
        loginerror()
    while True:
        with use_scope('userlist'):
            put_text(f"""
        用户列表：
        {listusers('sms')}
        """)
        sendto = pywebio.input.input("发送到：")
        output.clear('userlist')
        smscontent = pywebio.input.input("消息内容：")
        writesms = open(f"sms/{sendto}.user", "a+")
        writesms.write(smscontent)
        writesms.write('\n')
        put_success("发送成功！")
#写admin的时候，发消息一定要写到下一条消息上面，参考anika的getkey.py
if __name__ == '__main__':
    start_server([index,register,smsconsole,admin], debug=True, port=2294)
    pywebio.session.hold()
