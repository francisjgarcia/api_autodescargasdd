#!/usr/bin/env python

from threading import Thread
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import mysql.connector
from dotenv import load_dotenv
import requests
import os
import sys
import re
import time
import datetime
import hashlib
import myjdapi
import shutil
import random

# Load variables through .env file
load_dotenv()
# Telegram tokens and chat id
telegram_alert_bot = telepot.Bot(os.getenv("TELEGRAM_TOKEN_ALERT"))
telegram_download_bot = telepot.Bot(os.getenv("TELEGRAM_TOKEN_DOWNLOAD"))
telegram_notify_bot = telepot.Bot(os.getenv("TELEGRAM_TOKEN_NOTIFY"))
telegram_alert_id = os.getenv("TELEGRAM_ID_ALERT")
telegram_download_fullhd_id = os.getenv("TELEGRAM_ID_DOWNLOAD_FULLHD")
telegram_download_4k_id = os.getenv("TELEGRAM_ID_DOWNLOAD_4K")
# Database connection
database_connection = {
    'host': "ddd_database",
    'database': "dbmovies",
    'user': os.getenv("DATABASE_MOVIE_USER"),
    'password': os.getenv("DATABASE_MOVIE_PASSWORD")
    }
table_settings = "tbsettings"
table_movies = "tbmovies"
table_links = "tblinks"
table_quality = "tbquality"
table_users = "tbusers"
table_state = "tbstate"
table_history = "tbhistory"
# Web URL
web_url = "https://descargasdd.net"
web_thread = "/showthread.php?t="
web_forum = "/forumdisplay.php?f="
post_url = web_url + web_thread
# Web login
web_user = os.getenv("WEB_USER")
web_password = os.getenv("WEB_PASSWORD")
# MyJDownloader
myjd_user = os.getenv("MYJD_USER")
myjd_password = os.getenv("MYJD_PASSWORD")
myjd_device = os.getenv("MYJD_DEVICE")
# Directories
directory_downloads = "/downloads"
directory_movies_fullhd = "/movies_fullhd"
directory_movies_4k = "/movies_4k"
file_extension = "mkv"
# Telegram alerts messages
message_error_1 = "🔥 <b>Error Database (DescargasDD) </b> \n Ha sucedido un error al conectar con la base de datos."
message_error_2 = "🔥 <b>Error Database (DescargasDD) </b> \n Ha sucedido un error al insertar un registro con estado 2 en la base de datos."
message_error_3 = "🔥 <b>Error Telegram (DescargasDD) </b> \n Ha sucedido un error al notificar una nueva película en Telegram."
message_error_4 = "🔥 <b>Error Fichero (DescargasDD) </b> \n Ha sucedido un error al mover el fichero de la película desde descargas."
message_error_5 = "🔥 <b>Error Enlaces (DescargasDD) </b> \n Ha sucedido un error al intentar scrapear los enlaces de la película: "
# Other variables
synopsis_button = "Sinopsis"
download_button = "Descargar"
# Plex options
plex_user_id = int(os.getenv("PLEX_USER_ID"))
plex_group_id = int(os.getenv("PLEX_GROUP_ID"))

