# PasteBin
An simple PasteBin Based on Python Flask

Use pygments to generate html code and use Flask as background.
run PasteBinWeb.py to run

Use https://paste.ubuntu.com/ as sample.

Demo http://paste.cczu.org

## Run in Docker
```bash
sudo docker run --name pastebin -p 80:80 weicheng97/pastebin
```

## Run in bash
Do not try to just use app.run. Flask has serious problem on performance.
```bash
gunicorn -w 4 -b 0.0.0.0:80 PasteBinWeb:app
```

## Useage
Just open it and enjoy pasting.
### View all files
visit http://yourdomain/all to find all files ordered by newest pasted time.
### Use post method to paste
Post to root URL and server receive two parameters [syntax,content], quite easy.
'''
language = request.form['syntax']
content = request.form['content']
'''
### Clean
*DO NOT USE IT ON DEMO SERVER*
visit http://yourdomain/clean to clean all files.
