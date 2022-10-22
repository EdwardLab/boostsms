# coding=utf-8
# -*- coding: utf-8 -*-
import pywebio.input
from pywebio.input import *
from pywebio.output import *
from pywebio import *
from pywebio.session import *
from pywebio.pin import *
import pywebio.platform
import random
import time
import os
deploy = "Boost SMS"
admin_password = "xingyujie2294001xyj"
class GetError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
        
def index():
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    #put_markdown("## Welcome to Boost SMS Privacy SMS Platform")
    put_html("""

<div class="jumbotron">
  <h1 class="display-4">Welcome to Boost SMS Console</h1>
  <p class="lead">Boost SMS is an API interface, privacy, fast network SMS sending and receiving platform.</p>
  <hr class="my-4">
  <p>Project by Microtech Group and Edward Hsing</p>
  <a class="btn btn-primary btn-lg" href="/?app=register" role="button">Register now</a>
</div>
    """)
    put_text("Boost SMS is a messaging/communication platform that replaces SMS verification codes, developed by Microtech Group, supports sending and receiving SMS messages, docking verification codes, etc.")
    put_warning("If you are a user, please register an account, you will get a boost SMS number, you can chat freely with other boost numbers, if there is a form to fill out, please fill in your boost in the form provided by the service provider . If you are a developer, find our contact details on this page")
    put_link("register a boost user/message console", app='register')
    put_markdown("""
## Contact us to upgrade to Premium version with full API and additional plans
WhatsApp: +16167997429 
Discord: xingyujie#2550 
Facebook: [Edward](https://www.facebook.com/xingyujie50) 
Snapchat: [Edward Hsing](https://www.snapchat.com/add/xingyujie50?share_id=XQ8dG5mh_CI&locale=en-US) 
Instagram: yujie348 
Telegram: [@edward_hsing](https://t.me/edward_hsing)
    """)
def register():
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    put_markdown("## Welcome to Boost SMS")
    put_button("Register Boost SMS ", onclick=lambda: getuser(), color='success', outline=True)
    put_link("Boost SMS Dashborad", app='smsconsole')
def getuser():
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    put_markdown("## Welcome to register Boost SMS free plan")
    with use_scope('notice'):
        put_success("You are registering for Free Boost, the Boost SMS free plan supports personal use [commercial use prohibited], message sending and receiving and docking API (community support only). The free version does not support custom numbers and has 10 random numbers. Upgrade to our Premium version and enjoy 8-digit number length or less, optional standards-compliant custom numbers, optional business use, and full customer support/troubleshooting. Please find our full contact details on the page.")
        put_text("The free version requires no moderation, just answer a few questions and register to generate a number instantly! Do not abuse!")
    phonenum = pywebio.input.input("Enter your mobile number (please add the area code, e.g. +1 (xxx) xxx-xxxx):",required=True)
    f = open("phonelist.txt", "a")
    f.write(phonenum + '\n')
    output.clear('notice')
    reason = pywebio.input.textarea("Can you tell us why you chose boost:",required=True)
    f = open("regreason.txt", "a")
    f.write(reason + "\n")
    sunumber = random.randint(1000000000, 9999999999)
    os.makedirs(f"sms/{sunumber}.user")
    setpassword = pywebio.input.input("Setting login password:")
    f = open(f"sms/{sunumber}.user/loginpassword.txt", "w")
    f.write(setpassword)
    open(f"sms/{sunumber}.user/msgbox.txt", "w")
    put_success(f"registration success! Your boost number is: {sunumber}, please keep your boost number and password and do not disclose it to others")
def usersend():
        timenow = time.strftime("%m-%d-%Y %H:%M", time.localtime())
        set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
        output.clear('sendok')
        userinput = input_group("Send messages to other boost number [spam is strictly prohibited!]",[
        pywebio.input.input('Send to [boost number] [Support sending messages to multiple numbers, please separate with "," (such as xxx,xxx)]:', name='number'),
        pywebio.input.textarea('Content: [Support HTML syntax]', name='smscontent')])   
        sendnumber = userinput['number']
        sendcontent = userinput['smscontent']
        try:
            #writesms = open(f"sms/{sendnumber}.user/msgbox.txt", "a+")
            #writesms.write(f"{sunumber}: {sendcontent} [{timenow}]")
            #writesms.write('\n')

            line_data = sendnumber.replace('"', '').split(',')
            newlinedata = str(line_data)
            print(newlinedata.count(","))
            if newlinedata.count(",") == "0":
                writesms = open(f"sms/{line_data[0]}.user/msgbox.txt", "a+")
                writesms.write(f"{sunumber}: {sendcontent} [{timenow}]")
                writesms.write('\n')
            else:
                forlinedata = newlinedata.count(",") + 1
                for i in range(int(forlinedata)):
                    writesms = open(f"sms/{line_data[i]}.user/msgbox.txt", "a+")
                    writesms.write(f"{sunumber}: {sendcontent} [{timenow}]")
                    writesms.write('\n')
            with use_scope('sendok'):
                put_success("Sent successfully!")
                put_button("Sent successfully! Click here to post another", onclick=lambda: usersend(), color='success', outline=True)
        except(Exception, BaseException) as error:
            with use_scope('notfound'):
                put_error("User does not exist or send failed")
                output.clear('sendok')
                put_button("Resend", onclick=lambda: [output.clear('notfound'),usersend()], color='success', outline=True)
                output.clear('sendok')

