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



addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

scrape_url = "https://www.youtube.com"
search_url = "/results?search_query="
mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
systempjos1 = 'http://www.animeyt.tv/emision'
systempjos2= 'http://www.animeyt.tv/animes'

xbmcplugin.setContent(addon_handle, 'movies')


def findall(pattern, searText, flags):

    try:
        return re.findall(pattern, searText, flags)

    except Exception as e:
        return None

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

if mode is None:
    duration = 17500
    dialog = xbmcgui.Dialog()
    dialog.notification("Spokes", 'Mejor que el canal de los arbolitos felices!.',
                        xbmcgui.NOTIFICATION_INFO, duration, False)
    fanart = 'http://darkelite.ml/img/fondo.jpg'

    url = build_url({'mode': 'Novelas'})
    li = xbmcgui.ListItem('[COLOR yellow][B]Novelas[/B][/COLOR]', iconImage='http://www.novelashdgratis.io/img/logo.gif',
                          thumbnailImage='http://www.novelashdgratis.io/img/logo.gif')
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Reproduce el Mejor contenido en la Web de Novelas en tu Idioma[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'search', 'site': 'youtube'})
    li = xbmcgui.ListItem('[COLOR yellow][B]Buscador de Youtube[/B][/COLOR]', iconImage='http://sm.pcmag.com/t/pcmag_latam/photo/default/original_z8cw.640.jpg', thumbnailImage='http://sm.pcmag.com/t/pcmag_latam/photo/default/original_z8cw.640.jpg')
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Encuentra tus Videos Favoritos con el Buscador de Youtube[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'karaoke'})
    li = xbmcgui.ListItem('[COLOR yellow][B]Karaoke[/B][/COLOR]', iconImage='https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg',
                          thumbnailImage='https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg')
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Coleccion Selecta de Karaokes[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'plus01'})
    li = xbmcgui.ListItem('[COLOR yellow][B]PelisPlus[/B][/COLOR]',
                          iconImage='https://scontent-dft4-2.xx.fbcdn.net/v/t1.0-9/17634804_516923798698228_6361457002969571867_n.jpg?oh=9be6c309ab24227711b52e965207b877&oe=5A7DC18C',
                          thumbnailImage='https://scontent-dft4-2.xx.fbcdn.net/v/t1.0-9/17634804_516923798698228_6361457002969571867_n.jpg?oh=9be6c309ab24227711b52e965207b877&oe=5A7DC18C')
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Pelis Plus Contenido de Estrenos de Peliculas y Series de lo Mejor en la Web en tu Idioma[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'ultra'})
    li = xbmcgui.ListItem('[COLOR yellow][B]PelisUltra[/B][/COLOR]', iconImage='http://www.pelisultra.com/wp-content/uploads/2017/03/logoultra2-1.png',
                          thumbnailImage='http://www.pelisultra.com/wp-content/uploads/2017/03/logoultra2-1.png')
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Pelis Ultra Contenido de Estrenos de Peliculas[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': '0'})
    thumbnail = 'http://pm1.narvii.com/6506/9dd6c94fb32122770ca08cce3e45d4c280e08414_hq.jpg'
    li = xbmcgui.ListItem('[COLOR yellow][B]AnimeYT[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Aqui encontraras tus Animes Favoritos[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'animeflv'})
    thumbnail = 'https://pm1.narvii.com/5610/c07d6c52e768eb8d7a79d81223402fc56611971b_hq.jpg'
    li = xbmcgui.ListItem('[COLOR yellow][B]AnimeFLV[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": '[COLOR skyblue][B]Aqui encontraras tus Animes Favoritos[/B][/COLOR]'})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'plus01':
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

    url = build_url({'mode': 'plus07'})
    li = xbmcgui.ListItem('[COLOR orange][B]Buscar Peliculas o Series en PelisPLus[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Ingresa Datos para hacer Busqueda de Peliculas o Series '})
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)


    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0] == 'plus07':
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



elif mode[0] == 'plus04':
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



elif mode[0] == 'plus05':
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


elif mode[0] == 'plus06':
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



elif mode[0] == 'plus02':
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
        code = re.findall(pattern, match, re.MULTILINE)[0] #baby-el-aprendiz-del-crimen/

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


elif mode[0] == 'plus03':
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