def main():
    # Check if the connection to the database is successful.
    database_status = False
    while database_status == False:
        try:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Comprobando conexión a la base de datos...")
            connection = mysql.connector.connect(**database_connection)
            cursor = connection.cursor()
            time.sleep(5)
            sql = "SELECT " + table_settings + ".value FROM " + table_settings + " WHERE " + table_settings + ".option = 'api_enable'"
            cursor.execute(sql)
            result = cursor.fetchone()
            api_enable = int(result[0])
            cursor.close()
            connection.close()
            database_status = True
        except:
            print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] La conexión con la base de datos ha sido rechazada...")
            sys.exit(1)
    print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] La conexión con la base de datos se ha realizado con éxito.")

    # Check if the API is active
    if api_enable == 0:
        print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] La está API funcionando. Escuchando peticiones...")

        # Check web to find new movies
        def check_dd():
            while 1:
                download_dd(143,3) # Movies FullHD
                download_dd(324,3) # Animation FullHD
                download_dd(164,4) # Movies 4K
                time.sleep(3600)

        # Wait to download, scrapy url and add to download it
        def check_tg():
            telegram_download_bot.message_loop({'chat': notification_bot, 'callback_query': download_bot})

        # Check if a new download has been notified from telegram and all its process
        def check_dw():
            while 1:
                check_download()
                time.sleep(300)

        check_dd = Thread(target=check_dd)
        check_dd.start()
        check_tg = Thread(target=check_tg)
        check_tg.start()
        check_dw = Thread(target=check_dw)
        check_dw.start()
    else:
        print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] La API se encuentra actualmente deshabilitada.")

def download_dd(url, movie_quality):
    try:
        if movie_quality == 3:
            thread_title = "thread_title_16686"
            download_quality = "1080"
        elif movie_quality == 4:
            thread_title = "thread_title_16713"
            download_quality = "4K"
    except:
        sys.exit(1)
    web_status_code = requests.get(web_url).status_code
    if web_status_code == 200:
        movies_list = []
        r = requests.get(web_url + web_forum + str(url), stream=True)
        for line in r.iter_lines():
            line = line.decode('ISO-8859-1')
            if re.search(thread_title, line) is None:
                if re.search(r'class=\"magnify\"', line):
                    check = line.strip().split('"')
                    poster = check[3]
                if re.search(r'thread_title', line):
                    if re.search(download_quality, line):
                        check = line.strip().split('>')
                        register = re.split('[|([][ ]{0,1}([0-9]{4})[ ]{0,1}', check[1])
                        title_dd = str(register[0]).split('(')[0].replace("'","").replace(":"," -").replace("¿","").replace("?","").replace("?","").replace("4K","").replace("UHD","").rstrip()
                        year_dd = int(register[1])
                        link_dd = int(check[0].strip().split('?t=')[1].strip().split('&amp')[0])
                        # Just search for movies from this year or the previous year
                        if year_dd >= (datetime.datetime.now().year - 1):
                            movies_list.append([poster,title_dd,year_dd,link_dd])
        try:
            connection = mysql.connector.connect(**database_connection)
            cursor = connection.cursor()
            for movie in movies_list:
                poster = movie[0]
                movie_title = movie[1]
                movie_year = movie[2]
                movie_link = movie[3]
                search_movie = "SELECT " + table_movies + ".id, " + table_movies + ".title FROM " + table_movies + " WHERE " + table_movies + ".title = \"%s\" LIMIT 1" % (movie_title)
                search_quality = "SELECT " + table_quality + ".quality FROM " + table_quality + " WHERE " + table_quality + ".id = %d" % (movie_quality)
                cursor.execute(search_quality)
                quality_name = cursor.fetchone()[0]
                cursor.execute(search_movie)
                result = cursor.fetchone()
                if result:
                    movie_id = result[0]
                    try:
                        search_movie_state = "SELECT " + table_links + ".id, " + table_movies + ".title FROM " + table_movies + " INNER JOIN " + table_links + " ON " + table_movies + ".id = " + table_links + ".movie_id WHERE " + table_movies + ".title = \"%s\" AND " % (movie_title) + table_links + ".quality_id = %d" % (movie_quality)
                        cursor.execute(search_movie_state)
                        result = cursor.fetchall()
                        if not result:
                            movie_exists = False
                        else:
                            movie_exists = True
                    except:
                        telegram_alert_bot.sendMessage(telegram_alert_id, message_error_2, parse_mode='HTML')
                        raise
                else:
                    sql_insert_movie = "INSERT INTO " + table_movies + " (title, year) VALUES('%s', %d)" %(movie_title, movie_year)
                    cursor.execute(sql_insert_movie)
                    connection.commit()
                    search_movie_id = "SELECT LAST_INSERT_ID()"
                    cursor.execute(search_movie_id)
                    movie_id = int(cursor.fetchone()[0])
                    movie_exists = False
                if movie_exists == False:
                    sql_insert_link = "INSERT INTO " + table_links + " (id, movie_id, quality_id) VALUES(%d, %d, %d)" % (movie_link, movie_id, movie_quality)
                    sql_insert_history = "INSERT INTO " + table_history + " (link_id, state_id, date) VALUES(%d, %d, SYSDATE())" % (movie_link, 2)
                    cursor.execute(sql_insert_link)
                    cursor.execute(sql_insert_history)
                    connection.commit()
                    print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Nueva pelicula [" + str(quality_name) + "]: " + movie_title + ".")
                    notification_bot(poster, movie_title, movie_link, movie_quality, quality_name)
            cursor.close()
            connection.close()
        except:
            telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
            raise

