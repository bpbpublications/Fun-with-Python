# run

## server 1

```
python server_1.py
```


# server 2

```
python server_2.py
```

* improved

```
python server_2.1.py
```


simple use

* with no path and params

```
 ~/ curl "http://localhost:8083/"
main view
```

* with path only

```
 ~/ curl "http://localhost:8083/hello"
hello to you too
```

* with path and params

```
 ~/ curl "http://localhost:8083/hello?a=4&b=3"
Total sum: 7
```

* uknown path

```
 ~/ curl "http://localhost:8083/sd"
Sorry do not know you /sd
```

## improve code