elif mode[0] == 'ultra':

    fanart = ''
    thumbnail = 'http://www.pelisultra.com/wp-content/uploads/2017/03/logoultra2-1.png'

    url = build_url({'mode': 'ultra1'})
    li = xbmcgui.ListItem('Peliculas', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'ultra2-1' , 'direccion':'http://www.pelisultra.com/series/'})
    li = xbmcgui.ListItem('Series', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'ultra1':

    url = 'http://www.pelisultra.com'
    pattern = 'li(.*?ta.*?cat.*?href=.*)<'
    data = read(url)
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:

        pattern = '\<a.*\"\>(.*?)\<\/'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'href=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        thumbnail = 'http://www.pelisultra.com/wp-content/uploads/2017/03/logoultra2-1.png'
        fanart = ''
        info = 'Requests PelisUltra'

        url = build_url({'mode': 'ultra1-1', 'foldername': title, 'direccion': url})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'ultra1-1':
    url = args['direccion'][0]
    pattern = 'div.*id.*ml.*\n(.*\n.*\n.*)\/'
    data = read(url)
    pattern2 = 'link.*?next.*?href\=\'(.*?)\''
    pag = re.findall(pattern2, data, re.IGNORECASE)
    pag2 = pag[0]
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = 'alt=\"(.*?)\"'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'href=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'src=\"(.*?)\"'
        thumbnail = re.findall(pattern, match, re.MULTILINE)[0]
        thumbnail = thumbnail.replace("w185", "original")

        fanart = 'http://darkelite.ml/img/fondo.jpg'
        info = 'by JesusOSX '

        url = build_url({'mode': 'ultra1-2', 'foldername': title, 'direccion': url, 'thumbnail':thumbnail, 'fanart':fanart, 'info':info})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'ultra1-1', 'direccion': pag2})
    li = xbmcgui.ListItem('[COLOR red][B]Siguente Pagina[/B][/COLOR]',
                          iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png',
                          thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'ultra1-2':
    url = args['direccion'][0]
    name = args['foldername'][0]
    data = read(url)
    pattern = '(iframe.*?src=".*?".*?iframe)'
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:
        pattern = 'iframe.*?src=\"(.*?)\".*?ifra'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        info = ''

        pattern = 'pref.*\n.*\"(.*)\"'
        thumbnail = re.findall(pattern,  data, re.MULTILINE)[0]
        thumbnail = thumbnail.replace("w185", "original")

        pattern = 'pref.*\n.*\".*\".*\n.*\"(.*?)\"'
        fanart = re.findall(pattern,  data, re.MULTILINE)[0]
        fanart = fanart.replace("w780","original")


        if 'rapidvideo' in url:
            web = url
            opener = urllib2.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.71 Safari/537.36')]
            try:
                response = opener.open(web)
            except HTTPError as e:
                web=url

            except URLError as e:
                web = url

            else:
                data2 = response.read()
                pattern = '(a.*href.*ra.*q\=.*)'
                matches = re.findall(pattern, data2, re.IGNORECASE)
                for match in matches:

                    pattern = '.*?\"(.*?)\"'
                    url = re.findall(pattern, match, re.MULTILINE)[0]

                    if '360' in url:
                        title = name + '[COLOR lime][B]Opcion Rapidvideo Calidad 360 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    if '480' in url:
                        title = name + '[COLOR lime][B]Opcion Rapidvideo Calidad 480 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    if '720' in url:
                        title = name + '[COLOR lime][B]Opcion Rapidvideo Calidad 720 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)

                    if '1080' in url:
                        title = name + '[COLOR lime][B]Opcion Rapidvideo Calidad 1080 p[/B][/COLOR]'
                        url = build_url({'mode': 'play', 'playlink': url})
                        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                        li.setProperty('IsPlayable', 'true')
                        li.setProperty('fanart_image', fanart)
                        addMenuitem(url, li, False)


        if 'google' in url:
            title = name + '[COLOR lime][B]Opcion Gdrive[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'openload' in url:
            title = name + '[COLOR lime][B]Opcion Openload[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'streamango' in url:
            title = name + '[COLOR lime][B]Opcion StreaMango[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'downace' in url:
            title = name + '[COLOR lime][B]Opcion DownAce[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

        if 'youtube' in url:
            title = '[COLOR lime][B]Ver Trailer[/B][/COLOR]'
            url = 'http:' + url
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'ultra2-1':
    url = args['direccion'][0]
    pattern = 'div.*id.*ml.*\n(.*\n.*\n.*)\/'
    data = read(url)
    pattern2 = 'link.*?next.*?href\=\'(.*?)\''
    pag = re.findall(pattern2, data, re.IGNORECASE)
    pag2 = pag[0]
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = 'alt=\"(.*?)\"'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'href=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'src=\"(.*?)\"'
        thumbnail = re.findall(pattern, match, re.MULTILINE)[0]
        thumbnail = thumbnail.replace("w185", "original")

        fanart = 'http://darkelite.ml/img/fondo.jpg'
        info = 'by JesusOSX '

        url = build_url({'mode': 'ultra2-2', 'foldername': title, 'direccion': url, 'thumbnail':thumbnail, 'fanart':fanart, 'info':info})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    url = build_url({'mode': 'ultra2-1', 'direccion': pag2})
    li = xbmcgui.ListItem('[COLOR red][B]Siguente Pagina[/B][/COLOR]',
                          iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png',
                          thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'ultra2-2':
    url = args['direccion'][0]
    data = read(url)
    pattern = '(<div.*?numerando.*\n.*\n.*\n.*\n.*\n.*>)'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = '.*?([0-9]).*\n.*\n'
        temporada = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '\n.*?(\d+).*\<\/div'
        capitulo = re.findall(pattern, match, re.MULTILINE)[0]

        title = 'Temporada ' + temporada + ' Capitulo ' + capitulo


        pattern = 'href=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '\"fix.*\n.*src\=\"(.*?)\"'
        thumbnail = re.findall(pattern, data, re.MULTILINE)[0]
        thumbnail = thumbnail.replace("w185", "original")

        fanart = ''
        info = ' by JesusOSX'

        url = build_url({'mode': 'ultra2-3', 'foldername': title, 'direccion': url, 'thumbnail': thumbnail, 'fanart': fanart,'info': info})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'ultra2-3':
    url = args['direccion'][0]
    name = args['foldername'][0]
    data = read(url)
    pattern = '(iframe.*?src=".*?".*?iframe)'
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:

        pattern = 'src=\"(.*?)\"'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        info = ''


        thumbnail = ''

        fanart = ''



        if 'rapidvideo' in url:
            title = name + '[COLOR lime][B] Opcion Rapidvideo[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'google' in url:
            title = name + '[COLOR lime][B] Opcion Gdrive[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'openload' in url:
            title = name + '[COLOR lime][B] Opcion Openload[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'streamango' in url:
            title = name + '[COLOR lime][B] Opcion StreaMango[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)
        if 'downace' in url:
            title = name + '[COLOR lime][B] Opcion DownAce[/B][/COLOR]'
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'Novelas':
    fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'

    url = build_url({'mode': 'Novelas4'})
    li = xbmcgui.ListItem('Telenovelas en Transmision', iconImage='http://www.novelashdgratis.io/img/logo.gif',
                          thumbnailImage='http://www.novelashdgratis.io/img/logo.gif')
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'Novelas6'})
    li = xbmcgui.ListItem('Ultimas Telenovelas Agregadas', iconImage='http://www.novelashdgratis.io/img/logo.gif',
                          thumbnailImage='http://www.novelashdgratis.io/img/logo.gif')
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'Novelas5'})
    li = xbmcgui.ListItem('Transmision de Hoy', iconImage='http://www.novelashdgratis.io/img/logo.gif',
                          thumbnailImage='http://www.novelashdgratis.io/img/logo.gif')
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    url = build_url({'mode': 'Novelas1'})
    li = xbmcgui.ListItem('Novelas Finalizadas', iconImage='http://www.novelashdgratis.io/img/logo.gif',
                          thumbnailImage='http://www.novelashdgratis.io/img/logo.gif')
    li.setProperty('fanart_image', fanart)
    addMenuitem(url, li, True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'Novelas6':
    url = 'http://www.novelashdgratis.io/'
    data = read(url)
    pattern = 'div.*picture.*\n(.*)<\/a>'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:
        pattern = 'alt=\"(.*?)\"'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'href=\"(.*?)\"'
        link = re.findall(pattern, match, re.MULTILINE)[0]
        url = 'http://www.novelashdgratis.io/' + link

        thumbnail = 'http://www.novelashdgratis.io/img/logo.gif'
        fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'
        info = 'Novelas en Spokes'

        url = build_url({'mode': 'Novelas2', 'foldername': title, 'direccion': url})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Novelas5':
    url = 'http://www.novelashdgratis.io/'
    data = read(url)
    pattern = '<div.*?dia\".*\n.*\n(.*\n.*)div>'
    matches = re.findall(pattern, data, re.MULTILINE)
    for match in matches:

        pattern = '.*?title=\"(.*?)\">.*?div'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '.*?href="(.*?)".*?div'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        thumbnail = 'http://www.novelashdgratis.io/img/logo.gif'
        fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'
        info = 'Novelas en Spokes'

        url = build_url({'mode': 'Novelas3', 'foldername': title, 'direccion': url})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)