def notification_bot(poster, movie_title, movie_link, movie_quality, quality_name):
    try:
        if movie_quality == 3:
            telegram_download_id = telegram_download_fullhd_id
        elif movie_quality == 4:
            telegram_download_id = telegram_download_4k_id
        notify_bot_message = ("🎬 <b>Nueva película</b> <b>[" + quality_name + "]</b>\n<a href=\"" + post_url + str(movie_link) + "\">" + movie_title + "</a>")
        telegram_download_bot.sendPhoto(telegram_download_id, poster, notify_bot_message, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=synopsis_button,url=post_url + str(movie_link))],
            [InlineKeyboardButton(text=download_button,callback_data=str(movie_link))]
            ]
        ))
        time.sleep(60)
    except:
        telegram_alert_bot.sendMessage(telegram_alert_id, message_error_3, parse_mode='HTML')
        raise

def download_bot(msg):
    def download_content():
        telegram_message_data = int(msg['data'])
        telegram_user_id = int(msg['from']['id'])
        telegram_user_name = str(msg['from']['first_name'])
        try:
            telegram_user_last_name = (msg['from']['last_name'])
        except:
            telegram_user_last_name = "NULL"
        try:
            telegram_user_username = (msg['from']['username'])
        except:
            telegram_user_username = "NULL"
        try:
            connection = mysql.connector.connect(**database_connection)
            cursor = connection.cursor()
            sql = "SELECT " + table_movies + ".title, " + table_state + ".id, date FROM (((" + table_movies + " INNER JOIN " + table_links + " ON " + table_movies + ".id = " + table_links + ".movie_id) INNER JOIN " + table_history + " ON " + table_history + ".link_id = " + table_links + ".id) INNER JOIN " + table_quality + " ON " + table_quality + ".id = " + table_links + ".quality_id) INNER JOIN " + table_state + " ON " + table_state + ".id = " + table_history + ".state_id WHERE " + table_links + ".id = %d ORDER BY " % (telegram_message_data) + table_history + ".date DESC LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            movie_link = telegram_message_data
            movie_title = result[0]
            movie_state = result[1]
            telegram_message = result[2]
            cursor.close()
            connection.close()
            if movie_state == 1:
                search_telegram_user(movie_link, telegram_user_id, telegram_user_name, telegram_user_last_name, 1)
                print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] " + telegram_user_name + " quiere descargar la película: " + movie_title + ", pero hay un error con estos enlaces.")
                # try:
                #     connection = mysql.connector.connect(**database_connection)
                #     cursor = connection.cursor()
                #     sql = "SELECT COUNT(" + table_history + ".id) FROM " + table_history + " WHERE " + table_history + ".user_id = %d AND " % (telegram_user_id) + table_history + ".link_id = %d AND " % (movie_link) + table_history + ".state_id = 1"
                #     cursor.execute(sql)
                #     count_notify_1 = cursor.fetchone()[0]
                #     if count_notify_1 == 1:
                #         telegram_notify_bot.sendMessage(telegram_user_id, "¡Hubo un error al intentar descargar la película <b> " + movie_title + "</b>, pero se avisó al administrador para añadirla manualmente.", parse_mode='HTML')
                #     else:
                #         if count_notify_1 == 2:
                #             count_message = "No te preocupes, aunque haya habido un error, en cuanto se descargue la película <b>" + movie_title + "</b> yo te avisaré."
                #         elif count_notify_1 == 3:
                #             count_message = "Por más que insistas, hasta que no se añada la película <b>" + movie_title + "</b> manualmente, no se empezará a descargar."
                #         elif count_notify_1 == 4:
                #             count_message = "¿Crees que estoy descansando? ¡Estoy intentando hacerlo lo más rápido posible para descargar la película <b>" + movie_title + "</b>!"
                #         elif count_notify_1 == 5:
                #             count_message = "¡Vete a la mierda!"
                #         elif count_notify_1 == 6:
                #             count_notify_1 = "Paso de ti."
                #         elif count_notify_1 >= 7:
                #             random_message = ['Patata', 'Manzana', 'Acelgas', 'Vinagre', 'Avellana', 'Alubias', 'Sandía', 'Sardinas', 'Pipas']
                #             count_message = random.choice(random_message)
                #         telegram_notify_bot.sendMessage(telegram_user_id, count_message, parse_mode='HTML')
                #     cursor.close()
                #     connection.close()
                # except:
                #     telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
                #     raise
            elif movie_state == 2:
                scrapy_download_url(movie_link, movie_title, telegram_user_id, telegram_user_name, telegram_user_last_name)
            elif movie_state == 3:
                search_telegram_user(movie_link, telegram_user_id, telegram_user_name, telegram_user_last_name, 3)
                print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] " + telegram_user_name + " quiere descargar la película: " + movie_title + ", pero ya está en proceso de descarga.")
                # try:
                #     connection = mysql.connector.connect(**database_connection)
                #     cursor = connection.cursor()
                #     sql = "SELECT COUNT(" + table_history + ".id) FROM " + table_history + " WHERE " + table_history + ".user_id = %d AND " % (telegram_user_id) + table_history + ".link_id = %d AND " % (movie_link) + table_history + ".state_id = 3"
                #     cursor.execute(sql)
                #     count_notify_3 = cursor.fetchone()[0]
                #     if count_notify_3 == 1:
                #         telegram_notify_bot.sendMessage(telegram_user_id, "¡Hola <b>" + telegram_user_name + "</b>!\nLa película <b> " + movie_title + "</b> ya se estaba descargando.\nEn cuanto finalice la descarga, te avisaré.", parse_mode='HTML')
                #     else:
                #         if count_notify_3 == 2:
                #             count_message = "Que sí... que quieres descargar la película <b>" + movie_title + "</b>, ya lo sé."
                #         elif count_notify_3 == 3:
                #             count_message = "Por más veces que me lo digas, no se va a descargar más rápido la película <b>" + movie_title + "</b>."
                #         elif count_notify_3 == 4:
                #             count_message = "¿Cuántas veces me vas a decir que te quieres descargar la película <b>" + movie_title + "</b>? Ya te avisaré cuando esté disponible."
                #         elif count_notify_3 == 5:
                #             count_message = "¡Ya me he enterado de que quieres descargar la película <b>" + movie_title + "</b>! ¡No insistas!"
                #         elif count_notify_3 == 6:
                #             count_message = "¡Vete a la mierda!"
                #         elif count_notify_3 == 7:
                #             count_message = "Paso de ti."
                #         elif count_notify_3 >= 8:
                #             random_message = ['Patata', 'Manzana', 'Acelgas', 'Vinagre', 'Avellana', 'Alubias', 'Sandía', 'Sardinas', 'Pipas']
                #             count_message = random.choice(random_message)
                #         telegram_notify_bot.sendMessage(telegram_user_id, count_message, parse_mode='HTML')
                #     cursor.close()
                #     connection.close()
                # except:
                #     telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
                #     raise
            elif movie_state == 4:
                search_telegram_user(movie_link, telegram_user_id, telegram_user_name, telegram_user_last_name, 4)
                print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] " + telegram_user_name + " quiere descargar la película: " + movie_title + ", pero ya está descargada.")
                # try:
                #     connection = mysql.connector.connect(**database_connection)
                #     cursor = connection.cursor()
                #     sql = "SELECT COUNT(" + table_history + ".id) FROM " + table_history + " WHERE " + table_history + ".user_id = %d AND " % (telegram_user_id) + table_history + ".link_id = %d AND " % (movie_link) + table_history + ".state_id = 4"
                #     cursor.execute(sql)
                #     count_notify_4 = cursor.fetchone()[0]
                #     if count_notify_4 == 1:
                #         telegram_notify_bot.sendMessage(telegram_user_id, "¡Hola <b>" + telegram_user_name + "</b>!\nLa película <b> " + movie_title + "</b> ya estaba descargada, la puedes ver en <b>Plex</b>.", parse_mode='HTML')
                #     else:
                #         if count_notify_4 == 2:
                #             count_message = "Por si no lo recuerdas, la película <b>" + movie_title + "</b>, ya está descargada."
                #         elif count_notify_4 == 3:
                #             count_message = "No pongas más veces la película <b>" + movie_title + "</b> a descargar porque ya lo está."
                #         elif count_notify_4 == 4:
                #             count_message = "Vaya memoria tienes... ¡Que la película <b>" + movie_title + "</b> ya la puedes ver"
                #         elif count_notify_4 == 5:
                #             count_message = "Cuántas veces te habré dicho ya de que la película <b>" + movie_title + "</b> está en Plex."
                #         elif count_notify_4 >= 6:
                #             count_message = "¡Vete a la mierda!"
                #         elif count_notify_4 == 7:
                #             count_message = "Paso de ti."
                #         elif count_notify_4 >= 8:
                #             random_message = ['Patata', 'Manzana', 'Acelgas', 'Vinagre', 'Avellana', 'Alubias', 'Sandía', 'Sardinas', 'Pipas']
                #             count_message = random.choice(random_message)
                #         telegram_notify_bot.sendMessage(telegram_user_id, count_message, parse_mode='HTML')
                #     cursor.close()
                #     connection.close()
                # except:
                #     telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
                #     raise
                # telegram_notify_bot.sendMessage(telegram_user_id, "¡Hola <b>" + telegram_user_name + "</b>!\nLa película <b> " + movie_title + "</b> ya estaba descargada, la puedes ver en <b>Plex</b>.", parse_mode='HTML')
        except:
            telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
            raise
    download_content = Thread(target=download_content)
    download_content.start()

