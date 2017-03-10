#!/bin/bash
cd /root/plugin/torrentfastdownloadplugin
mkdir temp
export PYTHONPATH=./temp
/usr/bin/python setup.py build develop --install-dir ./temp
cp ./temp/TorrentFastDownloadPlugin.egg-link /root/.config/deluge/plugins
rm -fr ./temp
