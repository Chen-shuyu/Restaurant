import requests
from django.contrib import auth
from django.core.mail import send_mass_mail, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from random import Random
from myapp import forms, models
from myapp.forms import LoginForm, ProfileForm
from myapp.models import Dreamreal, Profile
from Crypto.Cipher import DES
import pyrebase


# Create your views here.

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
    return render(request, "index.html")

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

#===================================allen==allen==allen==allen==allen==allen=================================================

#===================================allen==allen==allen==allen==allen==allen=================================================

#===================================allen==allen==allen==allen==allen==allen=================================================

def Delicacy(request):
    shop1 = {"name": "享你好酒不見", "address": "100台北市中正區汀州路三段160巷", "star": "3.9", "dis": "550"}
    shop2 = {"name": "夢駝鈴咖啡餐廳", "address": "100台北市中正區汀州路三段108號", "star": "3.7", "dis": "400"}
    shop3 = {"name": "窩巷弄", "address": "10090台北市中正區羅斯福路四段78巷1弄11號", "star": "3.9", "dis": "400"}
    shop4 = {"name": "貳樓餐廳 Second Floor Cafe 公館店", "address": "100台北市中正區羅斯福路三段316巷9弄7號", "star": "4.1", "dis": "160"}
    shop5 = {"name": "三米三小館", "address": "100台北市中正區羅斯福路三段286巷4弄12號", "star": "4.3", "dis": "140"}
    shop6 = {"name": "初牛 台北公館店", "address": "100台北市中正區汀州路三段169號", "star": "4.2", "dis": "250"}
    shop7 = {"name": "易牙居餐廳", "address": "100台北市中正區羅斯福路三段286巷16號", "star": "3.9", "dis": "120"}
    shop8 = {"name": "站食可以", "address": "100台北市中正區羅斯福路四段24巷12弄7號", "star": "4.7", "dis": "280"}
    shop9 = {"name": "寶島肉圓店", "address": "116台北市文山區羅斯福路五段136號", "star": "4.2", "dis": "1500"}
    shop10 = {"name": "阿玉水餃 (生水餃專賣店)", "address": "106台北市大安區辛亥路二段217號", "star": "4.3", "dis": "1800"}
    shop11 = {"name": "拾年腸粉/公館美食", "address": "100台北市中正區水源路27巷19號", "star": "4.9", "dis": "900"}
    shop12 = {"name": "El Sabroso Mexican Food", "address": "100台北市中正區汀州路三段107號之一", "star": "4.2", "dis": "350"}
    shop13 = {"name": "海邊的卡夫卡 Kafka by the Sea", "address": "10090台北市中正區羅斯福路三段244巷2號2樓", "star": "4.5", "dis": "110"}
    shop14 = {"name": "INTERMISSION 中場休息 Cafe'", "address": "100台北市中正區汀州路三段149號1樓", "star": "4.9", "dis": "210"}
    shop15 = {"name": "辛殿麻辣鍋|公館店", "address": "100台北市中正區羅斯福路三段316巷9弄1號", "star": "3.9", "dis": "190"}
    shop16 = {"name": "池先生 Kopitiam (公館店)", "address": "100台北市中正區羅斯福路三段284巷10號", "star": "4.2", "dis": "130"}
    shop17 = {"name": "麥當勞-台北新生店", "address": "106台北市大安區新生南路三段88之2號", "star": "3.9", "dis": "350"}
    shop18 = {"name": "麥當勞-台北台大店", "address": "106台北市大安區羅斯福路四段1號1樓", "star": "3.3", "dis": "850"}
    shop19 = {"name": "炸手指/公館宵夜", "address": "100台北市中正區羅斯福路三段316巷8弄4號", "star": "4.5", "dis": "170"}
    shop20 = {"name": "鴉片粉圓", "address": "No. 191新生街中和區新北市235號", "star": "3.7", "dis": "7100"}
    shop21 = {"name": "鷹流東京豚骨拉麵-極匠", "address": "100台北市中正區汀州路三段104巷4號", "star": "4.0", "dis": "350"}
    shop22 = {"name": "尖蚪", "address": "100台北市中正區汀州路三段230巷57號", "star": "4.5", "dis": "1300"}
    shop23 = {"name": "心KOKORO食堂/台北日式料理/公館美食/公館小吃/公館餐廳/公館日式料理/公館壽司", "address": "100台北市中正區汀州路三段104巷11弄15號一樓",
              "star": "4.3", "dis": "450"}
    shop24 = {"name": "幸好沒錯過你 Master K.", "address": "100台北市中正區羅斯福路四段78巷1弄5號", "star": "4.0", "dis": "450"}
    shop25 = {"name": "泰國小館", "address": "100台北市中正區汀州路三段219號", "star": "3.9", "dis": "400"}
    shop26 = {"name": "台北美食/公館美食/酸菜白肉鍋/中式熱炒/聚餐/聚會/刀削麵/豆沙鍋餅/北方麵食/順園小館", "address": "100台北市中正區汀州路三段281號", "star": "4.0",
              "dis": "700"}
    shop27 = {"name": "Bravo Burger發福廚房公館台大店", "address": "100台北市中正區羅斯福路四段44之1號2樓", "star": "4.0", "dis": "240"}



    shops = [shop1, shop2, shop3, shop4, shop5, shop6, shop7, shop8, shop9, shop10,
             shop11, shop12, shop13, shop14, shop15, shop16, shop17, shop18, shop19, shop20,
             shop21, shop22, shop23, shop24, shop25, shop26, shop27]

    # for key, value in datas.items():
    #     print(key, value.split(";")[0], value.split(";")[1], value.split(";")[2])
    return render(request, 'Delicacy.html', locals())