def search_telegram_user(movie_link, telegram_user_id, telegram_user_name, telegram_user_last_name, state_id):
    try:
        connection = mysql.connector.connect(**database_connection)
        cursor = connection.cursor()
        if telegram_user_id == None:
            telegram_user_null = True
        else:
            telegram_user_null = False
        if telegram_user_null == False:
            search_user = "SELECT " + table_users + ".id FROM " + table_users + " WHERE " + table_users + ".id = %d" % (telegram_user_id)
            cursor.execute(search_user)
            result = cursor.fetchone()
            if not result:
                print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Se acaba de añadir el usuario " + telegram_user_name + " desde telegram.")
                sql = "INSERT INTO " + table_users + " (id, user, last_name) VALUES(%d, '%s', '%s')" % (telegram_user_id, telegram_user_name, telegram_user_last_name)
                cursor.execute(sql)
            insert_history = "INSERT INTO " + table_history + " (link_id, user_id, state_id, date) VALUES(%d, %d, %d, SYSDATE())" % (movie_link, telegram_user_id, state_id)
        else:
            insert_history = "INSERT INTO " + table_history + " (link_id, user_id, state_id, date) VALUES(%d, NULL, %d, SYSDATE())" % (movie_link, state_id)
        cursor.execute(insert_history)
        connection.commit()
        cursor.close()
        connection.close()
    except:
        telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
        raise

