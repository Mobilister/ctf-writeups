## Solve 

Set up socat locally: 

```
socat TCP-LISTEN:1337,fork OPENSSL:ispy--kyle-7850.ctf.kitctf.de:443
```

Get the debug end-point from

```
localhost:1337/json -->

[ {
   "description": "",
   "devtoolsFrontendUrl": "/devtools/inspector.html?ws=localhost:1337/devtools/page/EF9C81924892F61908532AD6BFF31937",
   "id": "EF9C81924892F61908532AD6BFF31937",
   "title": "google.com",
   "type": "page",
   "url": "http://google.com/",
   "webSocketDebuggerUrl": "ws://localhost:1337/devtools/page/EF9C81924892F61908532AD6BFF31937"
} ]
```

Run node: 

node getflag.js