def boardpost(request):
    if request.method == 'POST':
        postform = forms.PostForm(request.POST)
        if postform.is_valid():
            name = postform.cleaned_data['boardname']
            subject = postform.cleaned_data['boardsubject']
            message = postform.cleaned_data['boardmessage']

            unit = models.Board.objects.create(bname=name, bsubject=subject, bmessage=message)
            unit.save()
            msg = 'Your message is saved'
            postform = forms.PostForm()
            return redirect('/')
        else:
            msg = 'Error'
    else:
        msg = 'name, subject and message must be entered'
        postform = forms.PostForm()
    return render(request, 'boardpost.html', locals())

def boardlist(request, s):
    boardunits = models.Board.objects.all().order_by('-id')
    #today = date.today()
    shop1 = {'name': '享你好酒不見',
             'Introduction': '隱身熱鬧的台大公館夜市、公館捷運站、水源市場旁的自來水園區內，是台北市內難得一見的露天啤酒bar，擁有千坪廣大空間，老闆一手包辦設計了所有風格獨具的場景，傍晚後夜色迷人，成為北市上班族下班後吃飯喝酒、放鬆、聚餐的愜意場合。'}
    shop2 = {'name': '夢駝鈴咖啡餐廳', 'Introduction': '義大利口味不錯，東西平價，二樓的格局蠻特別的'}
    shop3 = {'name': '窩巷弄',
             'Introduction': '窩巷弄是一間寵物友善餐廳，餐點以義大利麵與早午餐為主，下午2點~5點還有推出「巷弄午茶」的下午茶的組合，這邊不收服務費，有提供免費wifi可以使用，一般用餐時間為2小時，如果沒有人候位的話，就沒有用餐時間的限制'}
    shop4 = {'name': '貳樓餐廳_Second_Floor_Cafe_公館店',
             'Introduction': '公館人久等了！閉店休息長達兩年多的「貳樓餐廳Second Floor Cafe」，經過長時間的整修和籌備，終於在2020年十月重新開幕'}
    shop5 = {'name': '三米三小館', 'Introduction': '是一家人氣高不收服務費的米食餐廳，就在公館商圈陳三鼎粉圓對面的小巷裡，餐廳裡的空間不大但是用餐的座位區是舒服的靠背沙發椅喔'}
    shop6 = {'name': '初牛_台北公館店',
             'Introduction': '在汀州路三段上的台北市政府警察局中正第二分局思源街派出所＆鐵路新店線水源地站遺址對面，思源街底，附近交通方便，不論中午或是晚上人潮和車潮都很多。'}
    shop7 = {'name': '易牙居餐廳',
             'Introduction': '公館店位於台大校園新生南路與羅斯福路交叉口交通便利，公館捷運站週邊更有自來水博物館的好景點公館店佔地三層樓，除了港式飲茶2樓更有獨立包廂，更是工商宴客、親朋好友聚會好地點精緻港式飲茶更推出「主廚親制冷凍半成品」'}
    shop8 = {'name': '站食可以', 'Introduction': '可以是一間以外帶為主的餐廳，有海南雞飯、好吃雞肉飯、蔥燒醬豚飯三種和湯品可以選擇。'}
    shop9 = {'name': '寶島肉圓店', 'Introduction': '曾經因為生意太好，被原本房東趕走，倉促之下來到了羅斯福路開店，卻因大量老主顧流失，讓寶島肉圓幾乎又辛苦的從頭開始經營。'}
    shop10 = {'name': '阿玉水餃_生水餃專賣店', 'Introduction': '阿玉水餃這裡沒有提供內用的服務. 只販賣沒煮過的生水餃. 客人可以自己買回家煮. 阿玉水餃以豬肉水餃為主。'}
    shop11 = {'name': '拾年腸粉_公館美食', 'Introduction': '裝潢擺設復古懷舊，彷彿重返外婆家，裡面僅3個位子，外頭一個方桌而已。'}
    shop12 = {'name': 'El_Sabroso_Mexican_Food',
              'Introduction': '一間小店面、溫馨可愛的墨西哥料理，老闆也是墨西哥人，餐點口味滿道地的，薄餅、捲餅是主要的品項，可以搭配的炒料和醬料選擇非常多。'}
    shop13 = {'name': '海邊的卡夫卡_Kafka_by_the_Sea', 'Introduction': '坐落在台電大樓旁的巷子上,某棟建築物的2F，不起眼的入口,循著階梯往上爬就是海邊的卡夫卡。'}
    shop14 = {'name': '池先生_Kopitiam_公館店',
              'Introduction': '超道地的馬來西亞料理，是許多大馬人想起家鄉味的一間餐廳，對於喜愛南洋風味的饕客也是一間必吃的餐廳，評價狂推薦咖哩椰漿飯、煲仔飯、叻沙麵、海南雞等等料理。'}
    shop15 = {'name': 'INTERMISSION_中場休息_Cafe', 'Introduction': '最近好喜歡融合復古懷舊的咖啡店，位在公館站的INTERMISSION 中場休息 Cafe。'}
    shop16 = {'name': '辛殿麻辣鍋_公館店',
              'Introduction': '超人氣火鍋吃到飽辛殿麻辣鍋在10月進軍公館商圈，改造60年台鐵老宅， 除了店外觀帶著懷舊復古感，內部環境更結合智利拼貼藝術家作品跨界合作。'}
    shop17 = {'name': '麥當勞_台北新生店',
              'Introduction': '麥當勞不僅僅是一家餐廳,這句話精確地涵概了麥當勞集團的經營理念。在全球麥當勞的整體制度體系中，麥當勞餐廳的營運是很重要的一環，因爲麥當勞的經營理念和歡樂、美味是通過。'}
    shop18 = {'name': '麥當勞_台北台大店',
              'Introduction': '麥當勞不僅僅是一家餐廳,這句話精確地涵概了麥當勞集團的經營理念。在全球麥當勞的整體制度體系中，麥當勞餐廳的營運是很重要的一環，因爲麥當勞的經營理念和歡樂、美味是通過。'}
    shop19 = {'name': '炸手指_公館宵夜', 'Introduction': '專賣鹹酥雞、炸物、碳烤類~ 而且是可以內用。'}
    shop20 = {'name': '鴉片粉圓', 'Introduction': '鴉片粉圓1973年成立，從新北市板橋發跡，從一碗3元開始，這家店名由來，是因有客人吃了，稱就像抽鴉片一樣會上癮，因此得名。'}
    shop21 = {'name': '鷹流東京豚骨拉麵_極匠', 'Introduction': '鷹流東京豚骨拉麵-極匠店內用餐空間也非常的小，只有吧檯座位，約莫不到20個座位。'}
    shop22 = {'name': '尖蚪', 'Introduction': '延續了寶藏巖富含歷史足跡的建築風格，店內不只氣氛好東西又好吃，還會跟藝術家合作展覽，在一波網美咖啡廳中顯得獨樹一格，是文青最愛的午茶首選'}
    shop23 = {'name': '心KOKORO食堂', 'Introduction': '心kokoro食堂的外觀帶點日系木質的設計，門口可以看到菜單和打卡送塔塔醬薯條的資訊。'}
    shop24 = {'name': '幸好沒錯過你_Master_K.',
              'Introduction': '羅斯福路巷弄中，幸好沒錯過你相較於左右幾間店面的招牌低調許多，日式風格的淡粉紅色招牌，寫著幸好沒錯過你，旁邊還有個愛心和小黑板，簡單但非常可愛。'}
    shop25 = {'name': '泰國小館', 'Introduction': '店內裝潢很居家感，不走華麗風，座位一二樓都有，上二樓的樓梯比較陡窄，需要注意。'}
    shop26 = {'name': '順園小館',
              'Introduction': '「順園小館」應該算是台大公館商圈知名的老餐館之一，從1986年開張至今，已經逾30歲，而在2018年底重新裝修改造，打造更優質的用餐環境及氛圍。'}
    shop27 = {'name': 'Bravo_Burger_發福廚房公館台大店',
              'Introduction': '公館店好像是今年初才新開幕的，所以餐廳裏的佈置裝潢都還蠻新的，位子比起其它兩家的分店好像也比較多一些，一、二樓層的客席坐位，加起來應該有50~60位左右。'}
    shops = [shop1, shop2, shop3, shop4, shop5, shop6, shop7, shop8, shop9, shop10,
         shop11, shop12, shop13, shop14, shop15, shop16, shop17, shop18, shop19, shop20,
         shop21, shop22, shop23, shop24, shop25, shop26, shop27]
    for i in range(27):
        if s == shops[i]['name']:
            n = shops[i]['name']
            info = shops[i]['Introduction']

    #print(info)
    return render(request, 'boardlist.html', locals())




