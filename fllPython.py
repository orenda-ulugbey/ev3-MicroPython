#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


ev3 = EV3Brick()


motor = Motor(Port.B) # yanda motorlardan birine isim verip B portuna atadım
motor2 = Motor(Port.C) # yanda motorlardan diğerine de isim verip C portuna atadım

robot = DriveBase(motor, motor2, wheel_diameter=55.5, axle_track=104) 
# yukarıda robotun iki tekerleğini de aynı anda kullanılabilmesi için DriveBase modülünü kullandık
# ilk boşluğa sol motoru diğerine sağ motoru ondan sonrakine tekerlek çapını 
# ve en sondakine tekerlekler arası mesafeyi giriyoruz
# artık robotun tekerleklerini robot ismi altında çalıştırabileceğiz

gs = GyroSensor(Port.S2) # burada gyro sensöre ad verdik ve port 2 ye atadık
iss = InfraredSensor(Port.S3) # burada mesafe sensörüne ad verdik ve port 3 e atadık
cs = ColorSensor(Port.S4) # burada renk sensörüne ad verdik ve port 4 e atadık
ts = TouchSensor(Port.S1) # burada da touch sensöre ad verdik ve port 1 e atadık

# yukarıda tüm tanımlama işlemlerini yaptık isterseniz daha fazla motor ekleyebilir 
# veya sensörleri falan değiştirebilirsiniz

ev3.speaker.beep() # ben burada tanımla işlemleri tamamlandımı emin olmak için robota ses çıkartıyorum


"""
tek motor kullanımı
"""
# ev3 ün tek motorunun çalıştırılmasının farklı yolları var

motor.run(200) #burada motor 200 hızla "motor.stop()" yapılmadıkça döner
# bunu döngü içinde kullanırsanız döngüyü durdurmanız da motoru durdurur

motor.stop()

while motor.angle() < 500:
    motor.run(100)

# burada motor un derecesi 500 ü geçince robot durur çünkü döngü biter

motor.run_time(200, 10) # burada motor 200 hızla 10 mili saniye döner eğer bir döngüde başka bir koşul yoksa

motor.run_angle(200, 90) # burada motor 200 hızla 90 derece döner eğer bir döngüde başka bir koşul yoksa
# burda motor verdiğimiz dererece kadar döner

motor.run_target(200, 90) # burada motor 200 hızla hedef açıya döner 90 dereceye geldiğinde durur
#burada motor verdiğimiz dereceye ulaşınca durur

motor.track_target(90)
# hedef açıya olabildiğince hızlı hareket eder. Hedef açıyı sürekli olarak değiştirmek istiyorsanız bu yöntem kullanışlıdır.

motor.reset_angle(0) # yanda motorumuzun derecesini sıfırladık bunu gerekli durumlarda kullanabilirsiniz

# yukarıda tek bir motorun kullanılış şekillerini yazdım bunları döngülere sokarak farklı şekillerde kullanabilirsiniz
# bunları fonksiyon içinde de kullanabiliriz

def ileri(a):
    motor.reset_angle(0)
    motor.run_angle(200, a)
# yukarıda bir ileri gitme fonksiyonu oluştuduk
# ilk başta motorun derecesini sıfırlıyor sonra da verdiğimiz değer kadar ilerlemesini sağlıyor

ileri(90) # şeklinde kullanılır motor 90 derece döner


"""
çift motor ve DriveBase kullanımı
"""

# çift motor kullanımını aşağıdaki gibi yapabiliriz
while True:
    motor.run(130)
    motor2.run(130)
# yukarıda iki motor da aynı anda çalışır
# istersek buna koşul ekleyip motorları durdurabiliriz
while ts.pressed()==False:
    motor.run(130)
    motor2.run(130)
# yukarıda robot ileri gider eğer ts ye dokkunulursa durur
# bunu sonradan yazacağım


# DriveBase modülünü en başta kütüpahaneden alıp tanımlamıştık
# bu modül iki motorun aynı anda kullanılıp ileri geri gitme ve dönme hareketlerini kullanmamızı sağlar
# birkaç farklı kullanımı vardır

robot.straight(100) # yanda robotumuz 100 mm ileri gider

robot.drive_time(300, 0, 3000) # yanda robot 300 hızla 3 saniye gider
# ortadaki 0 değeri robotun ileri gitmesini sağlar eğer + bir değer olsaydı sağa doğru giderdi - için ise sola

robot.drive_time(0, 90, 3000) # burada robot 90 hızla 3 saniye döner

robot.turn(90) # yanda robot 90 derece açı yapacak şekilde döner

