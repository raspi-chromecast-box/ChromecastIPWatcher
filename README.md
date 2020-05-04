# Chromecast IP Watcher

## Docker Build Command

```
sudo docker build -t alpine-chromecast-ip-watcher .
```

## Docker Run Command
```
sudo docker run -dit --restart='always' \
--name 'alpine-chromecast-ip-watcher' \
--network host \
alpine-chromecast-ip-watcher
```