# -*- coding: utf-8 -*-
import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
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





def animeyt(): #lista de secciones

    url = build_url({'mode': 'animeytreciente', 'direccion': systempjos3})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Capitulos Recientes[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Seccion Donde Estan Todos los Animes Finalizados'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = build_url({'mode': 'animeytlista', 'direccion': systempjos1})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Anime en Emision[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Aqui encontraras tus Animes en Emision'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = build_url({'mode': 'animeytlista', 'direccion': systempjos2})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Todos los Animes[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Seccion Donde Estan Todos los Animes Finalizados'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = build_url({'mode': 'animeytsearch'})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Buscar un Anime[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Ingresa Datos para hacer Busqueda de un Anime'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    endMenu()
    #return url
mode = args.get('mode', None)


url=None
playitem=''
try:
    playitem=urllib.unquote_plus(params["playitem"])
except:
    pass

if not playitem == '':
    s=getSoup('',data=playitem)
    name,url,regexs=getItems(s,None,dontLink=True)
    mode=117


elif mode == 'animeytreciente':  #Mostrar episodios
    emision = args['direccion'][0]
    data = read(emision)
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    patron_novedades = '<div class="capitulos-portada">[\s\S]+?<h2>Comentarios</h2>'
    data_novedades = scrapertools.find_single_match(data, patron_novedades)
    patron = 'href="([^"]+)"[\s\S]+?src="([^"]+)"[^<]+alt="([^"]+) (\d+)([^"]+)'
    matches = scrapertools.find_multiple_matches(data_novedades, patron)
    for url, img, scrapedtitle, eps, info in matches:
        title = scrapedtitle + " " + "1x" + eps + info
        url = build_url({'mode': 'animeytservers', 'direccion': url, 'thumbnail': img})
        li = xbmcgui.ListItem('[COLOR green][B]' + title + '[/B][/COLOR]', iconImage=img,thumbnailImage=img)
        li.setInfo("tvshows", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)
    endMenu()

elif mode == 'animeytlista': #mostrar lista de animes
    emision = args['direccion'][0]
    data = read(emision)
    pattern = '(\<article.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)'
    matches = re.findall(pattern,data,re.IGNORECASE)
    for match in matches:
        pattern = '.*?href\=\"(.*?)\".*?img'
        url = re.findall(pattern,match,re.MULTILINE)[0]

        pattern = '.*?img src\=\"(.*?)\"'
        thumbnail = re.findall(pattern,match,re.MULTILINE)[0]

        pattern = '.*title.*?>(.*?)<sm'
        title = re.findall(pattern,match,re.MULTILINE)[0]


        url = build_url({'mode': 'animeytepi','direccion':url,'thumbnail':thumbnail})
        li = xbmcgui.ListItem('[COLOR orange][B]'+ title + '[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("tvshows", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)


    pattern2 = 'page.*last.*?href\=\"(.*?)\"\>'
    paginacion = re.findall(pattern2, data, re.DOTALL)[0]
    url = build_url({'mode': 'animeytlista', 'direccion': paginacion})
    li = xbmcgui.ListItem('[COLOR red][B]Siguente Pagina[/B][/COLOR]',
                          iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png',
                          thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)

    endMenu()

elif mode == 'animeytepi':  #Mostrar episodios
    emision = args['direccion'][0]
    thumbnail = args['thumbnail'][0]
    data = read(emision)
    pattern = '(\<div.*item.*\n.*trian.*\n.*\n.*\n.*<\/a\>)'
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:
        pattern = 'href\=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'href.*\n(.*)'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        thumbnail = thumbnail

        url = build_url({'mode': 'animeytservers', 'direccion': url, 'thumbnail': thumbnail})
        li = xbmcgui.ListItem('[COLOR green][B]' + title + '[/B][/COLOR]', iconImage=thumbnail,thumbnailImage=thumbnail)
        li.setInfo("tvshows", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)
    endMenu()


elif mode == 'animeytservers':   #servers para reproducir
    emision = args['direccion'][0]
    thumbnail = args['thumbnail'][0]
    data = read(emision)
    pattern = '(if.*Opci.*\n.*?\.show.*?ht.*)'
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:
        pattern = 'src\=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        if 'dailymotion' in url:

            thumbnail = thumbnail
            web = url
            if 'http://www.dailymotion.com/embed/video/?autoPlay=1' == web:
                enlace = web
            else:
                url = build_url({'mode': 'play', 'playlink': web})
                li = xbmcgui.ListItem('[COLOR yellow][B]Opcion Dailymotion[/B][/COLOR]', iconImage=thumbnail,
                                      thumbnailImage=thumbnail)
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image',
                               'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
                addMenuitem(url, li, False)

        if 'naruto' in url:
            id = re.findall('id=([0-9]+).*', url, re.DOTALL)[0]
            file = re.findall('file\=(.*?)\.mp4', url, re.DOTALL)[0]
            title = '[COLOR yellow][B]Opcion Amazon Web Service[/B][/COLOR]'
            web = 'http://s4.animeyt.tv/chumi.php?cd='+id+'&file='+file
            url = web
            li = xbmcgui.ListItem(title, iconImage=thumbnail,
                                  thumbnailImage=thumbnail)
            li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
            addMenuitem(url, li, False)


    endMenu()



elif mode == 'animeytsearch': #search animeyt
    website= 'http://www.animeyt.tv/busqueda?terminos='
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Buscar en la Coleccion AnimeYT')
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
            search_term = search_term.replace(" ","+")
            dir = website + search_term
            html = read(dir)
            pattern = '(\<article.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)'
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:

                pattern = '.*?href\=\"(.*?)\".*?img'
                url = re.findall(pattern, match, re.MULTILINE)[0]

                pattern = '.*?img src\=\"(.*?)\"'
                thumbnail = re.findall(pattern, match, re.MULTILINE)[0]

                pattern = '.*title.*?\>(.*?)\<small'
                title = re.findall(pattern, match, re.MULTILINE)[0]
                title = title.replace("&amp;", "&")

                url = build_url({'mode': 'animeytepi', 'direccion': url, 'thumbnail': thumbnail})
                li = xbmcgui.ListItem('[COLOR orange][B]' + title + '[/B][/COLOR]', iconImage=thumbnail,
                                      thumbnailImage=thumbnail)
                li.setProperty('fanart_image','https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
                addMenuitem(url, li, True)

            xbmcplugin.endOfDirectory(addon_handle)

            endMenu()

    else:
        dialog = xbmcgui.Dialog()
        dialog.notification("Spokes", 'La Busqueda se cancelo',
                            xbmcgui.NOTIFICATION_INFO, 3500 , False)

