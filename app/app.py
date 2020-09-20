#!/usr/bin/env python
# -*- coding: 850 -*-
# -*- coding: utf-8 -*-

# Requirements (Python 2.7)
# pip install telepot
# pip install mysql-connector-python
# pip install python-dotenv
# pip install requests
# pip install myjdapi

from threading import Thread
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from dotenv import load_dotenv
from cStringIO import StringIO
import requests
import subprocess
import myjdapi
import os
import sys
import re
import time
import hashlib
from threading import Thread

load_dotenv()
TelegramToken1 = os.getenv("TELEGRAM_TOKEN_1")
TelegramToken2 = os.getenv("TELEGRAM_TOKEN_2")
TelegramID1 = os.getenv("TELEGRAM_ID_1")
TelegramID2 = os.getenv("TELEGRAM_ID_2")
dbhost = os.getenv("DatabaseHost")
dbuser = os.getenv("DatabaseUserPeliculas")
dbpassword = os.getenv("DatabasePasswordPeliculas")
database = os.getenv("DatabasePeliculas")
tabla1 = os.getenv("TablaPeliculas1")
tabla2 = os.getenv("TablaPeliculas2")
DirectorioDescargas = os.getenv("DirectorioDescargas")
DirectorioPeliculas = os.getenv("DirectorioPeliculas")
ExtensionPeliculas = os.getenv("ExtensionPeliculas")
UsernameDD = os.getenv("UsernameDD")
PasswordDD = os.getenv("PasswordDD")
BaseUrlDD = os.getenv("BaseUrlDD")
UserMyJD = os.getenv("MyJDownloaderUser")
PasswordMyJD = os.getenv("MyJDownloaderPassword")
MyJDDevice = os.getenv("MyJDDevice")

def telegram_alert(bot_message, bot_token, bot_chatID):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?parse_mode=html&disable_web_page_preview=True&chat_id=' + bot_chatID + '&text=' + bot_message
    response = requests.get(send_text)


def download_dd(URL, number):
    result = subprocess.check_output('curl -s -H "Cache-Control: no-cache" https://descargasdd.net/forumdisplay.php?f=' + str(URL) + ' | iconv -f ISO-8859-1 -t UTF-8 | grep -a "thread_title" | tail -n +' + str(number) + ' | grep "1080"', shell=True)
    download_list = StringIO(result)
    for films in download_list:
        Check1 = films.strip().split('>')
        Check2 = Check1[1].strip().split('<')
        TipoA = re.split('\| ([0-9]+) \|', Check2[0])
        TipoB = re.split('\(([0-9]+)\)', Check2[0])
        TipoC = Check1[1].strip().split('[')[0]
        Nombre = ""
        Anyo = ""
        global NombreDD
        global AnyoDD
        if len(TipoA) > 1:
            NombreDD=str(TipoA[0])
            AnyoDD=int(TipoA[1])
        elif len(TipoB) > 1:
            NombreDD=str(TipoB[0])
            AnyoDD=int(TipoB[1])
        else:
            NombreDD=str(TipoC)
            AnyoDD = "0000"
        NombreDD=NombreDD.split('(')[0].rstrip()
        NombreDD=NombreDD.replace("\'","")
        NombreDD=NombreDD.replace("¿","")
        NombreDD=NombreDD.replace("?","")
        NombreDD=NombreDD.replace(":"," -")
        EnlaceDD = Check1[0].strip().split('?t=')
        EnlaceDD = EnlaceDD[1].strip().split('&amp')
        EnlaceDD = int(EnlaceDD[0])
        check_database_dd(NombreDD, AnyoDD, EnlaceDD)


