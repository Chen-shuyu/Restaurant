from random import Random

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from Crypto.Cipher import DES
import pyrebase

config = {
    'apiKey': "AIzaSyC_66wWzNNsNlZay8c-B2YkwfXPqNhCnzI",
    'authDomain': "djangofirebase-36776.firebaseapp.com",
    'databaseURL': "https://djangofirebase-36776-default-rtdb.firebaseio.com",
    'projectId': "djangofirebase-36776",
    'storageBucket': "djangofirebase-36776.appspot.com",
    'messagingSenderId': "135981042713",
    'appId': "1:135981042713:web:39919f404983da2c42ee88",
    'measurementId': "G-E6ST30VQ4D",
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()
users = []
key = b'abcdefgh'  # 金鑰 8位或16位,必須為bytes
authe = firebase.auth()



"""
# 登入(GET)
:param text:
:return:
"""
def login(request):
    print('[def] login\n')
    return render(request, "login.html")

"""
# 首頁
:param text:
:return:
"""
def home(request):
    return render(request, "firebaseHome.html")

"""
# 檢查登入帳號密碼
:param text:
:return:
"""
def check(name, pasw):
    users, user_key = readDB()
    tmp = {}
    pas = False
    message = ""
    for k in users:
        if (k['name'] == name):
            tmp = k
            pas = True
            message = ""
            break
        else:
            pas = False
            message = "Invalid Credentials!!Please Check your name"
    if message != "":
        return message, pas

    if (password_decrypt(tmp['password']) == str(pasw)):
        if (k['certification'] == "1"):
            message = k['name']
            pas = True
        else:
            pas = False
            message = "Invalid Credentials!!Please Certification your Account"
    else:
        pas = False
        message = "Invalid Credentials!!Please Check your password"
    return message, pas

"""
# 登入(POST)
:param text:
:return:
"""
def postsignIn(request):
    name = request.POST.get('username')
    pasw = request.POST.get('password')
    print(name)
    print(pasw)
    message, pas = check(name, pasw)
    if (pas):
        return render(request, "firebaseHome.html", {"name": message})
    else:
        return render(request, "login.html", {"message": message})

"""
# 登出
:param text:
:return:
"""
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "login.html")

"""
# 註冊(get)
:param text:
:return:
"""
def enroll(request):
    print('signUp')
    return render(request, "enroll.html")

"""
# 註冊(post)
:param text:
:return:
"""
def postsignUp(request):
    print('[def] postsignUp\n')
    email = request.POST.get('email')
    password = request.POST.get('password')
    username = request.POST.get('username')
    print(password)
    print(email)
    password_ency = password_encryption(password)
    certification_id = create_certification_id()
    try:
        # "certification_id":
        users, user_key = readDB()
        for k in users:
            if k['name'] == username:
                return render(request, "enroll.html")

        data = {"name": username, "email": email, "password": str(password_ency), "certification": "0",
                "certification_id": certification_id}
        database.child("Data").child("users").push(data)
        sendCertificationEmail(certification_id, email, username, request)
    except Exception as e:
        print(e)
        return render(request, "enroll.html")
    return render(request, "login.html")

"""
# 寄出認證信
:param text:
:return: text
"""
def sendCertificationEmail(certification_id, email, username, request):
    certification_url = "http://127.0.0.1:8000/myapp/certification/" + certification_id
    res = send_mail("certification ", "Hello " + username + "\nPlease certification", "suyuchen322@gmail.com", [email],
                    html_message='<a <a href=' + certification_url + '>點選連結進行驗證<a>')
    return HttpResponse('%s' % res)

"""
# 認證信點取後的驗證
:param text:
:return: text
"""
def certification(request, id=""):
    print('[def] certification \n')
    tt = id
    print(tt)
    users, user_key = readDB()
    for i in range(len(users)):
        if users[i]['certification_id'] == tt:
            database.child("Data").child("users").child(user_key[i]).update({"certification": "1"})
    return render(request, "certification.html", {'id': id})

"""
# 產生亂數ID
:param text:
:return: text
"""
def createId():
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(16):
        str += chars[random.randint(0, length)]
    return str

"""
# 產生認證信的ID
:param text:
:return: text
"""
def create_certification_id():
    print('[def] create_certification_id \n')
    str = createId()
    users, user_key = readDB()
    stop = True
    while stop:
        for k in users:
            # print(k['certification_id'] )
            if k['certification_id'] != str:
                print("wrong")
                stop = False
            else:
                print("true")
    print(str)
    return str

"""
# 讀取會員資料
:param text:
:return: text
"""
def readDB():
    print('[def] readDB \n')
    all_Data = database.child("Data").child('users').get()
    user = []
    user_key = []
    for i, data in enumerate(all_Data.each()):
        user_key.append(data.key())
        user.append(data.val())
    return user, user_key



"""
# 加密函式，如果text不是8的倍數【加密文字text必須為8的倍數！】，那就補足為8的倍數
:param text:
:return:
"""
def pad(text):
    print('[def] pad \n')
    print('text: ' + text + '\n')
    while len(text) % 8 != 0:
        text += ' '
    return text


"""
# 加密
:param text:
:return: text
"""
def password_encryption(text):
    print('[def] password_encryption \n')
    des = DES.new(key, DES.MODE_ECB)  # 建立一個DES例項
    padded_text = pad(text)
    encrypted_text = des.encrypt(padded_text.encode('utf-8'))  # 加密
    print(encrypted_text)
    return encrypted_text


"""
# 解密
:param text:
:return: text
"""
def password_decrypt(encrypted_text):
    print('[def] password_decrypt \n')
    c = eval(encrypted_text)
    des = DES.new(key, DES.MODE_ECB)  # 建立一個DES例項
    # rstrip(' ')返回從字串末尾刪除所有字串的字串(預設空白字元)的副本
    plain_text = des.decrypt(c).decode().rstrip(' ')  # 解密
    print(plain_text)
    return plain_text


###############################################################################################

def reset(request):
    return render(request, "firebaseReset.html")


def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is successfully sent"
        return render(request, "firebaseReset.html", {"msg": message})
    except:
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "firebaseReset.html", {"msg": message})


def fireBaseDBtest(request):
    all_Data = database.child("Data").child('users').get()
    for i, data in enumerate(all_Data.each()):
        print(data.key())
        print(data.val())
        users.append(data.val())
    return HttpResponse("done")

def test(request):
    id = "NC3MOV8vJHPaKknq"
    users, user_key = readDB()
    for i in range(len(users)):
        if users[i]['certification_id'] == id:
            database.child("Data").child("users").child(user_key[i]).update({"certification": "1"})
            return HttpResponse("done")

    return HttpResponse("done")


def detail(request):
    return render(request, "detail.html")