def smsui():
        set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
        with use_scope('smsui'):
            noticesms.seek(0)
            sms.seek(0)
            put_markdown(f"""
## Messages:
____________________________________________________
{noticesms.read()}
{sms.read()}
____________________________________________________
Login user: {sunumber}
        """)
def smsconsole():
    global noticesms
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    global sunumber
    global sms
    put_markdown(f"## Welcome to the Boost Message Console[{deploy}]")
    sunumber = pywebio.input.input("Please enter your boost number:")
    try:
        sms = open(f"sms/{sunumber}.user/msgbox.txt", "r")
        #writesms = open(f"sms/{sunumber}.user", "w")
    except:
        loginerror()
    password = pywebio.input.input("Please enter your login password:", required=True)
    f = open(f"sms/{sunumber}.user/loginpassword.txt", "r")
    if password != f.read():
        loginerror()
    noticesms = open(f"noticesms.txt", "r")
    put_buttons(['refresh message list'], onclick=lambda _: [output.clear('smsui'), smsui()])
    smsui()
    put_buttons(['delete all messages'], onclick=lambda _: removeallsms())
    usersend()
def loginerror():
    try:
        raise GetError("Disconnect from server")
    except:
        put_error("Incorrect boost number or password")
        time.sleep(3)
        put_link("retry", './premiumpanel')   
        go_app('#', new_window=False)
def listusers(rootdir):
    import os
    _files = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            _files.extend(listusers(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def admin():
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    adminpassword = pywebio.input.input("password：")
    if admin_password != adminpassword:
        loginerror()
    while True:
        with use_scope('userlist'):
            put_text(f"""
        User files：
        {listusers('sms')}
        """)
        sendto = pywebio.input.input("Send to：")
        output.clear('userlist')
        smscontent = pywebio.input.textarea("Content：")
        put_success(f"sms/{sendto}.user/msgbox.txt")
        writesms = open(f"sms/{sendto}.user/msgbox.txt", "a+")
        writesms.write(smscontent)
        writesms.write('\n')
        put_success("OK!")
def removeallsms():
        writesms = open(f"sms/{sunumber}.user/msgbox.txt", "w")
        writesms.write("")
        writesms.write('\n')
        toast("successfully deleted!")
def infosend():
    tempcode = random.randint(10000, 99999)
    timenow = time.strftime("%m-%d-%Y %H:%M", time.localtime())
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    adminpassword = pywebio.input.input("password:")
    if admin_password != adminpassword:
        loginerror()
    while True:
        number = pywebio.input.input("Send to:")
        content = pywebio.input.textarea("Content:")
        put_success(f"sms/{number}.user/msgbox.txt")
        writesms = open(f"sms/{number}.user/msgbox.txt", "a+")
        writesms.write(f"100000000000000{tempcode}: {content} [{timenow}]")
        writesms.write('\n')
        writesms.close()
        put_success("OK!")
def authinfosms():
    tempcode = random.randint(10000, 99999)
    timenow = time.strftime("%m-%d-%Y %H:%M", time.localtime())
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    adminpassword = pywebio.input.input("password:")
    if admin_password != adminpassword:
        loginerror()
    while True:
        number = pywebio.input.input("Auth number:")
        open(f"sms/{number}.user/msgsmssave.txt", "w")
def sendto(number, content):
    tempcode = random.randint(10000, 99999)
    timenow = time.strftime("%m-%d-%Y %H:%M", time.localtime())
    writesms = open(f"sms/{number}.user/msgbox.txt", "a+")
    writesms.write(f"288000000000000{tempcode}: {content} [{timenow}]")
    writesms.write('\n')
    writesms.close()
def groupsend():
    set_env(title=f"Boost SMS",output_max_width="100%", auto_scroll_bottom=True)
    #adminpassword = pywebio.input.input("password:")
    #if admin_password != adminpassword:
    #    loginerror()
    while True:
        data = pywebio.input.input("Input Group send number:")
        content = pywebio.input.input("Content:")
        line_data = data.replace('"', '').split(',')
        print(line_data)
        print(line_data[1])
        newlinedata = str(line_data)
        print(newlinedata.count(","))
        for i in range(int(newlinedata.count(",") + 1)):
            sendto(line_data[i], content)
            

if __name__ == '__main__':
    start_server([index,register,smsconsole,admin,infosend,authinfosms,groupsend], debug=True, port=2294)
    pywebio.session.hold()