robot.drive(200,0) # yanda robot 200 hızla biz durdurana kadar döner
# 0 yine düz gitmesini sağlar

robot.drive(0, 80) # yanda robot sağa doğru biz durdurana kadar 80 hızla döner
# gelecekte bunu gyro da kulanacağız

robot.stop() # yandaki gibi durdurulabilir

robot.distance() # robotun kaç mm ilerlediğini gösterir

robot.reset() # roboton ilerleme mm sini ve derecesini sıfırlar

"""
sensörler
"""
# yukarıda sensörlerin nasıl tanımlandığını göstermiştim
# şimdi nasıl kullanıldıklarını göstericem

"""
TouchSensor
"""
# bu sensör bool tipinden yani true veya false olarak algılar
# sensör basılıysa True değilse False
# yukarıda bu sensöre ts ismini vermiştim
# tek bir kullanımı vardır

ts.pressed() # yandaki kod sensörün basılıp basılmadığına bakar

# örnek kod

while True:
    robot.drive(200,0)
    while ts.pressed() == True:
        robot.stop()
        robot.straight(-100)
        robot.turn(90)
        

# yukarıdaki kodda robot ts ye basılana kadar ileri gider 
# ts ye basılınca robot durur ve geri doğru 10 cm gider
# en son da 90 derece sağa döner

"""
color sensor
"""
cs.color()
# bu kullanım Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN ya da None olarak algılar
# kısaca renkleri algılar
# örnek kod

while True:
    robot.drive(200,0)
    if cs.color() == Color.BLACK:
        break
# burada robot ileri gider
# eğer cs siyah algılarsa döngü biter ve robot durur

cs.ambient()
# etraftaki ışık yoğunluğunu yüzdelik olarak algılar
# 0 = karanlık, 100 = aydınlık

while True:
    wait(10)
    while cs.ambient() < 20:
        ev3.speaker.beep()
# yukarıda robot bekler
# eğer ışık seviyesi yüzde yirminin altına düşerse robot bip sesi çıkarmaya başlar

cs.reflection()
# bu kullanımda renk sensörü ışığın yansımasını algılar
# 0 = az yansıma, 100 = çok yansıma
# örnek kod

while True:
    motor.run(130)
    motor2.run(cs.reflection() * 5) 
    

# yukarıdaki kodda robot sola kavisli ilerler siyah çizgiyi görünce sağa kavisli ilerler çizgiden çıkınca yine sola gider
# kısaca çizgiyi izler
# bunun sebebi ilk başta yansıma fazla olduğu için motor2 daha hızlı döner ve robot sola kavisli gider
# siyah çizgiyi görünce robot tam siyah çizginin ortasında 26 dan düşük bir değer görüyor çünkü yansıma az
# değer 26 dan yani 130\5 ten düşük olunca motor daha hızlı döner ve siyah la beyazın arası olan ara çizgiye gelince
# değer tam 26 gibi olur ve robot düz gider yani çizgiyi izler
# robot çizgiden çıkınca aynı şeyler tekrarlanır

# şimdi cs ile ilgili bilgilerden biriyle bir fonksiyon yazacam

def siyah(c):
    while True:
        robot.drive(c,0)
        if cs.color() == Color.BLACK:
            break
# artık robotumuz siyah(200)yazarsak 200 hızla siyahı göene kadar ilerleyecek ve siyahı görünce duracak
siyah(300)#robot 300 hızla gider

"""
mesafe densörü (InfraredSensor)
"""
# bu sensör kızıl ötesi ışınları kullanarak 70 cm ye kadar uzaklık ölçebilir
# 100 = uzak, 0 = yakın
iss.distance()# yandaki şekilde kullanılır yanda sensörümüz yüzde olarak uzaklığı ölçer

while True:
    print(iss.distance())
# yukarıda robot biz durdurana kadar ölçtüğü değerleri ekrana yazdırır

while True:
    robot.drive(300, 0)
    while iss.distance() < 25:
        robot.stop()
        robot.straight(-300)
        robot.turn(120)

# yukarıdaki kodda bir engelden kaçan yaptık
# ilk önce robot 300 hızla ileri gider eğer iss 25 ten daha yakın bir şey algılarsa
# robot durur geri gider ve dönüş yapar sonra aynı şeyler tekrar olur

# bu sensörü başka şekillerde de kulana biliriz ama bu size kalmış


