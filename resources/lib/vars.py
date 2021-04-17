# -*- coding: utf-8 -*-
# Copyright: (c) 2016, Chamchenko
# GNU General Public License v2.0+ (see LICENSE.txt or https://www.gnu.org/licenses/gpl-2.0.txt)
# This file is part of plugin.video.adtv

from __future__ import unicode_literals
import xbmcaddon
from xbmc import getInfoLabel
ADDON_ID = 'plugin.video.adtv'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
ADDON_NAME = REAL_SETTINGS.getAddonInfo('name')
SETTINGS_LOC = REAL_SETTINGS.getAddonInfo('profile')
ADDON_PATH = REAL_SETTINGS.getAddonInfo('path')
ADDON_VERSION = REAL_SETTINGS.getAddonInfo('version')
ICON = REAL_SETTINGS.getAddonInfo('icon')
FANART = REAL_SETTINGS.getAddonInfo('fanart')
LANGUAGE = REAL_SETTINGS.getLocalizedString
DEBUG = REAL_SETTINGS.getSetting('Debugging') == 'true'
XBMC_VERSION = int(getInfoLabel("System.BuildVersion").split('-')[0].split('.')[0])
INPUTSTREAM_PROP = 'inputstream' if XBMC_VERSION >= 19 else 'inputstreamaddon'
USER_AGENT = "ADtv/7 CFNetwork/1220.1 Darwin/20.3.0"
headers = {"User-Agent": USER_AGENT}


IMG_BASE_URL = 'https://admango.cdn.mangomolo.com/analytics/%s'
API_BASE_URL = 'https://admin.mgmlcdn.com/analytics/index.php/'
URL_LIVES = API_BASE_URL + 'plus/live_channels'
URL_LIVE = API_BASE_URL + 'plus/getchanneldetails'
CATEGORIES_URL = API_BASE_URL + 'plus/categories'
BLOCKS_URL = API_BASE_URL + 'endpoint/blocks/list_blocks'
BLOCK_URL = API_BASE_URL + 'endpoint/blocks/block_show_items'
SHOWS_URL = API_BASE_URL + 'endpoint/genres/shows_by_genre'
SHOW_URL = API_BASE_URL + 'plus/show'
EPISODE_URL = API_BASE_URL + 'nand/fullVideo'


PARAMS_LIVES = {
                    'user_id': '164',
                    'key': '06ca8574437919d902105c516f30d28f',
                    'device_id': 'F10379E579E54FE3ABB3D46B6AACF62D',
                    'json': 1,
                    'is_radio': 0
                }
PARAMS_LIVE_TV = {
                    'key': '06ca8574437919d902105c516f30d28f',
                    'user_id': '164',
                    'app_id': '17',
                    'need_playback': 'yes',
                    'need_geo': 'yes',
                    'need_live': 'yes'
                }
CATEGORIES_PARAMS = {
                        'key': '06ca8574437919d902105c516f30d28f',
                        'user_id': '164',
                        'app_id': '17'
                    }
BLOCKS_PARAMS = {
                    'key': '06ca8574437919d902105c516f30d28f',
                    'user_id': '164',
                    'p': '1',
                    'limit': '30',
                    'app_id': '17',
                    'need_labels': 'yes',
                    'need_top_10': 'yes',
                    'genre_id': '53'
                }
BLOCK_PARAMS = {
                    'key': '06ca8574437919d902105c516f30d28f',
                    'user_id': '164',
                    'need_labels': 'yes',
                    'p': '1',
                    'limit': '300'
                }
SHOWS_PARAMS = {
                    'user_id': '164',
                    'key': '06ca8574437919d902105c516f30d28f',
                    'p': '1',
                    'limit': '300',
                    'is_radio': '0',
                    'need_show_times': 'no',
                    'need_channel': 'yes',
                    'custom_order': 'yes',
                    'app_id': '17'
                }
SHOW_PARAMS = {
                'key': '06ca8574437919d902105c516f30d28f',
                'user_id': '164',
                'p': '1',
                'limit': '1000',
                'need_completion': 'yes',
                'channel_userid': '499344',
                'limit_also': '2',
                'need_trailer': 'yes',
                'app_id': '17',
                'need_like': 'yes',
                'cast': 'yes',
                'need_avg_rating': 'yes',
                'need_avg_videos_duration': 'yes',
                'need_production_year': 'yes'
            }
EPISODE_PARAMS = {
                    'key': '06ca8574437919d902105c516f30d28f',
                    'user_id': '164',
                    'channel_userid': '499344',
                    'app_id': '17',
                    'need_channel_details': 'yes'
                }
MAIN_MENU = [('\u0627\u0644\u0645\u0628\u0627\u0634\u0631', "", 1),
             ('\u0627\u0644\u0645\u0633\u0644\u0633\u0644\u0627\u062a', "53", 2),
             ('\u0643\u0644 \u0627\u0644\u0645\u062d\u062a\u0648\u064a\u0627\u062a', "", 6),
             ('\u0627\u0644\u0623\u0641\u0644\u0627\u0645', "56", 2)]
