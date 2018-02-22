# -*- coding: utf-8 -*-

import re
import xbmcgui
from core import scrapertools
from platformcode import logger


# Returns an array of possible video url's from the page_url
def get_google_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    duration = 7500
    dialog = xbmcgui.Dialog()
    
    video_urls = []

    # Lo extrae a partir de flashvideodownloader.org
    if page_url.startswith("http://"):
        url = 'http://www.flashvideodownloader.org/download.php?u=' + page_url
    else:
        url = 'http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid=' + page_url
    logger.info("url=" + url)
    data = scrapertools.cache_page(url)

    # Extrae el vídeo
    newpatron = '</script>.*?<a href="(.*?)" title="Click to Download">'
    newmatches = re.compile(newpatron, re.DOTALL).findall(data)
    dialog.ok("spokes",newmatches[0])
    if len(newmatches) > 0:
        video_urls.append(["[googlevideo]", newmatches[0]])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return newmatches
