# Orenda Robotik Takımı - FLL Python Eğitim Dökümanı
"""
Kütüphane, Motor ve Sensörlerin Tanımlanması
"""
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

solMotor = motor(Port.B)  # Sol motoru tanımlayıp B portuna atadım.
sagMotor = motor(Port.C)  # Sağ motoru tanımlayıp C portuna atadım.
robot = DriveBase(solMotor, sagMotor , wheel_diameter=55.5, axle_track=104)
# Yukarıda kullandığımız DriveBase modülü sayesinde iki motorumuzu aynı anda kullanabiliyoruz.
# DriveBase'in bizden istediği parametreler sırasıyla; "Sol Motor", "Sağ Motor", "Tekerlek Çapı" ve "Tekerlekler Arası Mesafe"
# DriveBase modülünü "robot" olarak tanımladığımız için kodun devamında "robot" yazarak DriveBase modülünün fonksiyonlarını kullanabiliyoruz.

ts = TouchSensor(Port.S1)  # Dokunma sensörünü "ts" olarak tanımlayıp Port1'e atadım.
gs = GyroSensor(Port.S2)  # Eksen sensörünü "gs" olarak tanımlayıp Port2'ye atadım.
iss = InfraredSensor(Port.S3)  # Mesafe sensörünü "iss" olarak tanımlayıp Port3'e atadım.
cs = ColorSensor(Port.S4)  # Renk sensörünü "cs" olarak tanımlayıp Port4'e atadım.

# Yukarıda örnek olarak verilen değerler bizim robotumuz için geçerlidir. İsteğe göre daha fazla motor ekleyip çıkarma, Farklı sensörler bağlama gibi işlemler yapılabilir.

ev3.speaker.beep()  # Her şeyin yolunda gittiğinden, tanımlamalarda bir sıkıntı olup olmadığından emin olmak için bu işlemler bittiğinde EV3 üzerinden ses çıkartıyorum.

"""
Tek Motor Kullanımı
"""
# Motor kullanım örnekleri için sadece sol motoru kullanacağım.

solMotor.run(200)  # Burada motor 200 hızla "motor.stop()" fonksiyonu kullanılmadıkça döner.

while solMotor.angle() < 360: # Burada motorun derecesi 360'ı (Tam Bir Tur) geçince döngü bittiği için motor durur.
    solMotor.run(100)

solMotor.run_time(200, 10)  # Burada motor 200 hızla 10 milisaniye döner. (Eğer döngüde başka bir koşul yoksa)

solMotor.run_angle(200, 90)  # Burada motor 200 hızla 90 derece döner. (Eğer döngüde başka bir koşul yoksa)

solMotor.run_target(200, 90)  # Burada motor 200 hızla hedef açıya gelene kadar döner. Açıyı manevradan önce resetlemediğimiz durumlarda bu fonksiyonu kullanıyoruz.

solMotor.track_target(90)  # Hedef açıya olabildiğince hızlı hareket eder. Hedef açıyı sürekli olarak değiştirmek istiyorsanız bu yöntem kullanışlıdır.

motor.reset_angle(0)  # Motorun açısını resetlemek için bu fonksiyonu kullanıyoruz.

motor.stop() # Motoru durdurmak için bu fonksiyonu kullanıyoruz.

# Yukarıda anlatılan fonksiyonların hepsini döngülere sokarak daha efektif kullanabiliriz.
# Ayrıca bu komutları kendi yazdığımız fonksiyonların içinde de kullanabiliriz

def ileri(a):  # Burada ileri gitme fonksiyonu oluştuduk. Başta motorun derecesini sıfırlıyor sonra da verdiğimiz değer kadar ilerlemesini sağlıyor
    motor.reset_angle(0)
    motor.run_angle(200, a)

ileri(90)  # Bu kullaınmda motor 90 derece döner.

"""
Çift Motor ve DriveBase Kullanımı
"""

while True:  # Yukarıda iki motor da aynı anda çalışır. İstersek buna koşul ekleyip motorları durdurabiliriz.
    solMotor.run(130)
    sagMotor.run(130)

# Şimdi en başta tanımladığımız DriveBase modülünün birkaç farklı kullanımını göreceğiz.

robot.straight(100)  # Bu kullanımda robotumuz 100mm ileri gider.

robot.drive_time(300, 0, 3000) # Bu kullanımda ise robot 300 hızla 3 saniye gider. Ortadaki 0 değeri robotun ileri gitmesini sağlar. Eğer + bir değer olsaydı sağa, - bir değer olsaydı sola giderdi.

robot.drive_time(0, 90, 3000)  # Burada robot 90 hızla 3 saniye sağa döner.

robot.turn(-90)  # Yanda robot -90 derece açı yapacak şekilde sola döner.

robot.drive(200, 0)  # Burada robot 200 hızla biz durdurana kadar döner. 0 tekrar düz gitmesini sağlar.

robot.stop()  # Robotun durmasını sağlar.

robot.distance()  # Robotun kaç "mm" ilerlediğini gösterir.

robot.reset()  # Robotun ilerleme değerini ve derecesini sıfırlar.

"""
Sensörler
"""
# Yukarıda sensörlerin nasıl tanımlandığını göstermiştim. Şimdi nasıl kullanıldıklarını göstereceğim.

"""
* TouchSensor
"""

# Bu sensör bool tipi girdi alır. Yani girilen değer "True" veya "False" olmak zorundadır.

ts.pressed()  # Yandaki fonksiyon sensörün basılıp basılmadığına bakar. Sensörün tek kullanımı bu şekildedir

# Şimdi bunu bir döngü içinde göstereceğim.