def index(request, d):
    shop1 = {"name": "享你好酒不見", "address": "100台北市中正區汀州路三段160巷", "star": "3.9", "dis": "550"}
    shop2 = {"name": "夢駝鈴咖啡餐廳", "address": "100台北市中正區汀州路三段108號", "star": "3.7", "dis": "400"}
    shop3 = {"name": "窩巷弄", "address": "10090台北市中正區羅斯福路四段78巷1弄11號", "star": "3.9", "dis": "400"}
    shop4 = {"name": "貳樓餐廳_Second_Floor_Cafe_公館店", "address": "100台北市中正區羅斯福路三段316巷9弄7號", "star": "4.1", "dis": "160"}
    shop5 = {"name": "三米三小館", "address": "100台北市中正區羅斯福路三段286巷4弄12號", "star": "4.3", "dis": "140"}
    shop6 = {"name": "初牛_台北公館店", "address": "100台北市中正區汀州路三段169號", "star": "4.2", "dis": "250"}
    shop7 = {"name": "易牙居餐廳", "address": "100台北市中正區羅斯福路三段286巷16號", "star": "3.9", "dis": "120"}
    shop8 = {"name": "站食可以", "address": "100台北市中正區羅斯福路四段24巷12弄7號", "star": "4.7", "dis": "280"}
    shop9 = {"name": "寶島肉圓店", "address": "116台北市文山區羅斯福路五段136號", "star": "4.2", "dis": "1500"}
    shop10 = {"name": "阿玉水餃_生水餃專賣店", "address": "106台北市大安區辛亥路二段217號", "star": "4.3", "dis": "1800"}
    shop11 = {"name": "拾年腸粉_公館美食", "address": "100台北市中正區水源路27巷19號", "star": "4.9", "dis": "900"}
    shop12 = {"name": "El_Sabroso_Mexican_Food", "address": "100台北市中正區汀州路三段107號之一", "star": "4.2", "dis": "350"}
    shop13 = {"name": "海邊的卡夫卡_Kafka_by_the_Sea", "address": "10090台北市中正區羅斯福路三段244巷2號2樓", "star": "4.5", "dis": "110"}
    shop14 = {"name": "INTERMISSION_中場休息_Cafe", "address": "100台北市中正區汀州路三段149號1樓", "star": "4.9", "dis": "210"}
    shop15 = {"name": "辛殿麻辣鍋_公館店", "address": "100台北市中正區羅斯福路三段316巷9弄1號", "star": "3.9", "dis": "190"}
    shop16 = {"name": "池先生_Kopitiam_公館店", "address": "100台北市中正區羅斯福路三段284巷10號", "star": "4.2", "dis": "130"}
    shop17 = {"name": "麥當勞_台北新生店", "address": "106台北市大安區新生南路三段88之2號", "star": "3.9", "dis": "350"}
    shop18 = {"name": "麥當勞_台北台大店", "address": "106台北市大安區羅斯福路四段1號1樓", "star": "3.3", "dis": "850"}
    shop19 = {"name": "炸手指_公館宵夜", "address": "100台北市中正區羅斯福路三段316巷8弄4號", "star": "4.5", "dis": "170"}
    shop20 = {"name": "鴉片粉圓", "address": "No. 191新生街中和區新北市235號", "star": "3.7", "dis": "7100"}
    shop21 = {"name": "鷹流東京豚骨拉麵_極匠", "address": "100台北市中正區汀州路三段104巷4號", "star": "4.0", "dis": "350"}
    shop22 = {"name": "尖蚪", "address": "100台北市中正區汀州路三段230巷57號", "star": "4.5", "dis": "1300"}
    shop23 = {"name": "心KOKORO食堂", "address": "100台北市中正區汀州路三段104巷11弄15號一樓",
              "star": "4.3", "dis": "450"}
    shop24 = {"name": "幸好沒錯過你 Master K.", "address": "100台北市中正區羅斯福路四段78巷1弄5號", "star": "4.0", "dis": "450"}
    shop25 = {"name": "泰國小館", "address": "100台北市中正區汀州路三段219號", "star": "3.9", "dis": "400"}
    shop26 = {"name": "順園小館", "address": "100台北市中正區汀州路三段281號", "star": "4.0",
              "dis": "700"}
    shop27 = {"name": "Bravo_Burger_發福廚房公館台大店", "address": "100台北市中正區羅斯福路四段44之1號2樓", "star": "4.0", "dis": "240"}

    shops = [shop1, shop2, shop3, shop4, shop5, shop6, shop7, shop8, shop9, shop10,
             shop11, shop12, shop13, shop14, shop15, shop16, shop17, shop18, shop19, shop20,
             shop21, shop22, shop23, shop24, shop25, shop26, shop27]


    d = int(d)
    can_go = []

    for i in range(27):
        if d > int(shops[i]['dis']):
            name = shops[i]['name']
            can_go.append(name)
    print(can_go)
    return render(request, 'index.html', locals())


