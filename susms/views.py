from django.http import HttpResponse,HttpResponseBadRequest
import json
import random
import time
def sendsms(request):
    timenow = time.strftime("%m-%d-%Y %H:%M", time.localtime())
    if request.method=="GET":
        sendto = request.GET["send"]
        number = request.GET["number"]
        password = request.GET["password"]
        content = request.GET["content"]
        try:
            open(f"sms/{number}.user/msgbox.txt", "r")
        except:
            error = { 'code' : 403, 'text': 'loginuserIncorrect' ,'loginnumber' : number } 
            data2 = json.dumps(error)
            return HttpResponse(data2)
        f = open(f"sms/{number}.user/loginpassword.txt", "r")
        if password != f.read():
            error = { 'code' : 403, 'text': 'passwordIncorrect' ,'loginnumber' : number, 'password' : password }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        try:
            line_data = sendto.replace('"', '').split(',')
            newlinedata = str(line_data)
            print(newlinedata.count(","))
            if newlinedata.count(",") == "0":
                writesms = open(f"sms/{line_data[0]}.user/msgbox.txt", "a+")
                writesms.write(f"{number}: {content} [{timenow}]")
                writesms.write('\n')
            else:
                forlinedata = newlinedata.count(",") + 1
                for i in range(int(forlinedata)):
                    writesms = open(f"sms/{line_data[i]}.user/msgbox.txt", "a+")
                    writesms.write(f"{number}: {content} [{timenow}]")
                    writesms.write('\n')
            data = { 'code' : 200, 'text': 'success' ,'number' : number, 'sendto' : sendto, 'content' : content, 'sendnumber' : forlinedata}
            data2 = json.dumps(data)
        except(Exception, BaseException) as error:
            errordata = { 'code' : 404, 'text': 'sendusernotfound' ,'sendnumber' : sendto, 'content' : content}
            data2 = json.dumps(errordata)
            return HttpResponse(data2)
    elif request.method=="POST":
        pass
    else:
        pass
    return HttpResponse(data2)
def listsms(request):
    if request.method=="GET":
        number = request.GET["number"]
        password = request.GET["password"]
        try:
            open(f"sms/{number}.user/msgbox.txt", "r")
        except:
            error = { 'code' : 403, 'text': 'loginuserIncorrect' ,'loginnumber' : number }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        f = open(f"sms/{number}.user/loginpassword.txt", "r")
        if password != f.read():
            error = { 'code' : 403, 'text': 'passwordIncorrect' ,'loginnumber' : number, 'password' : password }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        try:
            readsms = open(f"sms/{number}.user/msgbox.txt", "r")
            getsms = readsms.read()
            data = { 'code' : 200, 'text': 'success', 'number' : number, 'smscontent' : getsms}
            data2 = json.dumps(data)
        except:
            data = { 'code' : 404, 'text': 'failed','number' : number}
            data2 = json.dumps(data)
    elif request.method=="POST":
        pass
    else:
        pass
    return HttpResponse(data2)
def clearmsg(request):
    if request.method=="GET":
        number = request.GET["number"]
        password = request.GET["password"]
        try:
            open(f"sms/{number}.user/msgbox.txt", "r")
        except:
            error = { 'code' : 403, 'text': 'loginuserIncorrect' ,'loginnumber' : number }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        f = open(f"sms/{number}.user/loginpassword.txt", "r")
        if password != f.read():
            error = { 'code' : 403, 'text': 'passwordIncorrect' ,'loginnumber' : number, 'password' : password }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        try:
            writesms = open(f"sms/{number}.user/msgbox.txt", "w")
            writesms.write("")
            data = { 'code' : 200, 'text': 'success' ,'number' : number}
            data2 = json.dumps(data)
        except:
            data = { 'code' : 404, 'text': 'failed' ,'number' : number}
            data2 = json.dumps(data)
    elif request.method=="POST":
        pass
    else:
        pass
    return HttpResponse(data2)
def infosms(request):
    timenow = time.strftime("%m-%d-%Y %H:%M", time.localtime())
    if request.method=="GET":
        number = request.GET["number"]
        password = request.GET["password"]
        sendto = request.GET["send"]
        content = request.GET["content"]
        try:
            open(f"sms/{number}.user/msgbox.txt", "r")
        except:
            error = { 'code' : 403, 'text': 'loginuserIncorrect' ,'loginnumber' : number }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        f = open(f"sms/{number}.user/loginpassword.txt", "r")
        if password != f.read():
            error = { 'code' : 403, 'text': 'passwordIncorrect' ,'loginnumber' : number, 'password' : password }
            data2 = json.dumps(error)
            return HttpResponse(data2)
        try:
            tempcode = random.randint(10000, 99999)
            maketempcodenum = '10000' + number + str(tempcode)
            msgsmssave = open(f"sms/{number}.user/msgsmssave.txt", "a")
            msgsmssave.write(f"{maketempcodenum}: {content}\n")
        except(Exception, BaseException) as error:
            error = { 'code' : 403, 'text': 'servicenotactivated', 'error' : error}
            data2 = json.dumps(error)
            return HttpResponse(data2)
        try:
            line_data = sendto.replace('"', '').split(',')
            newlinedata = str(line_data)
            print(newlinedata.count(","))
            if newlinedata.count(",") == "0":
                writesms = open(f"sms/{line_data[0]}.user/msgbox.txt", "a+")
                writesms.write(f"{maketempcodenum}: {content} [{timenow}]")
                writesms.write('\n')
            else:
                forlinedata = newlinedata.count(",") + 1
                for i in range(int(forlinedata)):
                    writesms = open(f"sms/{line_data[i]}.user/msgbox.txt", "a+")
                    writesms.write(f"{maketempcodenum}: {content} [{timenow}]")
                    writesms.write('\n')
            data = { 'code' : 200, 'text': 'success' ,'number' : number, 'sendto' : sendto, 'content' : content, 'infonumber' : maketempcodenum, 'sendnumber' : forlinedata}
            data2 = json.dumps(data)
        except:
            data = { 'code' : 404, 'text': 'sendusernotfound' ,'number' : number}
            data2 = json.dumps(data)
    elif request.method=="POST":
        pass
    else:
        pass
    return HttpResponse(data2)
