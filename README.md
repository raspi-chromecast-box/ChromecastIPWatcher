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

## Find the UUID of what will be the 'output' Chromecast

### aka just watch the logs , hopefully will get something later in the config to do this automatically based on friendly name
```
sudo docker logs -f alpine-chromecast-ip-watcher
```

## Then save it into Redis as "CONFIG.CHROMECAST_OUTPUT.UUID"

```
redis-cli -n 1 set "CONFIG.CHROMECAST_OUTPUT.UUID" "0f85e8b7-eeaf-b4ae-f809-85f7ad5c921c"
```