elif mode[0] == 'Novelas4':
    url = 'http://www.novelashdgratis.io/'
    data = read(url)
    pattern = 'div.*Transmiten.*\n.*\n.*(\n.*)>'
    data1 = re.findall(pattern, data, re.MULTILINE)[0]
    pattern2 = '<li>(.*?)<\/li'
    matches = re.findall(pattern2, data1, re.IGNORECASE)
    for match in matches:

        pattern = '.*?>(.*?)<\/a'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '.*?"(.*?)".*ti'
        link = re.findall(pattern, match, re.MULTILINE)[0]
        link = 'http://www.novelashdgratis.io' + link

        thumbnail = 'http://www.novelashdgratis.io/img/logo.gif'
        fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'
        info = 'Novelas en Spokes'

        url = build_url({'mode': 'Novelas2', 'foldername': title, 'direccion': link})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'Novelas1':
    url = 'http://www.novelashdgratis.io/'
    data = read(url)
    pattern = 'div.*Lista.*\n.*\n.*(\n.*)>'
    data1 = re.findall(pattern, data, re.MULTILINE)[0]
    pattern2 = '<li>(.*?)<\/li'
    matches = re.findall(pattern2, data1, re.IGNORECASE)
    for match in matches:

        pattern = '.*?>(.*?)<\/a'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '.*?"(.*?)".*ti'
        link = re.findall(pattern, match, re.MULTILINE)[0]
        link = 'http://www.novelashdgratis.io' + link

        thumbnail = 'http://www.novelashdgratis.io/img/logo.gif'
        fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'
        info = 'Novelas en Spokes'

        url = build_url({'mode': 'Novelas2', 'foldername': title, 'direccion': link})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Novelas2':
    website = args['direccion'][0]
    data = read(website)
    pattern = 'div.*lista-capitulos.*\n.*\n(.*)<\/ul>'
    data1 = re.findall(pattern, data, re.MULTILINE)[0]
    pattern2 = '<li(.*?)<\/li>'
    matches = re.findall(pattern2, data1, re.IGNORECASE)
    for match in matches:
        pattern = 'lcc.*?>(.*?)<\/a'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '.*?href=\"(.*?)\"'
        link = re.findall(pattern, match, re.MULTILINE)[0]
        link = 'http://www.novelashdgratis.io' + link

        thumbnail = 'http://www.novelashdgratis.io/img/logo.gif'
        fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'
        info = 'Novelas en Spokes'

        url = build_url({'mode': 'Novelas3', 'foldername': title, 'direccion': link})
        li = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('fanart_image', fanart)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                    listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'Novelas3':
    website = args['direccion'][0]
    data = read(website)
    pattern = 'div.*contenido_tab.*\n(.*)'
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:

        thumbnail = 'http://www.novelashdgratis.io/img/logo.gif'
        fanart = 'http://s2.dmcdn.net/JHwgw/1280x720-HSm.jpg'
        info = 'Novelas en Spokes'


        pattern = '.*?>(.*?)\('
        title = re.findall(pattern, match, re.MULTILINE)[0]

        if 'openload' in title:
            title = '[COLOR lime][B]Opcion Openload[/B][/COLOR]'

        elif 'netu' in title:
            title = '[COLOR lime][B]Opcion Netu[/B][/COLOR]'

        elif 'gamo' in title:
            title = '[COLOR lime][B]Opcion Gamovideo[/B][/COLOR]'




        pattern = '.*?\("(.*?)"\)'
        code = re.findall(pattern, match, re.MULTILINE)[0]
        if 'Openload' in title:
            url = 'https://openload.co/embed/' + code
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

        elif 'Netu' in title:
            url = 'https://waaw.tv/watch_video.php?v=' + code
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)

        elif 'Gamovideo' in title:
            url = 'http://gamovideo.com/' + code
            url = build_url({'mode': 'play', 'playlink': url})
            li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
            li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
            li.setProperty('IsPlayable', 'true')
            li.setProperty('fanart_image', fanart)
            addMenuitem(url, li, False)









    xbmcplugin.endOfDirectory(addon_handle)













