import xbmcaddon,os,requests,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin

def mainMenu():
   addDir3('Live Tv','goLiveTV',2,'https://www.materialui.co/materialIcons/notification/live_tv_black_192x192.png','','')
   addDir3('Movies','goMovies',4,'https://cdn2.iconfinder.com/data/icons/bazza-internet-and-websites/60/12_-_Film_slate-512.png','','')
   addDir3('Series','goSeries',3,'https://cdn2.iconfinder.com/data/icons/bazza-internet-and-websites/60/12_-_Film_slate-512.png','','')
   
def liveTv():   
	addDir3('[COLOR cyan][B]Izzi[/B][/COLOR]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/lista.txt',20,'http://lh3.googleusercontent.com/nkg3nSt-FYi98ZNk6ITz6qjbgzUKSaVZn6p-DGu_eTrQ0uPAhlmXDEedOIexAY1NBQ=w300','','')
	addDir3('[COLOR red][B]IPTV Canales[/B][/COLOR]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/snake.txt',21,'https://iptvcanales.com/wp-content/uploads/2018/01/logo.png','','')
   
def MoviesCategories():
	addDir3('Todas [Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/movies.txt',40,'http://cdn.revistagq.com/uploads/images/thumbs/201536/superheroes_gq_4812_645x485.jpg','','')
	addDir3('Todas [Ingles/Sub]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/movies.txt',41,'http://cdn.revistagq.com/uploads/images/thumbs/201536/superheroes_gq_4812_645x485.jpg','','')
	addDir3('Accion [Ingles/Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/accion.txt',42,'http://icons.veryicon.com/ico/System/Icons8%20Metro%20Style/Movie%20Genres%20Action.ico','','')
	addDir3('Animacion [Ingles/Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/animacion.txt',43,'https://cdn3.iconfinder.com/data/icons/movies-3/32/shrek-character-animation-movie-ogre-512.png','','')
	addDir3('Comedia [Ingles/Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/comedia.txt',44,'https://d30y9cdsu7xlg0.cloudfront.net/png/60743-200.png','','')
	addDir3('Drama [Ingles/Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/drama.txt',45,'http://icons.veryicon.com/ico/System/iOS7%20Minimal/Movie%20Genres%20Drama.ico','','')
	addDir3('Romance [Ingles/Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/romance.txt',46,'http://icons.iconarchive.com/icons/icons8/ios7/256/Cinema-Romance-icon.png','','')
	addDir3('Terror [Ingles/Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/terror.txt',47,'http://www.iconarchive.com/download/i87740/icons8/ios7/Cinema-Horror-2.ico','','')
	
def seriesCategories():
	addDir3('Alf [Latino]','https://raw.githubusercontent.com/xxspokiixx/testkod/master/alf.txt',30,'http://lh3.googleusercontent.com/nkg3nSt-FYi98ZNk6ITz6qjbgzUKSaVZn6p-DGu_eTrQ0uPAhlmXDEedOIexAY1NBQ=w300','','')
	
def channel():
	if mode==20:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/lista.txt'
		createListMenu(l)
	elif mode==21:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/plugin.video.ShortyLiveTV/canalesTemp.m3u'
		createListM3U(l)
		 
def seriesPlay():
	if mode==30:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/alf.txt'
		createListMenu(l)
	elif mode==None:
		print "Oops!..."
		
def pelis():
	if mode==40:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/movies.txt'
		createListMenu(l)
	elif mode==41:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/movies.txt'
		createListMenu(l)
	elif mode==42:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/accion.txt'
		createListMenu(l)
	elif mode==43:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/animacion.txt'
		createListMenu(l)
	elif mode==44:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/comedia.txt'
		createListMenu(l)
	elif mode==45:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/drama.txt'
		createListMenu(l)
	elif mode==46:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/romance.txt'
		createListMenu(l)
	elif mode==47:
		l= 'https://raw.githubusercontent.com/xxspokiixx/testkod/master/terror.txt'
		createListMenu(l)
		
#def Moviess():
 #  r = requests.get('')
  # match = re.compile('<div class="folder-cell"><a href="(.+?)">(.+?)</a></div>').findall(r.content)
   #for videoUrl,videoName  in match:
    # addLink(videoName,'https://www.googledrive.com%s'%videoUrl,'','','')

def createListMenu(l):
		r = requests.get(l)
		match = re.compile('logo= "(.+?)" name= "(.+?)" url= "(.+?)"').findall(r.content)
		for logo,name,link in match:
			addLink(name,link,logo,'','')

def createListM3U(l):
		r = requests.get(l)
		match = re.compile('^#EXTINF:-?[0-9]*(.*?),(.*?)\n(.*?)$',re.I+re.M+re.U+re.S).findall(r.content)
		for logo,name,link in match:
			addLink(name,link,logo,'','')
	 
def addLink(name,url,image,urlType,fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable','true')
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param       
#################################################################################################################

#                               NEED BELOW CHANGED

  
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
     
def addDir2(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % viewType )
 


              
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
   
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        mainMenu()
       
elif mode==1:
        OPEN_URL(url)
elif mode==2:
		print ""
		liveTv()
elif mode==3:
		print ""
		seriesCategories()
elif mode==4:
        print ""
        MoviesCategories()
elif mode==20 or mode<=29:
        channel()	
elif mode==30 or mode<=39:
		seriesPlay()
elif mode==40 or mode<=49:
		pelis()

		


        


xbmcplugin.endOfDirectory(int(sys.argv[1]))