def insert_database_dd(nombre, anyo, enlace):
    try:
        connection = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        if anyo == 0000:
            telegram_alert("🔥 <b>Error [DescargasDD]</b> %0A No se ha encontrado ninguna fecha para la película <b>"+ NombreDD +"</b>.", TelegramToken1, TelegramID1)
        sql = "INSERT INTO " + tabla1 + " (enlace, nombre, anyo_pelicula, estado_pelicula, fecha) VALUES(%d,'%s',%d,1,SYSDATE())" % (enlace, nombre, int(anyo))
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    except:
        telegram_alert("🔥 <b>ERROR (Shenron)</b> %0A Ha sucedido un error al insertar un registro en la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)


def check_database_dd(nombre, anyo, enlace):
    try:
        connectioncheck = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "SELECT nombre FROM " + tabla1 + " WHERE nombre = '%s'" % (nombre)
        cursorcheck = connectioncheck.cursor()
        cursorcheck.execute(sql)
        result = cursorcheck.fetchone()
        if not result:
            insert_database_dd(str(nombre), int(anyo), int(enlace))
        cursorcheck.close()
        connectioncheck.close()
    except:
        telegram_alert("🔥 <b>Error Database (DescargasDD) [1]</b> %0A Ha sucedido un error al conectar con la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)


def check_database():
    try:
        connectioncheck = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "SELECT id,nombre,enlace,fecha FROM " + tabla1 + " WHERE estado_pelicula = 1"
        cursorcheck = connectioncheck.cursor()
        cursorcheck.execute(sql)
        result = cursorcheck.fetchall()
        for row in result:
            Nombre = row[1].encode("utf-8")
            Enlace = int(row[2])
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Nueva pelicula: " + Nombre)
            update_database(int(row[0]))
            notificacion(str(Nombre), str(Enlace))
        cursorcheck.close()
        connectioncheck.close()
    except:
        telegram_alert("🔥 <b>Error Database (DescargasDD) [2]</b> %0A Ha sucedido un error al conectar con la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)


def movie_on_plex(ID_Pelicula):
    try:
        connection = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "UPDATE " + tabla1 + " SET estado_pelicula = 5 WHERE id = %d" % (int(ID_Pelicula))
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    except:
        telegram_alert("🔥 <b>Error Database (Plex)</b> %0A Ha sucedido un error al actualizar un registro en la base de datos " + datase + ".", TelegramToken, TelegramID)
        sys.exit(1)


def update_download(ID_Pelicula):
    try:
        connection = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "UPDATE " + tabla1 + " SET estado_pelicula = 4 WHERE id = %d" % (ID_Pelicula)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    except:
        telegram_alert("🔥 <b>Error Database (DescargasDD)</b> %0A Ha sucedido un error al actualizar un registro en la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)

def move_movie(DirectorioPeliculaCompleto, ID_Pelicula, NombrePelicula, AnyoPelicula, NombreFichero, Subfolder):
    update_download(int(ID_Pelicula))
    try:
        print('['+time.strftime('%d/%m/%Y %H:%M:%S')+'] Moviendo la pelicula '+NombrePelicula+' ('+str(AnyoPelicula)+') a Plex.')
        if Subfolder != "":
            os.system('mv "'+DirectorioPeliculaCompleto+'/'+Subfolder+'/'+NombreFichero+'" "'+DirectorioPeliculas+'/'+NombrePelicula+' ('+str(AnyoPelicula)+').'+ExtensionPeliculas+'"')
        else:
            os.system('mv "'+DirectorioPeliculaCompleto+'/'+NombreFichero+'" "'+DirectorioPeliculas+'/'+NombrePelicula+' ('+str(AnyoPelicula)+').'+ExtensionPeliculas+'"')
        #os.system('rm -rf "'+DirectorioPeliculaCompleto+'"')
        movie_on_plex(int(ID_Pelicula))
    except:
        telegram_alert("🔥 <b>Error Moviendo Películas (DescargasDD)</b> %0A Ha sucedido un error al mover la película " + NombrePelicula + " a la carpeta de descargas de Plex.", TelegramToken1, TelegramID1)
        sys.exit(1)


def find_film(ID_Pelicula, NombrePelicula, AnyoPelicula):
    DirectorioPeliculaCompleto=str(DirectorioDescargas)+'/'+NombrePelicula+' ('+str(AnyoPelicula)+')'
    pattern = re.compile(r'^.*[.](mkv)$')
    if os.path.exists(DirectorioPeliculaCompleto):
            for folder in os.listdir(DirectorioPeliculaCompleto):
                    if os.path.isdir(os.path.join(DirectorioPeliculaCompleto+"/"+folder)):
                            for file in os.listdir(DirectorioPeliculaCompleto+"/"+folder):
                                if pattern.match(file):
                                    NombreFichero=file
                                    Subfolder=folder
                                    #move_movie(DirectorioPeliculaCompleto, ID_Pelicula, NombrePelicula, AnyoPelicula, NombreFichero, Subfolder)
                    else:
                            if pattern.match(folder):
                                    NombreFichero=folder
                                    #move_movie(DirectorioPeliculaCompleto, ID_Pelicula, NombrePelicula, AnyoPelicula, NombreFichero, "")


def check_download():
    try:
        connectioncheckdownload = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "SELECT id, nombre, anyo_pelicula FROM " + tabla1 + " WHERE estado_pelicula = 3"
        cursorcheckdownload = connectioncheckdownload.cursor()
        cursorcheckdownload.execute(sql)
        result = cursorcheckdownload.fetchall()
        for row in result:
            ID_Pelicula=int(row[0])
            NombrePelicula=row[1]
            AnyoPelicula=int(row[2])
            find_film(ID_Pelicula, NombrePelicula, AnyoPelicula)
        cursorcheckdownload.close()
        connectioncheckdownload.close()
    except:
        telegram_alert("🔥<b>Error Database (DescargasDD) [3]</b> %0A Ha sucedido un error al conectar con la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)


def update_database(id):
    try:
        connection = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "UPDATE " + tabla1 + " SET estado_pelicula = 2 WHERE id = %d" % (id)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
    except:
        telegram_alert("🔥 <b>Error Database (DescargasDD)</b> %0A Ha sucedido un error al actualizar un registro en la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)


def myjdownloader(nombre, anyo, url_download):
    jd=myjdapi.Myjdapi()
    jd.connect(UserMyJD,PasswordMyJD)
    jd.update_devices()
    device=jd.get_device(MyJDDevice).linkgrabber.add_links([{
    "autostart" : True,
    "packageName" : str(nombre)+" ("+str(anyo)+")",
    "links" : url_download
    }])


def scrapy_url(enlace, nombre, anyo):
    with requests.Session() as su:
        username = str(UsernameDD)
        password = str(PasswordDD)
        base_url = str(BaseUrlDD)
        urlDD = str(BaseUrlDD)+'/showthread.php?t='+str(enlace)
        su.post(base_url + '/login.php?do=login', {
            'vb_login_username': username,
            'vb_login_password': password,
            'vb_login_md5password': hashlib.md5(password.encode()).hexdigest(),
            'vb_login_md5password_utf': hashlib.md5(password.encode("utf-8")).hexdigest(),
            'cookieuser': 1,
            'do': 'login',
            's': '',
            'securitytoken': 'guest'
    })
    base_page = su.get(urlDD)
    linkcount = 0
    download_list = StringIO(base_page.content)
    for line in download_list:
        if re.search(r'https://mega.nz', line) is not None:
            CheckDownload = line.strip().split('>')
            if linkcount == 0:
                url_download = CheckDownload[1]
                linkcount = 1
            else:
                url_mega = CheckDownload[0]
                url_download = url_download+" "+url_mega
    try:
        last_line = ""
        download_list = StringIO(base_page.content)
        for line in download_list:
            if url_mega in last_line:
                last_line = line
                CheckDownload = line.strip().split('<')
            last_line = line
        url_uploaded = CheckDownload[0]
        url_download = url_uploaded+" "+url_download
        myjdownloader(nombre, anyo, url_download)
    except:
        telegram_alert("🔥 <b>Error Descarga (DescargasDD)</b> %0A Ha sucedido un error al intentar descargar la película <b><a href='https://descargasdd.net/showthread.php?t=" + str(enlace) + "'>" + str(nombre) + "</a></b>.", TelegramToken1, TelegramID1)


def scrapy_btn(enlace, nombre, anyo):
    with requests.Session() as sb:
        username = str(UsernameDD)
        password = str(PasswordDD)
        base_url = str(BaseUrlDD)
        urlDD = str(BaseUrlDD)+'/showthread.php?t='+str(enlace)
        sb.post(base_url + '/login.php?do=login', {
            'vb_login_username': username,
            'vb_login_password': password,
            'vb_login_md5password': hashlib.md5(password.encode()).hexdigest(),
            'vb_login_md5password_utf': hashlib.md5(password.encode("utf-8")).hexdigest(),
            'cookieuser': 1,
            'do': 'login',
            's': '',
            'securitytoken': 'guest'
        })
    base_page = sb.get(urlDD)
    var = 0
    download_list = StringIO(base_page.content)
    for line in download_list:
        if var == 0:
            if re.search(r'post_thanks.php\?do\=post_thanks_add', line) is not None:
                var = 1
                Check = line.strip().split('\"')
                brutedata = Check[1].strip().split('=')
                p = brutedata[2].strip().split('&amp')[0]
                securitytoken = brutedata[3]
    with requests.Session() as s:
        username = str(UsernameDD)
        password = str(PasswordDD)
        base_url = str(BaseUrlDD)
        urlDD = str(BaseUrlDD)+'/showthread.php?t='+str(enlace)
        s.post(base_url + '/login.php?do=login', {
            'vb_login_username': username,
            'vb_login_password': password,
            'vb_login_md5password': hashlib.md5(password.encode()).hexdigest(),
            'vb_login_md5password_utf': hashlib.md5(password.encode("utf-8")).hexdigest(),
            'cookieuser': 1,
            'do': 'login',
            's': '',
            'securitytoken': 'guest'
        })
        s.post(base_url + '/post_thanks.php?do=post_thanks_add', {
            'do': 'post_thanks_add',
            'using_ajax': 1,
            'p': p,
            'securitytoken': securitytoken,
        })
    scrapy_url(enlace, nombre, anyo)


def notificacion(nombre, enlace):
    MensajeBot="🎬 <b>Nueva película</b> \n <a href='https://descargasdd.net/showthread.php?t=" + str(enlace) + "'>" + str(nombre) + "</a>"
    bot.sendMessage(TelegramID2, MensajeBot, parse_mode='HTML', disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Sinopsis",url="https://descargasdd.net/showthread.php?t="+enlace)],
        [InlineKeyboardButton(text="Descargar",callback_data=enlace)]
        ]
    ))


def boton(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    try:
        connection = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
        sql = "SELECT estado_pelicula, descripcion, " + tabla1 + ".nombre, anyo_pelicula FROM " + tabla1 + " INNER JOIN " + tabla2 + " ON " + tabla1 + ".estado_pelicula = " + tabla2 + ".id WHERE enlace = %d" % (int(query_data))
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        nombre = str(result[2].encode("utf-8"))
        estado = int(result[0])
        anyo = str(result[3])
        enlace = str(query_data)
        mensaje = str(result[1].encode("utf-8"))
        if result[0] == 2:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] "+str(msg['from']['first_name']) + " quiere descargar la película [" + nombre + "].")
            try:
                connection = mysql.connector.connect(host=dbhost, user=dbuser, password=dbpassword, database=database)
                sql = "UPDATE " + tabla1 + " SET estado_pelicula = 3 WHERE enlace = %d" % (int(enlace))
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                cursor.close()
                connection.close()
            except:
                telegram_alert("🔥 <b>Error Database (DescargasDD)</b> %0A Ha sucedido un error al actualizar un registro en la base de datos " + database + ".", TelegramToken1, TelegramID1)
                sys.exit(1)
            scrapy_btn(enlace, nombre, anyo)
            telegram_alert("🎬 <b>Descargar película</b> %0A <b>" + str(msg['from']['first_name']) + "</b> quiere descargar la siguiente película: %0A <a href='https://descargasdd.net/showthread.php?t=" + str(query_data) + "'>" + nombre + "</a>", TelegramToken1, TelegramID1)
        elif result[0] == 3:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] "+str(msg['from']['first_name']) + " quiere descargar la película [" + str(nombre) + "], pero ya está en proceso de descarga.")
        elif result[0] == 4:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] "+str(msg['from']['first_name']) + " quiere descargar la película [" + str(nombre) + "], pero ya está descargada.")
        elif result[0] == 5:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] "+str(msg['from']['first_name']) + " quiere descargar la película [" + str(nombre) + "], pero ya se encuentra en Plex")
        else:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Estado de la película [" + nombre + "] desconocido.")
            mensaje = "Se ha producido un error."
        cursor.close()
        connection.close()
    except:
        telegram_alert("🔥 <b>Error Database (DescargasDD)</b> %0A Ha sucedido un error al actualizar un registro en la base de datos " + database + ".", TelegramToken1, TelegramID1)
        sys.exit(1)        
    bot.answerCallbackQuery(query_id, text=mensaje)


bot = telepot.Bot(TelegramToken2)
bot.message_loop({'chat': notificacion, 'callback_query': boton})

#time.sleep(300)

def check_dd():
    while 1:
        Hora = int(time.strftime("%H"))
#        if 8 <= Hora <= 22:
        download_dd(143, 5)
        download_dd(324, 0)
        time.sleep(3600)

def check_db():
    while 1:
        check_database()
        time.sleep(60)

def check_dw():
    while 1:
        check_download()
        time.sleep(300)

check_dd = Thread(target=check_dd)
check_db = Thread(target=check_db)
check_dw = Thread(target=check_dw)

check_dd.start()
check_db.start()
check_dw.start()
