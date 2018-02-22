# -*- coding: utf-8 -*-
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmc
import urllib2
import socket
import xbmcaddon
import datetime
import re
import os
import base64
import urlresolver
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, URLError, HTTPError
import requests
import re
from lib import jsunpack
import shortytv
from core import httptools
from core import scrapertools
from platformcode import logger,config
from core import jsontools
from servers import openload
from servers import okru
from servers import rapidvideo
from servers import gvideo


__modo_grafico__ = config.get_setting('modo_grafico', 'animeyt')

HOST = "http://animeyt.tv/"
systempjos1 = 'http://www.animeyt.tv/emision'
systempjos2= 'http://www.animeyt.tv/animes'
systempjos3= 'http://www.animeyt.tv'
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
scrape_url = "https://www.youtube.com"
search_url = "/results?search_query="
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
xbmcplugin.setContent(addon_handle, 'movies')


def findall(pattern, searText, flags):

    try:
        return re.findall(pattern, searText, flags)

    except Exception as e:
        return None


def verificar_video(url):
    codigo=httptools.downloadpage(url).code
    if codigo==200:
        # Revise de otra forma
        data=httptools.downloadpage(url).data
        removed = scrapertools.find_single_match(data,'removed(.+)')
        if len(removed) != 0:
            codigo1=404
        else:
            codigo1=200
    else:
        codigo1=200
    return codigo1

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)



def getusersearch(website):
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Buscador de '+website )
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        search_term = kb.getText()
        return(search_term)
    else:
        return


def addMenuitem(url, li, folder):
    return xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=folder)


def endMenu():
    xbmcplugin.endOfDirectory(addon_handle)


def bstheurl(url):
    sb_get = requests.get(url, headers=mozhdr)
    soupeddata = BeautifulSoup(sb_get.content, "html.parser")
    yt_links = soupeddata.find_all("a", class_="yt-uix-tile-link")
    for x in yt_links:
        yt_href = x.get("href")
        yt_title = x.get("title")
        yt_final = scrape_url + yt_href
        url = build_url({'mode': 'play', 'playlink': yt_final})
        li = xbmcgui.ListItem(yt_title, iconImage='DefaultVideo.png')
        li.setProperty('IsPlayable', 'true')
        addMenuitem(url, li, False)
    endMenu()

