# -*- coding: utf-8 -*-

import re
import urlparse

from channels import renumbertools
from core import httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core import tmdb
from platformcode import config,logger

__modo_grafico__ = config.get_setting('modo_grafico', 'animeyt')

HOST = "http://animeyt.tv/"
systempjos1 = 'http://www.animeyt.tv/emision'
systempjos2= 'http://www.animeyt.tv/animes'
systempjos3= 'http://www.animeyt.tv'

def animeyt(): #lista de secciones

    url = animeytreciente(systempjos3)
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Capitulos Recientes[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Seccion Donde Estan Todos los Animes Finalizados'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = animeytlista(systempjos1)
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Anime en Emision[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Aqui encontraras tus Animes en Emision'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = animeytlista(systempjos2)
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Todos los Animes[/B][/COLOR]', iconImage=thumbnail, thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Seccion Donde Estan Todos los Animes Finalizados'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    url = animeytsearch()
    thumbnail = 'https://3.bp.blogspot.com/-2Syl4EthAAg/VtOq5pCnmdI/AAAAAAAAACY/4QwHamZIyFIscovoVHdzkOzcNXJDWG9Vw/s1600/bleach4.png'
    li = xbmcgui.ListItem('[COLOR orange][B]Buscar un Anime[/B][/COLOR]', iconImage=thumbnail,
                          thumbnailImage=thumbnail)
    li.setInfo("video", {"Plot": 'Ingresa Datos para hacer Busqueda de un Anime'})
    li.setProperty('fanart_image', 'https://i1.wp.com/www.gamerfocus.co/wp-content/uploads/2017/03/anime.jpeg')
    addMenuitem(url, li, True)

    endMenu()

def animeytreciente(url):  #Mostrar episodios
    emision = url
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

def animeytlista(url): #mostrar lista de animes
    emision = url
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

def animeytepi(url,thumbnail):  #Mostrar episodios
    emision = url
    thumbnail = thumbnail
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


def animeytservers(url,thumbnail):   #servers para reproducir
    emision = url
    thumbnail = thumbnail
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



def animeytsearch(): #search animeyt
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