"""
ultrasonik sensör (UltrasonicSensor)
"""
# bu sensör bende olmadığı için hakkında çok bir şey yazamicam veya yazdıklarımı kontrol edemicem
# eğer sensör sizde varsa yazdıklarımı test edebilir ve üstüne yeni şeyler ekleyebilirsiniz
# ses dalgalarını kullanarak nesne ile arasındaki mesafeyi ölçer
# yukarıda tanımlamadım çünkü ev3 te sensörler için 4 boşluk var ve ben dördünü de kullandım
# ama tanımlanışı aynı   us = UltrasonicSensor(Port.S2)
# burada sensörü port 2 ye atama kodunu yazdım
# bu sensörün iki kullanımı var

us.distance() # yandaki kullanımı mesafe sensörüyle aynı sadece mm cinsinden ölçüm yapar

while True:
    print(us.distance())
# yukarıda mm ölçen bir kod yazdık mm yi sürekli olarak ekrana yazdırır
# zaten kullanım şekli yukarıdakiyle aynı bunun için örnek yazmicam 

us.presence()  # Ultrasonik sesleri algılayarak diğer ultrasonik sensörlerin varlığını kontrol eder.
# bunu nerede kullanırsınız bilmiyorum hiç denemedim ama yine de yazdım umarım işe yarar

"""
gyro sensörü (GyroSensor)
"""
# bu sensör dereceleri ölçer 
# diğer dönüş şekilleri sorun çıkartabilir ama gyro ile düzgün ve takılmadan dönebiliriz
# eğer ağırlık taşıyorsak robotun düz gitmesini sağlayabiliriz 

gs.angle() # yandaki kodda gs robotun derecesini ölçer
# şimdi bununla nasıl dönüş yapacağımıza bakalım

while gs.angle() < 85:
    robot.drive(0,80)

# yukarıdaki kodda robot sürekli gs nin derecesini ölçer ve aynı zamanda sağa doğru döner
# gs nin derecesi 85 e eşit veya 85 ten büyük olduğu an robotun dönmesi durur
# çünkü while döngüsü biter

# bunun sola dönüş şeklide şöyledir

while gs.angle() > -85:
    robot.drive(0,-80)
# burada da robot gs nin derecesi -85 ten büyükken robot sola doğru dner 
# eğer gs nin derecesi -86 gibi yani -85 ten küçük olursa döngü biter ve robot durur

# şimdi bunları biraz kısaltmayı deneyelim
def right(r):
    while gs.angle() < r:
        robot.drive(0,80)

def left(l):
    while gs.angle() > l:
        robot.drive(0,-80)
# artık robotumuz
right(90) # yazınca sağa 90 derece
left(-45) # soldaki 45 dereceye dönecek

# eğer robot -90 dayken ona right(90) komutunu verirseniz 180 derece döner çünkü gs başladığı konumu 0
# olarak kabul eder yani siz bir x y ekseni üzerindeymişsiniz gibi ve robot onon tam ortasında 
# ve başlangıç noktası da sıfır

# şimdi robotun sağa mı sola mı gideceğine kendi karar vermesini sağlayan bir kod yazalım
aci = 90
while True:
    if gs.angle() < aci:
        robot.drive(0, 30)
    elif gs.angle() > aci:
        robot.drive(0, -30)
    elif gs.angle() == aci:
        robot.stop()
        break
# yukarıda eğer gs nin derecesi 90 dan küçükse robot sağa doğru döner ve derece 90 la eşit olunca durur
# eğer gs nin derecesi 90 dan büyükse robot sola doğru döner ve derece 90 la eşit olunca durur
# isterseniz bu kodu geliştirebilirsiniz

# şimdi gs yi nasıl sıfırlayacağımızı göstereceğim
gs.reset_angle(0) 
# yukarıda gyro nun derecesini sıfırladım isterseniz 0 yerine başka bir
# sayı yazıp gyro yu o sayıya programlayabilirsiniz

# şimdi gyro ile nasıl düz gidebileceğimizi göstericem
while True:
    an = gs.angle()
    d = (an * -10)
    robot.drive(200, d)
# burada robot biz ittirsek bile düz gitmeye devam eder
# bunun sebebi ilk başta robot 0 dereceyle ilerlemeye başlar o*-10= 0 olduğu için robot düz gider
# eğer robotun önünü sağa doğuru ittirirsek gs nin değeri + bir değer olur
# atıyorum gs nin değeri +5 bu sayıyla -10 u çarparsak -50 eder yani robot sola kavisli gider
# robot sola kavisini yavaşça azaltır çünkü sayılar 4 3 2 ve 1 değerlerinde devam eder ve en sonunda
# robot 0 değerine tekrar ulaştığında düz gitmeye devam eder
