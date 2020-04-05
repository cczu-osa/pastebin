# Data Exchange

## Raw API

Suppose the PasteBin url is http://pastepath . To add a new paste, POST raw code to http://pastepath/raw , and you can get a response with a token of the new paste on the payload.

You can always obtain raw code of any paste by GET http://pastepath/raw/{token} , 404 status code will returned if not found.

## JSON API

### Add a new paste

POST with data matches the json shown below:

```json
{
    "poster": "who",
    "language": "lang",
    "content": "hello",
    "expire": 2592000,
    "secret": false
}
```

"expire" represent seconds before expiration.

Server will return a simple json contains a token of the new paste:

```json
{
    "token": "ZKmYQ5YP"
}
```

Valid language values are defined in the `static/languages.json` file. Server doesn't check the language value you provided.

### Get pastes already existing

GET http://pastepath/paste/{token} , and the corresponding will be similar to the following format:

```json
{
    "token": "xxxxxxxx",
    "poster": "who",
    "language": "lang",
    "content": "main(){printf(\"helloworld\");}",
    "paste_time": 1586106844.249158,
    "expire_time": 1586711644.249158
}
```

"paste_time" and "expire_time" are unix timestamps. Float numbers bring higher precision than one second.

If paste not found, server will return a 404 status code and some error messages.

## Pagination

Only JSON API available. GET a page from http://pastepath/page/{num} will obtain response with pagination data:

```json
{
    "pagination": {
        "sum": 2,
        "current": 1
    },
    "items": [
        {
            "token": "xxxxxx",
            "poster": "who",
            "language": "lang",
            "content": "hello",
            "paste_time": 1586111003.301263,
            "expire_time": 1588703003.301263
        },
        ...
    ]
}
```

`.pagination.sum` defines total page number and `.pagination.current` is current page. `.items` contains all paste data in this page.