elif mode[0] == 'karaoke':
    url = build_url({'mode': 'karaokesearch'})
    li = xbmcgui.ListItem('Buscar Karaoke',
                          iconImage='https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg',
                          thumbnailImage='https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg')
    addMenuitem(url, li, True)

    web = 'https://www.redkaraoke.com/genre'
    data = read(web)
    pattern = '<li>(.*href.*\n.*<h3>.*\n.*\n.*)<\/li>'
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:

        pattern = 'h3>(.*?)<\/h3'
        name = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = 'href=\"(.*?)\"'
        url2 = re.findall(pattern, match, re.MULTILINE)[0]
        url = 'https://www.redkaraoke.com' + url2

        info = 'Karaoke en Spokes'
        thumbnail = 'https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg'
        fanart =  'https://lh3.googleusercontent.com/RxPAWt2xSDH0NgAeUbAch6Css6lhQbfPTPfpwJfEzZmTTop8zCmgsMGw0ygOj5gca8yE=h1264'

        url = build_url({'mode': 'karrequest', 'foldername': name, 'direccion': url})
        li = xbmcgui.ListItem(name, iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": name, "FileName": name, "Plot": info})
        li.setProperty('fanart_image', fanart)
        addMenuitem(url, li, True)


    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'karrequest':
    website = args['direccion'][0]
    data = read(website)
    pattern = '<button onClick=\"javascript\:singSong(.*?youtube.*?)"'
    pattern2 = '<li class=\"pagination\-next\"><a href=\"(.*?)\"'
    pag = re.findall(pattern2, data, re.IGNORECASE)
    pag2 = 'https://www.redkaraoke.com' + pag[0]
    matches = re.findall(pattern, data, re.IGNORECASE)
    for match in matches:

        pattern = '\'(.*?)\'.*'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        thumbnail = 'https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg'

        fanart = 'https://lh3.googleusercontent.com/RxPAWt2xSDH0NgAeUbAch6Css6lhQbfPTPfpwJfEzZmTTop8zCmgsMGw0ygOj5gca8yE=h1264'
        info = 'Karaoke en Spokes'

        pattern = '.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'(.*?)\'.*'
        url = re.findall(pattern, match, re.MULTILINE)[0]
        url = 'https://www.youtube.com/watch?v=' + url

        url = build_url({'mode': 'play', 'playlink': url})
        li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
        li.setProperty('IsPlayable', 'true')
        li.setProperty('fanart_image', fanart)
        addMenuitem(url, li, False)

    url = build_url({'mode': 'karrequest' , 'direccion': pag2})
    li = xbmcgui.ListItem('Siguente Pagina',
                          iconImage='https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg',
                          thumbnailImage='https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg')
    addMenuitem(url, li, True)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'karaokesearch':
    website = 'https://www.redkaraoke.com/searchengine?keywords='
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Buscar un Karaoke')
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
            search_term = search_term.replace(" ","%20")
            dir = website + search_term
            html = read(dir)
            pattern = '<button onClick=\"javascript\:singSong(.*?youtube.*?)"'
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                pattern = '\'(.*?)\'.*'
                title = re.findall(pattern, match, re.MULTILINE)[0]

                thumbnail = 'https://i.pinimg.com/736x/6d/4e/d9/6d4ed9bda988e53269d0e925a259b612--karaoke-logos.jpg'

                fanart = 'https://lh3.googleusercontent.com/RxPAWt2xSDH0NgAeUbAch6Css6lhQbfPTPfpwJfEzZmTTop8zCmgsMGw0ygOj5gca8yE=h1264'
                info = 'Karaoke en Spokes'

                pattern = '.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'.*?\'(.*?)\'.*'
                url = re.findall(pattern, match, re.MULTILINE)[0]
                url = 'https://www.youtube.com/watch?v=' + url

                url = build_url({'mode': 'play', 'playlink': url})
                li = xbmcgui.ListItem(title, iconImage=thumbnail, thumbnailImage=thumbnail)
                li.setInfo("video", {"Title": title, "FileName": title, "Plot": info})
                li.setProperty('IsPlayable', 'true')
                li.setProperty('fanart_image', fanart)
                addMenuitem(url, li, False)


            xbmcplugin.endOfDirectory(addon_handle)





elif mode[0] == 'search':
    website = args['site'][0]
    search_string = getusersearch(website)
    yotube_search_url = scrape_url + search_url + \
        search_string.replace(" ", "+")
    xbmcplugin.setContent(addon_handle, 'movies')
    bstheurl(yotube_search_url)


elif mode[0] == 'search2':
    website = args['site'][0]
    titulo = args['titulo'][0]
    string = 'Trailer '+titulo+' latino'
    search_string = string
    yotube_search_url = scrape_url + search_url + \
        search_string.replace(" ", "+")
    xbmcplugin.setContent(addon_handle, 'movies')
    bstheurl(yotube_search_url)

elif mode[0] == 'play':
    final_link = args['playlink'][0]
    print "in mode play"
    print final_link
    play_video(final_link)


elif mode[0] == '0': #lista de secciones

    url = build_url({'mode': '1', 'direccion': systempjos1})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Anime en Emision[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Aqui encontraras tus Animes en Emision'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = build_url({'mode': '1', 'direccion': systempjos2})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Todos los Animes[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Seccion Donde Estan Todos los Animes Finalizados'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = build_url({'mode': '5'})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Buscar un Anime[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Ingresa Datos para hacer Busqueda de un Anime'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    endMenu()

elif mode[0] == '1': #mostrar lista de animes
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


        url = build_url({'mode': '2','direccion':url,'thumbnail':thumbnail})
        li = xbmcgui.ListItem('[COLOR orange][B]'+ title + '[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
        li.setInfo("tvshows", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)


    pattern2 = 'page.*last.*?href\=\"(.*?)\"\>'
    paginacion = re.findall(pattern2, data, re.DOTALL)[0]
    url = build_url({'mode': '1', 'direccion': paginacion})
    li = xbmcgui.ListItem('[COLOR red][B]Siguente Pagina[/B][/COLOR]',
                          iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png',
                          thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)

    endMenu()

elif mode[0] == '2':  #Mostrar episodios
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

        url = build_url({'mode': '3', 'direccion': url, 'thumbnail': thumbnail})
        li = xbmcgui.ListItem('[COLOR green][B]' + title + '[/B][/COLOR]', iconImage=thumbnail,thumbnailImage=thumbnail)
        li.setInfo("tvshows", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)
    endMenu()


elif mode[0] == '3':   #servers para reproducir
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


elif mode[0] == '4':
    thumbnail = args['thumbnail'][0]
    response = 'http://s2.animeyt.tv/narutos_animeyt.php'
    id = re.findall('id=([0-9]+).*', datos, re.DOTALL)[0]
    file = re.findall('file\=(.*)', datos, re.DOTALL)[0]
    token = 'eyJjdCI6IjJhckx0bDIrRmlzQzliaU5UazdsblE9PSIsIml2IjoiZTJhNWIyYWJlOTIxOTUyOGI5M2ZiMjAzZDY0YjRhOTYiLCJzIjoiODJlMjhiNTM0ZDg1ZWI1YyJ9'
    handler = 'Animeyt'
    opener = urllib2.build_opener()
    data_post = urllib.urlencode({'cd': id, 'file': file, 'token': token, 'handler': handler})
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.71 Safari/537.36')]
    f = opener.open(response, data_post)
    parse = f.read()
    pattern1 = 'file\"\:\"(.*?)\"'
    web = re.findall(pattern1, parse, re.DOTALL)[0]
    url = web.replace("\\", "")
    li = xbmcgui.ListItem('[COLOR yellow][B]Reproducir[/B][/COLOR]', iconImage=thumbnail,thumbnailImage=thumbnail)
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, False)
    endMenu()


elif mode[0] == '5': #search animeyt
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

                url = build_url({'mode': '2', 'direccion': url, 'thumbnail': thumbnail})
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


elif mode[0] == 'animeflv': #lista secciones

    url = build_url({'mode': 'flvactualizados', 'direccion': 'https://animeflv.net/browse?order=added'})
    thumbnail = 'https://pm1.narvii.com/5610/c07d6c52e768eb8d7a79d81223402fc56611971b_hq.jpg'
    li = xbmcgui.ListItem('[COLOR orange][B]Anime Recientemente Actualizados[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Aqui encontraras tus Animes Recientemente Actualizados'})
    li.setProperty('fanart_image', 'https://kasukabe48.files.wordpress.com/2016/07/1444014275-106dee95104209bb9436d6df2b6d5145.jpg?w=1200')
    addMenuitem(url, li, True)

    url = build_url({'mode': 'flvagregados', 'direccion': 'https://animeflv.net/browse?order=updated'})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Animes Agregados Recientemente[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Seccion Donde Estan Todos los Animes Finalizados'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = build_url({'mode': 'flvsearch'})
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Buscar un Anime[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Ingresa Datos para hacer Busqueda de un Anime'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    endMenu()

elif mode[0] == 'flvactualizados':  #actualizados recientes
    actualizados = args['direccion'][0]
    data = read(actualizados)
    pattern =  '(\<article.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)'
    matches = re.findall(pattern,data,re.IGNORECASE)
    for match in matches:
        pattern = 'a href="/anime/(.*?)"'
        url = re.findall(pattern,match,re.MULTILINE)[0]

        pattern = 'img src="(.*?)"'
        thumbnail = re.findall(pattern,match,re.MULTILINE)[0]

        pattern = 'class="Title">(.*?)<'
        title = re.findall(pattern,match,re.MULTILINE)[0]

       # pattern = '<p>(.*?)</p>.*\n.*<span'
       # info = re.findall(pattern,match,re.MULTILINE)[0]


        url = build_url({'mode': 'flvepisodios','direccion':'https://animeflv.net/anime/'+url,'thumbnail':'https://animeflv.net'+thumbnail})
        li = xbmcgui.ListItem('[COLOR orange][B]'+ title + '[/B][/COLOR]', iconImage='https://animeflv.net'+thumbnail, thumbnailImage='https://animeflv.net'+thumbnail)
        li.setInfo("video", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)


    pattern2 = '<li><a href="(.*?)" rel="next"'
    paginacion = re.findall(pattern2, data, re.DOTALL)[0]
    url = build_url({'mode': 'flvactualizados', 'direccion': 'https://animeflv.net' + paginacion})
    li = xbmcgui.ListItem('[COLOR red][B]Siguente Pagina[/B][/COLOR]'+paginacion,
                          iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png',
                          thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)

    endMenu()

elif mode[0] == 'flvagregados':  #actualizados recientes
    actualizados = args['direccion'][0]
    data = read(actualizados)
    pattern =  '(\<article.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)'
    matches = re.findall(pattern,data,re.IGNORECASE)
    for match in matches:
        pattern = 'a href="/anime/(.*?)"'
        url = re.findall(pattern,match,re.MULTILINE)[0]

        pattern = 'img src="(.*?)"'
        thumbnail = re.findall(pattern,match,re.MULTILINE)[0]

        pattern = 'class="Title">(.*?)<'
        title = re.findall(pattern,match,re.MULTILINE)[0]

      #  pattern = '</p>.*\n.*<p>(.*?)</p>'
       # plot = re.findall(pattern,match,re.MULTILINE)[0]


        url = build_url({'mode': 'flvepisodios','direccion':'https://animeflv.net/anime/'+url,'thumbnail':'https://animeflv.net'+thumbnail})
        li = xbmcgui.ListItem('[COLOR orange][B]'+ title + '[/B][/COLOR]', iconImage='https://animeflv.net'+thumbnail, thumbnailImage='https://animeflv.net'+thumbnail)
        li.setInfo("tvshows", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)


    pattern2 = '.*?browse?order=added&page=(.*?)"'
    paginacion = re.findall(pattern2, data, re.DOTALL)[0]
    url = build_url({'mode': 'flvactualizados', 'direccion': 'https://animeflv.net' + paginacion})
    li = xbmcgui.ListItem('[COLOR red][B]Siguente Pagina #[/B][/COLOR]'+paginacion,
                          iconImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png',
                          thumbnailImage='http://2.bp.blogspot.com/-q5yGYcBCQzg/Uv1E2m4c6oI/AAAAAAAAA7I/mK2JPXZh1w0/s1600/SIGUIENTE.png')
    addMenuitem(url, li, True)
    xbmcplugin.endOfDirectory(addon_handle)

    endMenu()



elif mode[0] == 'flvepisodios':  #Mostrar episodios
    emision = args['direccion'][0]
    thumbnail = args['thumbnail'][0]
    data = read(emision)
    pattern = '(\<li class="fa-play-circle">.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)'
    matches = re.findall(pattern, data, re.IGNORECASE)

    for match in matches:
        pattern = '<a href="/ver/(.*?)">'
        url = re.findall(pattern, match, re.MULTILINE)[0]

        pattern = '<p>(.*?)</p>'
        title = re.findall(pattern, match, re.MULTILINE)[0]

        thumbnail = thumbnail

        url = build_url({'mode': 'flvservers', 'direccion': 'https://animeflv.net/ver/'+url, 'thumbnail': thumbnail})
        li = xbmcgui.ListItem('[COLOR green][B]'+ title + '[/B][/COLOR]', iconImage=thumbnail,thumbnailImage=thumbnail)
        li.setInfo("movies", {"Title": title, "FileName": title})
        li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
        addMenuitem(url, li, True)
    endMenu()


elif mode[0] == 'flvservers':   #servers para reproducir
    emision = args['direccion'][0]
    thumbnail = args['thumbnail'][0]
    data = read(emision)
    pattern = 's3.animeflv.com/(.*?)="'
    url = re.findall(pattern, data, re.MULTILINE)[0]

    mediaf= 'https://s3.animeflv.com/'+url+'='
    data2=read(mediaf)
    pattern2 = 'https://www.mediafire.com/file/(.*?)/'
    url2 = re.findall(pattern2,data2,re.MULTILINE)[0]

    scramed = 'https://www.mediafire.com/file/'+url2
    data3=read(scramed)
    pattern3 = 'https://www.mediafire.com/file/(.*?).mp4'
    url3 = re.findall(pattern3,data3,re.MULTILINE)[0]



    thumbnail = thumbnail
    url = build_url({'mode': 'play', 'playlink':'https://www.mediafire.com/file/' + url3})
    li = xbmcgui.ListItem('[COLOR skyblue][B]Opcion Mediafire[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setProperty('IsPlayable', 'true')
    li.setProperty('fanart_image',thumbnail)
    addMenuitem(url, li, False)




    endMenu()


elif mode[0] == 'flvsearch':
    website= 'https://animeflv.net/browse?q='
    kb = xbmc.Keyboard('default', 'heading')
    kb.setDefault('')
    kb.setHeading('Buscar en la Coleccion FLV')
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
            pattern =  '(\<article.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*)'
            matches = re.findall(pattern,html,re.IGNORECASE)
            for match in matches:
				pattern = 'a href="/anime/(.*?)"'
				url = re.findall(pattern,match,re.MULTILINE)[0]

				pattern = 'img src="(.*?)"'
				thumbnail = re.findall(pattern,match,re.MULTILINE)[0]

				pattern = 'class="Title">(.*?)<'
				title = re.findall(pattern,match,re.MULTILINE)[0]

				url = build_url({'mode': 'flvepisodios','direccion':'https://animeflv.net/anime/'+url,'thumbnail':'https://animeflv.net'+thumbnail})
				li = xbmcgui.ListItem('[COLOR orange][B]'+ title + '[/B][/COLOR]', iconImage='https://animeflv.net'+thumbnail, thumbnailImage='https://animeflv.net'+thumbnail)
				li.setInfo("tvshows", {"Title": title, "FileName": title})
				li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
				addMenuitem(url, li, True)

            xbmcplugin.endOfDirectory(addon_handle)

            endMenu()

    else:
        dialog = xbmcgui.Dialog()
        dialog.notification("Spokes", 'La Busqueda se cancelo',
                            xbmcgui.NOTIFICATION_INFO, 3500 , False)