def read(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.71 Safari/537.36')]
    response = opener.open(url)
    data = response.read()

    return data


def resolve_url(url):
    duration = 7500  # in milliseconds
    message = "Este enlace no utiliza Resolver"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("Spokes", message,
                            xbmcgui.NOTIFICATION_INFO, duration, False)
        return False
    else:
        return stream_url

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data
    match = re.search('(.+)/v/(\w+)/file.html', page_url)
    domain = match.group(1)

    patron = 'getElementById\(\'dlbutton\'\).href\s*=\s*(.*?);'
    media_url = scrapertools.find_single_match(data, patron)
    numbers = scrapertools.find_single_match(media_url, '\((.*?)\)')
    url = media_url.replace(numbers, "'%s'" % eval(numbers))
    url = eval(url)

    mediaurl = '%s%s' % (domain, url)
    extension = "." + mediaurl.split('.')[-1]
    video_urls.append([extension + " [zippyshare]", mediaurl])

    return video_urls

def play_video(path):
    """
    Prueba de Funcionamiento de Repositorio
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_url = play_item.getfilename()
    stream_url = resolve_url(vid_url)
    if stream_url:
        play_item.setPath(stream_url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)


mode = args.get('mode', None)


def plus01():
    fanart = 'http://darkelite.ml/img/fondo.jpg'
    thumbnail = 'https://scontent-dft4-2.xx.fbcdn.net/v/t1.0-9/17634804_516923798698228_6361457002969571867_n.jpg?oh=9be6c309ab24227711b52e965207b877&oe=5A7DC18C'
    web = 'https://www.pelisplus.tv'
    data = read(web)
    pattern = '(unitem.*\n.*?href\=\".*?\".\n.*)'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:


        pattern = 'href\=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]
        fanart=fanart
        thumbnail=thumbnail
        if 'peliculas' in url:
            title = '[COLOR yellow][B]Todas las Peliculas[/B][/COLOR]'
            parse = web + url

            url = build_url({'mode': 'plus02', 'foldername': title, 'direccion': parse, 'tags':'pag-', 'pagina': '0'})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Plot": '[COLOR skyblue][B]Coleccion Completa de PelisPlus[/B][/COLOR]'})
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)

        if 'estrenos' in url:
            title = '[COLOR yellow][B]Estrenos de Peliculas[/B][/COLOR]'
            parse = web + url

            url = build_url({'mode': 'plus02', 'foldername': title, 'direccion': parse, 'tags':'pag-', 'pagina': '0'})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Plot": '[COLOR skyblue][B]Estrenos Peliculas de PelisPlus[/B][/COLOR]'})
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)

        if 'series' in url:
            title = '[COLOR yellow][B]Series[/B][/COLOR]'
            parse = web + url

            url = build_url({'mode': 'plus04', 'foldername': title, 'direccion': parse, 'tags': 'pag-', 'pagina': '0'})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Plot": '[COLOR skyblue][B]Series de PelisPlus[/B][/COLOR]'})
            li.setProperty('fanart_image', fanart)
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                        listitem=li, isFolder=True)

    #url = build_url({'mode': 'plus07'})
    li = xbmcgui.ListItem('[COLOR orange][B]Buscar Peliculas o Series en PelisPLus[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Ingresa Datos para hacer Busqueda de Peliculas o Series '})
    li.setProperty('fanart_image', fanart)
    addMenuitem(plus07(), li, True)


    xbmcplugin.endOfDirectory(addon_handle)



#if mode == 'plus07':
def plus07():
    website = 'https://www.pelisplus.tv/busqueda/?s='
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Buscar en la Coleccion PelisPlus')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        if kb.getText() == '':
            duration = 3500
            dialog = xbmcgui.Dialog()
            dialog.notification("Spokes", 'No se detecto nada escrito en el buscador Vuelve a Intentar',
                                xbmcgui.NOTIFICATION_INFO, duration, False)
        else:
            search_term = kb.getText()
            search_term = search_term.replace(" ", "%20")
            dir = website + search_term
            html = read(dir)
            pattern = '(\<li.*?data.*\n.*\n.*\n.*\n.*\n.*\<\/a)'
            matches = re.findall(pattern, html, re.MULTILINE)
            for match in matches:
                pattern = '.*?\/+.*?\/(.*?)\".*tip'
                code = re.findall(pattern, match, re.MULTILINE)[0]  # baby-el-aprendiz-del-crimen/

                pattern = 'src\=\"(.*?)\"'
                thumbnail = re.findall(pattern, match, re.MULTILINE)[0]
                thumbnail = thumbnail.replace("w154", "original")

                fanart = 'http://darkelite.ml/img/fondo.jpg'

                pattern = '.*\>(.*?)<\/a'
                title = re.findall(pattern, match, re.MULTILINE)[0]

                url = 'https://www.pelisplus.tv/' + code
                info = 'PelisPlus'

                if 'pelicula' in url:
                    url = build_url({'mode': 'plus03', 'foldername': title, 'direccion': code, 'thumbnail': thumbnail,
                                     'fanart': fanart})
                    li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                    li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                    li.setProperty('fanart_image', fanart)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                                listitem=li, isFolder=True)

                elif 'serie' in url:
                    url = build_url(
                        {'mode': 'plus05', 'foldername': title, 'direccion': url, 'thumbnail': thumbnail,
                         'fanart': fanart})
                    li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                    li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                    li.setProperty('fanart_image', fanart)
                    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                                listitem=li, isFolder=True)




            endMenu()



if mode == 'plus04':
    web = args['direccion'][0]
    tags = args['tags'][0]
    previos = args['pagina'][0]
    pagina = int(float(previos)) + 1
    html = web + tags + str(pagina)
    data = read(html)
    pattern = '(\<li.*?data.*\n.*\n.*\n.*\n.*\n.*\<\/a)'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = '.*?url.*?serie\/(.*?)\"'
        code = re.findall(pattern, match, re.MULTILINE)[0] #baby-el-aprendiz-del-crimen/

        pattern = 'src\=\"(.*?)\"'
        thumbnail = re.findall(pattern, match, re.MULTILINE)[0]
        thumbnail = thumbnail.replace("w154","original")

        fanart = 'http://darkelite.ml/img/fondo.jpg'

        pattern = '.*\>(.*?)<\/a'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        url = 'https://www.pelisplus.tv/serie/'+code
        info = 'Series de PelisPlus'

        url = build_url({'mode': 'plus05', 'foldername': title, 'direccion': url, 'thumbnail': thumbnail, 'fanart':fanart})
        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'plus04', 'foldername': 'Siguiente Pagina', 'direccion': 'https://www.pelisplus.tv/series/', 'tags':'pag-', 'pagina': pagina})
    li = xbmcgui.ListItem('Siguiente Pagina', iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png', thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    li.setProperty('fanart_image', 'http://darkelite.ml/img/fondo.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode == 'plus05':
    web = args['direccion'][0]
    title = args['foldername'][0]
    thumbnail = args['thumbnail'][0]
    fanart = args['fanart'][0]
    data = read(web)
    pattern = '(a.*href.*\n.*?span.*\/a.*\n.*\>)'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = 'span\>(.*?)\<'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '.*href\=\"(.*?)".*?ena'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        thumbnail = thumbnail
        fanart = fanart
        info = 'Series de PelisPlus'

        url = build_url(
            {'mode': 'plus06', 'foldername': title, 'direccion': url, 'thumbnail': thumbnail, 'fanart': fanart})
        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode == 'plus06':
    web = args['direccion'][0]
    title = args['foldername'][0]
    thumbnail = args['thumbnail'][0]
    fanart = args['fanart'][0]
    data = read(web)
    pattern = '(https.*?rey.*?epi.*?\/.*?\/)'
    enlace = re.findall(pattern, data, re.IGNORECASE)[0]
    html = read(enlace)
    pattern = '(<li.*?data\-id\=.*?<a.*?href.*?>)'
    matches = re.findall(pattern, html, re.MULTILINE)
    for match in matches:

        pattern = 'href\=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        title = title
        thumbnail = thumbnail
        fanart = fanart

        if 'rapidvideo' in url:
            title = title
            thumbnail = thumbnail
            fanart = fanart
            info = 'Peliculas de PelisPlus'
            web = url
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.71 Safari/537.36')]
            try:
                response = opener.open(web)
            except HTTPError as e:
                web = url

            except URLError as e:
                web = url

            else:
                data2 = response.read()
                pattern = '(a.*href.*ra.*q\=.*)'
                parsers = re.findall(pattern, data2, re.IGNORECASE)
                for parse in parsers:

                    pattern = '.*?\"(.*?)\"'
                    url = re.findall(pattern, parse, re.MULTILINE)[0]

                    if '360' in url:
                        title = '[COLOR lime][B]Opcion Rapidvideo Calidad 360 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    elif '480' in url:
                        title = '[COLOR lime][B]Opcion Rapidvideo Calidad 480 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    elif '720' in url:
                        title = '[COLOR lime][B]Opcion Rapidvideo Calidad 720 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    elif '1080' in url:
                        title = '[COLOR lime][B]Opcion Rapidvideo Calidad 1080 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

        elif 'downace' in url:

            title = '[COLOR lime][B]Opcion DownAce[/B][/COLOR]'
            thumbnail = thumbnail
            fanart = fanart
            info = 'Peliculas de PelisPlus'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

        elif 'streamango' in url:

            title = '[COLOR lime][B]Opcion StreaMango[/B][/COLOR]'
            thumbnail = thumbnail
            fanart = fanart
            info = 'Peliculas de PelisPlus'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode == 'plus02':
    web = args['direccion'][0]
    tags = args['tags'][0]
    previos = args['pagina'][0]
    pagina = int(float(previos)) + 1
    html = web + tags + str(pagina)
    data = read(html)
    pattern = '(\<li.*?data.*\n.*\n.*\n.*\n.*\n.*\<\/a)'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = '.*?url.*?pelicula\/(.*?)\"'
        code = re.findall(pattern, match, re.MULTILINE)[0] 

        pattern = 'original\=\"(.*?)\"'
        thumbnail = re.findall(pattern, match, re.MULTILINE)[0]
        thumbnail = thumbnail.replace("w154","original")

        fanart = 'http://darkelite.ml/img/fondo.jpg'

        pattern = '.*\>(.*?)<\/a'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        url = 'https://www.pelisplus.tv/pelicula/'+code
        info = 'Peliculas de PelisPlus'

        url = build_url({'mode': 'plus03', 'foldername': title, 'direccion': code, 'thumbnail': thumbnail, 'fanart':fanart})
        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'plus02', 'foldername': 'Siguiente Pagina', 'direccion': 'https://www.pelisplus.tv/peliculas/', 'tags':'pag-', 'pagina': pagina})
    li = xbmcgui.ListItem('Siguiente Pagina', iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png', thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    li.setProperty('fanart_image', 'http://darkelite.ml/img/fondo.jpg')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode == 'plus03':
    web = 'https://www.elreyxhd.com/reproductor/'
    code = args['direccion'][0]
    code = code.replace("pelicula/","")
    title = args['foldername'][0]
    thumbnail = args['thumbnail'][0]
    fanart = args['fanart'][0]
    html = web + code
    data = read(html)
    pattern = '(<li.*?data\-id\=.*?<a.*?href.*?>)'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:

        pattern = 'href\=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        title = title
        thumbnail = thumbnail
        fanart = fanart

        if 'rapidvideo' in url:
            title = title
            thumbnail = thumbnail
            fanart = fanart
            info = 'Peliculas de PelisPlus'
            web = url
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.71 Safari/537.36')]
            try:
                response = opener.open(web)
            except HTTPError as e:
                web = url

            except URLError as e:
                web = url

            else:
                data2 = response.read()
                pattern = '(a.*href.*ra.*q\=.*)'
                parsers = re.findall(pattern, data2, re.IGNORECASE)
                for parse in parsers:

                    pattern = '.*?\"(.*?)\"'
                    url = re.findall(pattern, parse, re.MULTILINE)[0]

                    if '360' in url:
                        title ='[COLOR lime][B]Opcion Rapidvideo Calidad 360 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    elif '480' in url:
                        title ='[COLOR lime][B]Opcion Rapidvideo Calidad 480 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    elif '720' in url:
                        title ='[COLOR lime][B]Opcion Rapidvideo Calidad 720 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    elif '1080' in url:
                        title ='[COLOR lime][B]Opcion Rapidvideo Calidad 1080 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

        elif 'downace' in url:

            title = '[COLOR lime][B]Opcion DownAce[/B][/COLOR]'
            thumbnail = thumbnail
            fanart = fanart
            info = 'Peliculas de PelisPlus'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

        elif 'streamango' in url:

            title = '[COLOR lime][B]Opcion StreaMango[/B][/COLOR]'
            thumbnail = thumbnail
            fanart = fanart
            info = 'Peliculas de PelisPlus'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

    xbmcplugin.endOfDirectory(addon_handle)