def scrapy_download_url(movie_link, movie_title, telegram_user_id, telegram_user_name, telegram_user_last_name):
    # Create a new cookie session
    with requests.Session() as session:
        session.post(web_url + '/login.php?do=login', {
            'vb_login_username': web_user,
            'vb_login_password': web_password,
            'vb_login_md5password': hashlib.md5(web_password.encode()).hexdigest(),
            'vb_login_md5password_utf': hashlib.md5(web_password.encode("utf-8")).hexdigest(),
            'cookieuser': 1,
            'do': 'login',
            's': '',
            'securitytoken': 'guest'
    })

    # Get data from URL using a cookie session
    r = session.get(post_url + str(movie_link), stream=True)

    # Find HTML code to press the thanks button
    thanks_button = False
    for line in r.iter_lines():
        if thanks_button == False:
            if re.search(b'post_thanks.php\?do\=post_thanks_add', line) is not None:
                check = line.decode('ISO-8859-1').strip().split('\"')
                data = check[1].strip().split('=')
                p = data[2].strip().split('&amp')[0]
                securitytoken = data[3]
                thanks_button = True

    # Push thanks button to unlock downlaods links
    session.post(web_url + '/post_thanks.php?do=post_thanks_add', {
        'do': 'post_thanks_add',
        'using_ajax': 1,
        'p': p,
        'securitytoken': securitytoken,
    })

    s = session.get(post_url + str(movie_link), stream=True)
    for line in s.iter_lines():
        if re.search(b'https://mega.nz', line) is not None:
            url_download = line.decode('ISO-8859-1').strip().split('>')
            if 'second_iteration' in locals():
                url_mega = url_mega + " " + url_download[0]
                last_mega_url = 0
            else:
                url_mega = url_download[1]
                second_iteration = True
        if 'last_mega_url' in locals():
            if last_mega_url <= 1:
                url_uploaded = line.decode('ISO-8859-1').split('<')[0]
                last_mega_url = last_mega_url+1
    try:
        full_url_download=url_mega + " " + url_uploaded
        myjdownloader(movie_link, full_url_download)
        search_telegram_user(movie_link, telegram_user_id, telegram_user_name, telegram_user_last_name, 3)
        print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] " + telegram_user_name + " quiere descargar la película: " + movie_title + ", por lo que se pone a descargar.")
        # telegram_notify_bot.sendMessage(telegram_user_id, "¡Hola <b>" + telegram_user_name + "</b>!\nAcabo de poner a descargar la película <b> " + movie_title + "</b>.\nEn cuanto esté descargada te avsaré.", parse_mode='HTML')
    except:
        time.sleep(5)
        search_telegram_user(movie_link, telegram_user_id, telegram_user_name, telegram_user_last_name, 1)
        print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Ha habido un error intentando descargar la película: " + movie_title + " que quiere descargar " + telegram_user_name + ".")
        telegram_alert_bot.sendMessage(telegram_alert_id, message_error_5 + "<b>" + movie_title + "</b>", parse_mode='HTML', disable_web_page_preview=True, reply_markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=synopsis_button,url=post_url + str(movie_link))]
            ]
        ))
        # telegram_notify_bot.sendMessage(telegram_user_id, "Ha habido un error al intentar descargar la película: <b>" + movie_title + "</b> de forma automática...\n\nSe ha notificado al administrador y se pondrá a descargar de forma manual.\n\n<b>¡Ten paciencia!</b>", parse_mode='HTML')

