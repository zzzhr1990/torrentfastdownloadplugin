#
# core.py
#
# Copyright (C) 2009 zzzhr <zzzhr@hotmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

import json
import time
import requests
import os
import base64
import traceback
from twisted.internet.task import LoopingCall
from deluge.error import InvalidTorrentError
from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export




DEFAULT_PREFS = {
    "test":"NiNiNi",
    'update_interval': 1,  # 2 seconds.
}

class Core(CorePluginBase):
    def __init__(self, plugin_name):
        self.config = {}
        self.processing = False
        log.info("%s plugin enabled...", plugin_name)

    def enable(self):
        log.info("Cluster download plugin enabled...")
        self.config = deluge.configmanager.ConfigManager("torrentfastdownloadplugin.conf", DEFAULT_PREFS)
        #self.config = {}
        self.update_stats()
        self.update_timer = LoopingCall(self.update_stats)
        self.update_timer.start(1)

    def disable(self):
        log.info("Cluster download plugin enabled...")
        try:
            self.update_timer.stop()
        except AssertionError:
            pass

    def process_torrents(self):
        downloading_list = component.get("Core").get_torrents_status({}, {})
        for key in downloading_list:
            torrent_info = downloading_list[key]
            torrent_key = key
            torrent_hash = torrent_info["hash"]
            dest_path = torrent_info["move_completed_path"]
            progress = torrent_info["progress"]
            state = torrent_info["state"]
 #           download_speed = torrent_info["download_payload_rate"]
            log.info("----------JSON-------------")
            log.info(json.dumps(downloading_list))
            log.info("----------====-------------")

    def update_stats(self):
        # Refresh torrents.
        if self.processing:
            return
        self.processing = True
        
        # Foreach processing status.
        
            # update path...

        # get torrent wait..
        try:
        # torrent http://qietv-play.wcs.8686c.com/torrent/debian-8.7.1-amd64-netinst.iso.torrent
            self.process_torrents()
            down_url = "http://qietv-play.wcs.8686c.com/json/list.json?ts=" + str(time.time())
            req = requests.get(down_url)
            if req.status_code == 200:
                res = req.json()
                if res["success"]:
                    torrents = res["data"]
                    for torrent in torrents:
                        torrent_file = requests.get(torrent["url"])
                        if torrent_file.status_code == 200:
                            fname = os.path.basename(torrent["url"])
                            b64 = base64.encodestring(torrent_file.content)
                            try:
                                add_torrent_id = component.get("Core").add_torrent_file(fname, b64, {})
                                if add_torrent_id is not None:
                                    log.info("%s add to server success!, torrent id : %s.", fname, add_torrent_id)
                            except InvalidTorrentError:
                                log.warn("%s add to server failed!, InvalidTorrentError occored.", fname)
 #                           if add_torrent_id is None:
                                
        except Exception as error:
            log.warn("error occored, %s , traceback \r\n %s" , error.message,traceback.format_exc())
        finally:
            self.processing = False

    def update(self):
        pass

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        pass
 #       for key in config.keys():
 #           self.config[key] = config[key]
 #       self.config.save()



    @export
    def get_config(self):
        """Returns the config dictionary"""
        return {}
 #       return self.config.config