while True:  # Yandaki döngüde robot sensöre "True" değer girilene karar ileri gider. Sensör "True" değer alınca robot durur ve geri doğru 10 cm ileri ve 90 derece sağa gider.
    robot.drive(200, 0)
    while ts.pressed() == True:
        robot.stop()
        robot.straight(-100)
        robot.turn(90)

"""
* ColorSensor
"""

# Bu sensör Color.BLACK, Color.BLUE, Color.GREEN, Color.YELLOW, Color.RED, Color.WHITE, Color.BROWN ya da None olmak üzere toplam 8 çıktı verir.

cs.color() # Renk algılama özelliği yandaki gibi kullanılır
# Ayrıca bu sensörü de döngülerde kullanabiliriz.

while True:  # Burada robot ileri gider. Eğer sensör siyah renk algılarsa döngü biter ve robot durur.
    robot.drive(200, 0)
    if cs.color() == Color.BLACK:
        break

cs.ambient() # Işık seviyesi algılama özelliği bu şekilde kullanılır. 0 = karanlık, 100 = aydınlık.

while True:  # Bu döngüde robot bekler. Eğer ışık seviyesi yüzde yirminin altına düşerse robot ses çıkarmaya başlar.
    wait(10)
    while cs.ambient() < 20:
        ev3.speaker.beep()

cs.reflection()  # Bu kullanımda renk sensörü ışığın yansımasını algılar, 0 = az yansıma, 100 = çok yansıma.

while True:              # Yandaki örnekte robot sola kavisli ilerler siyah çizgiyi görünce sağa kavisli ilerler çizgiden çıkınca yine sola gider.
    solMotor.run(130)    # Bunun sebebi ilk başta yansıma fazla olduğu için sagMotor daha hızlı döner ve robot sola kavisli gider.
    sagMotor.run(cs.reflection() * 5)

# Renk Fonksiyonu ile Örnek Fonksiyon

def siyah(c):  # Artık "siyah(200)" yazarsak robotumuz 200 hızla siyahı göene kadar ilerleyecek ve siyahı görünce duracak.
    while True:
        robot.drive(c, 0)
        if cs.color() == Color.BLACK:
            break

siyah(300)  # Bu kullanımda robot 300 hızla gider.

"""
* Mesafe Sensörü (InfraredSensor)
"""
# Mesafe sensörü, kızıl ötesi ışınlar sayesinde 70cm mesafeye kadar ölçüm yapabiliyor.

iss.distance()  # Yandaki şekilde kullanılır yanda sensörümüz yüzde olarak uzaklığı ölçer

while True:  # Bu örnekte robot, biz durdurana kadar ölçtüğü değerleri ekrana yazdırır
    print(iss.distance())

while True:  # Yukarıdaki kodda bir engelden kaçan yaptık. İlk önce robot 300 hızla ileri gider eğer iss 25 ten daha yakın bir şey algılarsa robot durur geri gider ve dönüş yapar sonra aynı şeyler tekrar olur.
    robot.drive(300, 0)
    while iss.distance() < 25:
        robot.stop()
        robot.straight(-300)
        robot.turn(120)

"""
Eksen Sensörü (GyroSensor)
"""

# Bu sensör dereceleri ölçer. Diğer yöntemlere göre daha stabil çalıştığı için robotumuzda dönüşlerimizi "Gyro Sensor" sayesinde yapıyoruz.

gs.angle()  # Yandaki örnekte sensör robotun derecesini ölçer.

while gs.angle() < 85:  # Yandaki örnekte robot sürekli sensörün derecesini ölçer ve aynı zamanda sağa doğru döner. Sensörün derecesi 85'e eşit veya 85'ten büyük olduğu an robotun dönmesi durur.
    robot.drive(0, 80)

# Aynı örneğin sola dönüş hali;

while gs.angle() > -85:
    robot.drive(0, -80)

# Bu kodları daha kullanışlı hale getirmek için kendi fonksiyonlarımızı yazıyoruz.

def right(r):
    while gs.angle() < r:
        robot.drive(0, 80)

def left(l):
    while gs.angle() > l:
        robot.drive(0, -80)

right(90)  # Artık bu kullanımda sağa doğru 90 derece,
left(-45)  # Bu kodda ise sola 45 derece dönüyor.

# Eğer robotun daha önceki konumu sıfırlamadıysak robot yeni gelen değeri onun üstüne ekleyerek dönecektir.

# Şimdi robotun kendi yönünü belirliyeceği bir kod yazalım.

aci = 90
while True: # Bu örnekte eğer sensörün derecesi 90'dan küçükse robot sağa doğru döner ve derece 90'la eşit olunca durur. Eğer sensörün derecesi 90'dan büyükse robot sola doğru döner ve derece 90'la eşit olunca durur.
    if gs.angle() < aci:
        robot.drive(0, 30)
    elif gs.angle() > aci:
        robot.drive(0, -30)
    elif gs.angle() == aci:
        robot.stop()
        break

gs.reset_angle(0) # Bu fonksiyon sayesinde sensörü sıfırlayabilir veya istediğimiz dereceye ayarlayabiliyoruz.

while True:                 # Bu örnekte robot biz dışarıdan müdahale etsek bile düz gitmeye devam eder. Bunun sebebi ilk başta robot 0 dereceyle ilerlemeye başlar, o*-10= 0 olduğu için robot düz gider.
    an = gs.angle()         # Eğer robotun önünü sağa doğuru ittirirsek sensörün değeri pozitif bir değer olur. Örneğin sensörün değeri +5 bu sayıyla -10 u çarparsak -50 eder yani robot sola doğru gider.
    d = (an * -10)          # Robot sola kavisini yavaşça azaltır çünkü sayılar 4, 3, 2 ve 1 değerlerinde devam eder ve en sonunda robot 0 değerine tekrar ulaştığında düz gitmeye devam eder.
    robot.drive(200, d)
