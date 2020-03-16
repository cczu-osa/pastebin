# PasteBin

代码剪切板

Demo https://icpc.cczu.edu.cn/paste

## 运行

### Docker

```sh
sudo docker run --restart=always --name pastebin -p 127.0.0.1:80:80 -v /var/pastebin:/pastebin/data weicheng97/pastebin:2.0
```

### 原生

不要直接运行，会有性能问题

```sh
gunicorn -w 4 -b 0.0.0.0:80 PasteBinWeb:app
```

### 反向代理

如果要用别的地址访问，例如 https://example.com/paste, 需要在 data 文件夹里新建一个 `settings.json` 文件, 并放入以下内容:

```
{
    "baseurl": "https://example.com/paste"
}
```

## 使用

### 所有文件

公开的片段可以在 http://pastebinpath/all 上看到。

### 用 post 新增一条记录

向根路径 post 两个参数 [syntax,content] 即可。
