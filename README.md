# PasteBin

An simple PasteBin uses pygments to generate html and Flask as background.

Demo https://paste.cczu.org

## Run

### With Docker

```sh
sudo docker run --name pastebin -p 80:80 weicheng97/pastebin
```

### Directly

Do not try to just use app.run. Flask has serious problem on performance.

```sh
gunicorn -w 4 -b 0.0.0.0:80 PasteBinWeb:app
```

## Useage

Just open it and enjoy pasting.

### View all files

visit http://yourdomain/all to find all files ordered by newest pasted time.

### Use post method to paste

Post to root URL and server receive two parameters [syntax,content], quite easy.

### Clean

**DO NOT USE IT ON PRODUCTION ENVIRONMENT**

visit http://yourdomain/clean to clean all files.
