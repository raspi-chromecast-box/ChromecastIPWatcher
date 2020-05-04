#!/bin/bash
sudo docker run -it \
--name 'alpine-chromecast-ip-watcher' \
--network host \
alpine-chromecast-ip-watcher