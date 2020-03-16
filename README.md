# PasteBin

Language: [CN](README_cn.md)

An simple PasteBin uses pygments to generate html and Flask as background.

Demo https://icpc.cczu.edu.cn/paste

## Run

### With Docker

```sh
sudo docker run --restart=always --name pastebin -p 127.0.0.1:80:80 -v /var/pastebin:/pastebin/data weicheng97/pastebin:2.0
```

### Directly

Do not try to just use app.run. Flask has serious problem on performance.

```sh
gunicorn -w 4 -b 0.0.0.0:80 PasteBinWeb:app
```

### Reverse proxy

If you want to use another URL, e.g. https://example.com/paste, you need to create a text file `settings.json` in the data folder, and type content as follow:

```
{
    "baseurl": "https://example.com/paste"
}
```

## Useage

Just open it and enjoy pasting.

### View all files

visit http://pastebinpath/all to find all files ordered by newest pasted time.

### Use post method to paste

Post to root URL and server receive two parameters [syntax,content], quite easy.
