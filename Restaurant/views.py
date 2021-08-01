from urllib import request
from django.shortcuts import render
import json

# Create your views here.
def Delicacy_datas():

    datas = {"享你好酒不見":"100台北市中正區汀州路三段160巷;3.9;550",
            "夢駝鈴咖啡餐廳":"100台北市中正區汀州路三段108號;3.7;400",
            "窩巷弄":"10090台北市中正區羅斯福路四段78巷1弄11號;3.9;400",
            "貳樓餐廳 Second Floor Cafe 公館店":"100台北市中正區羅斯福路三段316巷9弄7號;4.1;160",
            "三米三小館":"100台北市中正區羅斯福路三段286巷4弄12號;4.3;140",
            "初牛 台北公館店":"100台北市中正區汀州路三段169號;4.2;250",
            "易牙居餐廳":"100台北市中正區羅斯福路三段286巷16號;3.9;120",
            "站食可以":"100台北市中正區羅斯福路四段24巷12弄7號;4.7;280",
            "寶島肉圓店":"116台北市文山區羅斯福路五段136號;4.2;1.5",
            "阿玉水餃 (生水餃專賣店)":"106台北市大安區辛亥路二段217號;4.3;1.8",
            "拾年腸粉/公館美食":"100台北市中正區水源路27巷19號;4.9;900",
            "El Sabroso Mexican Food":"100台北市中正區汀州路三段107號之一;4.2;350",
            "海邊的卡夫卡 Kafka by the Sea":"10090台北市中正區羅斯福路三段244巷2號2樓;4.5;110",
            "INTERMISSION 中場休息 Cafe'":"100台北市中正區汀州路三段149號1樓;4.9;210",
            "辛殿麻辣鍋|公館店":"100台北市中正區羅斯福路三段316巷9弄1號;3.9;190",
            "池先生 Kopitiam (公館店)":"100台北市中正區羅斯福路三段284巷10號;4.2;130",
            "麥當勞-台北新生店":"106台北市大安區新生南路三段88之2號;3.9;350",
            "麥當勞-台北台大店":"106台北市大安區羅斯福路四段1號1樓;3.3;850",
            "炸手指/公館宵夜":"100台北市中正區羅斯福路三段316巷8弄4號;4.5;170",
            "鴉片粉圓":"No. 191新生街中和區新北市235號;3.7;7.1",
            "鷹流東京豚骨拉麵-極匠":"100台北市中正區汀州路三段104巷4號;4.0;350",
            "尖蚪":"100台北市中正區汀州路三段230巷57號;4.5;1.3",
            "心KOKORO食堂/台北日式料理/公館美食/公館小吃/公館餐廳/公館日式料理/公館壽司":"100台北市中正區汀州路三段104巷11弄15號一樓;4.3;450",
            "幸好沒錯過你 Master K.":"100台北市中正區羅斯福路四段78巷1弄5號;4.0;450",
            "泰國小館":"100台北市中正區汀州路三段219號;3.9;400",
            "台北美食/公館美食/酸菜白肉鍋/中式熱炒/聚餐/聚會/刀削麵/豆沙鍋餅/北方麵食/順園小館":"100台北市中正區汀州路三段281號;4.0;700",
            "Bravo Burger發福廚房公館台大店":"100台北市中正區羅斯福路四段44之1號2樓;4.0;240"

            }

    return render(request, 'detail.html', datas)