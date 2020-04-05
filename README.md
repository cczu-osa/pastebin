# PasteBin

Language: [CN](doc/README_cn.md)

An simple PasteBin Application with Python Flask backend and pretty frontend.

Demo https://icpc.cczu.edu.cn/paste

![preview](doc/preview.png)

## Features

### Automatic code format recognition

If you leave language selection empty, it will try to recognize code syntax automatically.

### View all files

Visit http://pastebinpath/all to find all files ordered by newest pasted time.

### Easy data transmission ui

You can post raw code to http://pastebinpath/raw directly to add a new paste, or post a structured json data to http://pastebinpath/paste to get more detailed control. see [DataExchange.md](doc/DataExchange.md) for more information.

## Run

### With Docker

```sh
sudo docker run --restart=always --name pastebin -p 127.0.0.1:80:80 -v /var/pastebin:/pastebin/data weicheng97/pastebin:3.0
```

### Directly

```sh
./run.sh
```

### Debugging

```sh
./run.py
```

### Reverse proxy

If you want to use another URL, like https://example.com/paste, you need to create a text file `settings.json` in the data folder, and type content as follow:

```
{
    "baseurl": "https://example.com/paste"
}
```