def myjdownloader(movie_link, full_url_download):
    jd = myjdapi.Myjdapi()
    jd.connect(myjd_user,myjd_password)
    jd.update_devices()
    device = jd.get_device(myjd_device).linkgrabber.add_links([{
        "autostart" : True,
        "packageName" : str(movie_link),
        "links" : full_url_download
    }])

def check_download():
    try:
        connection = mysql.connector.connect(**database_connection)
        cursor = connection.cursor()
        sql = "SELECT " + table_movies + ".title, " + table_movies + ".year, " + table_links + ".quality_id, " + table_links + ".id FROM (" + table_movies + " INNER JOIN " + table_links + " ON " + table_movies + ".id = " + table_links + ".movie_id) INNER JOIN " + table_history + " ON " + table_history + ".link_id = " + table_links + ".id WHERE " + table_history + ".state_id = 3"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            movie_title = row[0]
            movie_year = row[1]
            movie_quality = row[2]
            movie_link = row[3]
            movie_file(movie_link, movie_title, movie_year, movie_quality)
        cursor.close()
        connection.close()
    except:
        telegram_alert_bot.sendMessage(telegram_alert_id, message_error_1, parse_mode='HTML')
        raise

def movie_file(movie_link, movie_title, movie_year, movie_quality):
    all_directory_downloads = directory_downloads + "/" + str(movie_link)
    if os.path.exists(all_directory_downloads):
        for folder in os.listdir(all_directory_downloads):
            if os.path.isdir(os.path.join(all_directory_downloads + "/" + folder)):
                for subfolder in os.listdir(all_directory_downloads + "/" + folder):
                    file = subfolder
                    path, dirs, files = next(os.walk(all_directory_downloads + "/" + folder))
                    finish_download_movie(movie_link, movie_title, movie_year, movie_quality, path, file, all_directory_downloads)
            else:
                file = folder
                path, dirs, files = next(os.walk(all_directory_downloads))
                finish_download_movie(movie_link, movie_title, movie_year, movie_quality, path, file, all_directory_downloads)