def boardlist2(request, d, s):
    boardunits = models.Board.objects.all().order_by('-id')
    #today = date.today()
    shop1 = {'name': '享你好酒不見',
             'Introduction': '隱身熱鬧的台大公館夜市、公館捷運站、水源市場旁的自來水園區內，是台北市內難得一見的露天啤酒bar，擁有千坪廣大空間，老闆一手包辦設計了所有風格獨具的場景，傍晚後夜色迷人，成為北市上班族下班後吃飯喝酒、放鬆、聚餐的愜意場合。'}
    shop2 = {'name': '夢駝鈴咖啡餐廳', 'Introduction': '義大利口味不錯，東西平價，二樓的格局蠻特別的'}
    shop3 = {'name': '窩巷弄',
             'Introduction': '窩巷弄是一間寵物友善餐廳，餐點以義大利麵與早午餐為主，下午2點~5點還有推出「巷弄午茶」的下午茶的組合，這邊不收服務費，有提供免費wifi可以使用，一般用餐時間為2小時，如果沒有人候位的話，就沒有用餐時間的限制'}
    shop4 = {'name': '貳樓餐廳_Second_Floor_Cafe_公館店',
             'Introduction': '公館人久等了！閉店休息長達兩年多的「貳樓餐廳Second Floor Cafe」，經過長時間的整修和籌備，終於在2020年十月重新開幕'}
    shop5 = {'name': '三米三小館', 'Introduction': '是一家人氣高不收服務費的米食餐廳，就在公館商圈陳三鼎粉圓對面的小巷裡，餐廳裡的空間不大但是用餐的座位區是舒服的靠背沙發椅喔'}
    shop6 = {'name': '初牛_台北公館店',
             'Introduction': '在汀州路三段上的台北市政府警察局中正第二分局思源街派出所＆鐵路新店線水源地站遺址對面，思源街底，附近交通方便，不論中午或是晚上人潮和車潮都很多。'}
    shop7 = {'name': '易牙居餐廳',
             'Introduction': '公館店位於台大校園新生南路與羅斯福路交叉口交通便利，公館捷運站週邊更有自來水博物館的好景點公館店佔地三層樓，除了港式飲茶2樓更有獨立包廂，更是工商宴客、親朋好友聚會好地點精緻港式飲茶更推出「主廚親制冷凍半成品」'}
    shop8 = {'name': '站食可以', 'Introduction': '可以是一間以外帶為主的餐廳，有海南雞飯、好吃雞肉飯、蔥燒醬豚飯三種和湯品可以選擇。'}
    shop9 = {'name': '寶島肉圓店', 'Introduction': '曾經因為生意太好，被原本房東趕走，倉促之下來到了羅斯福路開店，卻因大量老主顧流失，讓寶島肉圓幾乎又辛苦的從頭開始經營。'}
    shop10 = {'name': '阿玉水餃_生水餃專賣店', 'Introduction': '阿玉水餃這裡沒有提供內用的服務. 只販賣沒煮過的生水餃. 客人可以自己買回家煮. 阿玉水餃以豬肉水餃為主。'}
    shop11 = {'name': '拾年腸粉_公館美食', 'Introduction': '裝潢擺設復古懷舊，彷彿重返外婆家，裡面僅3個位子，外頭一個方桌而已。'}
    shop12 = {'name': 'El_Sabroso_Mexican_Food',
              'Introduction': '一間小店面、溫馨可愛的墨西哥料理，老闆也是墨西哥人，餐點口味滿道地的，薄餅、捲餅是主要的品項，可以搭配的炒料和醬料選擇非常多。'}
    shop13 = {'name': '海邊的卡夫卡_Kafka_by_the_Sea', 'Introduction': '坐落在台電大樓旁的巷子上,某棟建築物的2F，不起眼的入口,循著階梯往上爬就是海邊的卡夫卡。'}
    shop14 = {'name': '池先生_Kopitiam_公館店',
              'Introduction': '超道地的馬來西亞料理，是許多大馬人想起家鄉味的一間餐廳，對於喜愛南洋風味的饕客也是一間必吃的餐廳，評價狂推薦咖哩椰漿飯、煲仔飯、叻沙麵、海南雞等等料理。'}
    shop15 = {'name': 'INTERMISSION_中場休息_Cafe', 'Introduction': '最近好喜歡融合復古懷舊的咖啡店，位在公館站的INTERMISSION 中場休息 Cafe。'}
    shop16 = {'name': '辛殿麻辣鍋_公館店',
              'Introduction': '超人氣火鍋吃到飽辛殿麻辣鍋在10月進軍公館商圈，改造60年台鐵老宅， 除了店外觀帶著懷舊復古感，內部環境更結合智利拼貼藝術家作品跨界合作。'}
    shop17 = {'name': '麥當勞_台北新生店',
              'Introduction': '麥當勞不僅僅是一家餐廳,這句話精確地涵概了麥當勞集團的經營理念。在全球麥當勞的整體制度體系中，麥當勞餐廳的營運是很重要的一環，因爲麥當勞的經營理念和歡樂、美味是通過。'}
    shop18 = {'name': '麥當勞_台北台大店',
              'Introduction': '麥當勞不僅僅是一家餐廳,這句話精確地涵概了麥當勞集團的經營理念。在全球麥當勞的整體制度體系中，麥當勞餐廳的營運是很重要的一環，因爲麥當勞的經營理念和歡樂、美味是通過。'}
    shop19 = {'name': '炸手指_公館宵夜', 'Introduction': '專賣鹹酥雞、炸物、碳烤類~ 而且是可以內用。'}
    shop20 = {'name': '鴉片粉圓', 'Introduction': '鴉片粉圓1973年成立，從新北市板橋發跡，從一碗3元開始，這家店名由來，是因有客人吃了，稱就像抽鴉片一樣會上癮，因此得名。'}
    shop21 = {'name': '鷹流東京豚骨拉麵_極匠', 'Introduction': '鷹流東京豚骨拉麵-極匠店內用餐空間也非常的小，只有吧檯座位，約莫不到20個座位。'}
    shop22 = {'name': '尖蚪', 'Introduction': '延續了寶藏巖富含歷史足跡的建築風格，店內不只氣氛好東西又好吃，還會跟藝術家合作展覽，在一波網美咖啡廳中顯得獨樹一格，是文青最愛的午茶首選'}
    shop23 = {'name': '心KOKORO食堂', 'Introduction': '心kokoro食堂的外觀帶點日系木質的設計，門口可以看到菜單和打卡送塔塔醬薯條的資訊。'}
    shop24 = {'name': '幸好沒錯過你_Master_K.',
              'Introduction': '羅斯福路巷弄中，幸好沒錯過你相較於左右幾間店面的招牌低調許多，日式風格的淡粉紅色招牌，寫著幸好沒錯過你，旁邊還有個愛心和小黑板，簡單但非常可愛。'}
    shop25 = {'name': '泰國小館', 'Introduction': '店內裝潢很居家感，不走華麗風，座位一二樓都有，上二樓的樓梯比較陡窄，需要注意。'}
    shop26 = {'name': '順園小館',
              'Introduction': '「順園小館」應該算是台大公館商圈知名的老餐館之一，從1986年開張至今，已經逾30歲，而在2018年底重新裝修改造，打造更優質的用餐環境及氛圍。'}
    shop27 = {'name': 'Bravo_Burger_發福廚房公館台大店',
              'Introduction': '公館店好像是今年初才新開幕的，所以餐廳裏的佈置裝潢都還蠻新的，位子比起其它兩家的分店好像也比較多一些，一、二樓層的客席坐位，加起來應該有50~60位左右。'}
    shops = [shop1, shop2, shop3, shop4, shop5, shop6, shop7, shop8, shop9, shop10,
         shop11, shop12, shop13, shop14, shop15, shop16, shop17, shop18, shop19, shop20,
         shop21, shop22, shop23, shop24, shop25, shop26, shop27]
    for i in range(27):
        if s == shops[i]['name']:
            n = shops[i]['name']
            info = shops[i]['Introduction']

    #print(info)
    return render(request, 'boardlist.html', locals())

