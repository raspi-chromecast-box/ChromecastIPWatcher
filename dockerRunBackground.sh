#!/bin/bash
sudo docker run -dit --restart='always' \
--name 'alpine-chromecast-ip-watcher' \
--network host \
alpine-chromecast-ip-watcher