def finish_download_movie(movie_link, movie_title, movie_year, movie_quality, path, file, all_directory_downloads):
    pattern = re.compile(r'^.*[.](' + file_extension + ')$', re.IGNORECASE)
    if movie_quality == 3:
        directory_movies = directory_movies_fullhd
    elif movie_quality == 4:
        directory_movies = directory_movies_4k
    else:
        raise
    if pattern.match(file):
        try:
            movie = path + "/" + file
            full_movie = directory_movies + "/" + movie_title + " (" + str(movie_year) + ")." + file_extension
            os.utime(movie, None)
            shutil.move(movie, full_movie)
            os.chown(full_movie, plex_user_id, plex_group_id)
            os.chmod(full_movie, 0o770)
            try:
                search_telegram_user(movie_link, None, None, None, 4)
                print("["+time.strftime("%d/%m/%Y %H:%M:%S")+"] Se acaba de descargar la película: " + movie_title + ".")
                # connection = mysql.connector.connect(**database_connection)
                # cursor = connection.cursor()
                # search_user_download = "SELECT " + table_history + ".user_id FROM " + table_history + " WHERE " + table_history + ".link_id = %d AND " % (movie_link) + table_history + ".state_id = %d" % (3)
                # cursor.execute(search_user_download)
                # result = cursor.fetchall()
                # for row in result:
                #     telegram_user_id = row[0]
                #     telegram_notify_bot.sendMessage(telegram_user_id, "Ya tienes disponible en Plex la película:\n<b>" + movie_title + "</b>.", parse_mode='HTML')
                # cursor.close()
                # connection.close()
            except:
                telegram_alert_bot.sendMessage(telegram_alert_id, message_error_4, parse_mode='HTML')
                raise
            shutil.rmtree(all_directory_downloads)
        except:
            telegram_alert_bot.sendMessage(telegram_alert_id, message_error_4, parse_mode='HTML')
            raise

# Run application
main()