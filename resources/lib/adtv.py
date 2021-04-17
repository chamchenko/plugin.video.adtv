# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.adtv

from __future__ import unicode_literals

import sys
import json
import urlquick
import xbmcgui
import xbmcplugin
import inputstreamhelper

from .tools import *
from .livetv import browseLiveTV
from .tvshows import *
from .create_item import addDir
from .vars import *

class ADTV(object):
    def __init__(self):
        log('__init__')
    def buildMenu(self):
        for item in MAIN_MENU: addDir(*item)
    def browseLive(self):
        browseLiveTV()
    def browseProgramsMenu(self):
        browseCategories()
    def browseShowsMenu(self, genre_id):
        browseBlocks(genre_id)
    def browseShows(self, infos):
        getTvShows(infos)
    def browsePrograms(self, infos):
        getTvPrograms(infos)
    def browseEpisodes(self, infos):
        getEpisodes(infos)


    def playLive(self, name, channel_id):
        PARAMS_LIVE_TV.update({'channel_id': channel_id})
        log(" Fetching url: %s" % URL_LIVE)
        log(" Fetching params: %s" % PARAMS_LIVE_TV)
        json_parser = json.loads(urlquick.get(URL_LIVE, params=PARAMS_LIVE_TV).text)
        playbackURL = json_parser['playbackURL']
        liz = xbmcgui.ListItem(name, path=playbackURL)
        liz.setProperty(INPUTSTREAM_PROP,'inputstream.adaptive')
        liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
        liz.setProperty('inputstream.adaptive.stream_headers', 'User-Agent=%s' % USER_AGENT)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=liz)


    def playVideo(self, name, streamID, liz=None):
        EPISODE_PARAMS.update({'id': streamID})
        json_parser = json.loads(
                        urlquick.get(EPISODE_URL,
                            params=EPISODE_PARAMS,
                            max_age=-1).text)
        playbackURL = json_parser['playbackURL']
        if 'drm' in playbackURL:
            is_helper = inputstreamhelper.Helper('mpd', drm='com.widevine.alpha')
            if is_helper.check_inputstream():
                playbackURL = json_parser['playbackURL']['dash_url']
                licenseURL = json_parser['playbackURL']['widevine_key_url']
                LICENCE_KEY_TEMP = '%s|User-Agent=%s&Content-Type=|R{SSM}|'
                liz = xbmcgui.ListItem(name, path=playbackURL)
                URL_LICENCE_KEY = LICENCE_KEY_TEMP % (licenseURL, USER_AGENT)
                liz.setProperty(INPUTSTREAM_PROP,'inputstream.adaptive')
                liz.setProperty('inputstream.adaptive.manifest_type', 'mpd')
                liz.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
                liz.setProperty('inputstream.adaptive.license_key', URL_LICENCE_KEY)
            else:
                return
        else:
            liz = xbmcgui.ListItem(name, path=playbackURL)
            liz.setProperty(INPUTSTREAM_PROP,'inputstream.adaptive')
            liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
        liz.setProperty('inputstream.adaptive.stream_headers', 'User-Agent=%s' % USER_AGENT)
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem=liz)

        
params=getParams()
try: url=unquote_plus(params["url"])
except: url=None
try: name=unquote_plus(params["name"]).encode('utf-8').strip().decode('utf-8')
except: name=None
try: mode=int(params["mode"])
except: mode=None
log("Mode: "+str(mode))
log("URL : "+str(url))
log("Name: "+str(name))

if  mode==None: ADTV().buildMenu()
elif mode == 1: ADTV().browseLive()
elif mode == 2: ADTV().browseShowsMenu(url)
elif mode == 3: ADTV().browseShows(url)
elif mode == 4: ADTV().browsePrograms(url)
elif mode == 5: ADTV().browseEpisodes(url)
elif mode == 6: ADTV().browseProgramsMenu()
elif mode == 8: ADTV().playLive(name, url)
elif mode == 9: ADTV().playVideo(name, url)

xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
