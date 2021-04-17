# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.adtv


from __future__ import unicode_literals
import json
import xbmcplugin
import sys
import urlquick
import re

from .vars import *
from .tools import *
from .create_item import addDir
from .create_item import addLink


def browseCategories():
    log('browseCategories')
    log(" Fetching url: %s" % CATEGORIES_URL)
    log(" Fetching params: %s" % CATEGORIES_PARAMS)
    categories = json.loads(
                    urlquick.get(CATEGORIES_URL,
                            params=CATEGORIES_PARAMS,
                            headers=headers).text)
    categories.append({'id': '', 'title_ar': 'كل البرامج'})
    for category in categories:
        category_id = category['id']
        if category_id == "216860" or category_id == "214429" or category_id == "219422":
            continue
        category_name = formatTitles(category['title_ar'])
        SHOWS_PARAMS.update({'cat_id': category_id})
        infos = json.dumps(SHOWS_PARAMS)
        addDir(category_name, infos, 4)

def browseBlocks(genre_id):
    log('browseBlocks')
    log(" Fetching url: %s" % BLOCKS_URL)
    log(" Fetching params: %s" % BLOCKS_PARAMS)
    BLOCKS_PARAMS.update({'genre_id': genre_id})
    blocks = json.loads(
                urlquick.get(BLOCKS_URL,
                        params=BLOCKS_PARAMS,
                        headers=headers).text)['data']
    for block in blocks:
        block_id =  block['id']
        if str(block_id) == '3':
            continue 
        block_name = block['title_ar']
        BLOCK_PARAMS.update({'block_id': block_id})
        infos = json.dumps(BLOCK_PARAMS)
        addDir(block_name, infos, 3)
        

def getTvShows(infos):
    log('getTvShows')
    xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    BLOCK_PARAMS = json.loads(infos)
    log(" Fetching url: %s" % BLOCK_URL)
    log(" Fetching params: %s" % BLOCK_PARAMS)
    apijson = json.loads(
                urlquick.get(BLOCK_URL,
                    headers=headers,
                    params=BLOCK_PARAMS).text)
    for item in apijson['data']:
        title = formatTitles(item['title_ar'])
        showId = item['id']
        thumb_path = item['thumbnail']
        fanart_path = (item['atv_thumbnail'] or item['thumbnail'])
        thumb = IMG_BASE_URL % thumb_path
        fanart = IMG_BASE_URL % fanart_path
        infoList = {
                    "mediatype": "tvshows",
                    "title": title,
                    "TVShowTitle": title,
                }
        infoArt = {
                    "thumb": thumb,
                    "poster": thumb,
                    "fanart": fanart,
                    "icon": ICON,
                    "logo": ICON
                }
        infos = json.dumps({
                            'showId': showId,
                            'thumb': thumb,
                        })
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_TITLE)
        addDir(title, showId, 5, infoArt, infoList,0, showId)


def getTvPrograms(infos):
    log('getTvShows')
    xbmcplugin.setContent(int(sys.argv[1]), 'videos')
    SHOWS_PARAMS = json.loads(infos)
    log(" Fetching url: %s" % SHOWS_URL)
    log(" Fetching params: %s" % SHOWS_PARAMS)
    apijson = json.loads(
                urlquick.get(SHOWS_URL,
                    headers=headers,
                    params=SHOWS_PARAMS).text)
    for item in apijson['data']['shows']:
        title = formatTitles(item['title_ar'])
        showId = item['id']
        plot =  item['description_ar']
        thumb_path = item['thumbnail']
        fanart_path = (item['atv_thumbnail'] or item['cover'] or item['thumbnail'])
        thumb = IMG_BASE_URL % thumb_path
        fanart = IMG_BASE_URL % fanart_path
        infoList = {
                    "mediatype": "tvshows",
                    "title": title,
                    "TVShowTitle": title,
                    "plot": plot
                }
        infoArt = {
                    "thumb": thumb,
                    "poster": thumb,
                    "fanart": fanart,
                    "icon": ICON,
                    "logo": ICON
                }
        infos = json.dumps({
                            'showId': showId,
                            'thumb': thumb,
                        })
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_TITLE)
        addDir(title, showId, 5, infoArt, infoList,0, showId)


def getEpisodes(showId):
    log('getEpisodes')
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    SHOW_PARAMS.update({'show_id': showId})
    log(" Fetching url: %s" % SHOW_URL)
    log(" Fetching params: %s" % SHOW_PARAMS)
    items = json.loads(urlquick.get(SHOW_URL, params=SHOW_PARAMS,
                    headers=headers).text)
    showTitle = items['cat']['title_ar']
    for item in items['videos']:
        streamID = item['id']
        title = formatTitles(item['title_ar'])
        tags = item['tags']
        thumb = IMG_BASE_URL % item['img']
        aired = str(item['publish_time']).split(' ')[0]
        duration = item['duration']
        infoLabels = {
                        "mediatype": "episode",
                        "title": title,
                        "aired": aired,
                        "duration": duration,
                        "TVShowTitle": showTitle
                    }
        infoArt = {
                    "thumb":thumb,
                    "poster":thumb,
                    "fanart":thumb,
                    "icon":thumb,
                    "logo":thumb
                }
        try:
            ep = re.compile(r'.*ep\-(.*?)$').findall(tags)[0].split(',')[0]
            episode_number = int(ep)
            infoLabels.update({'episode': episode_number, 'season': 1})
            xbmcplugin.addSortMethod(int(sys.argv[1]) , xbmcplugin.SORT_METHOD_EPISODE)
        except:
            pass
        addLink(title, streamID, 9, infoLabels, infoArt, len(items['videos']))
