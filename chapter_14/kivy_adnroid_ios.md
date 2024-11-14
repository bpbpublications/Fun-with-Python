# Android

```bash
$ pip install buildozer
```

## init

```bash
$ buildozer init
```

## run

```bash
$ buildozer -v android debug
```

# iOS

(on MacOS)
```bash
$ brew install autoconf automake libtool pkg-config
$ brew link libtool
```

```bash
$ pip install Cython kivy-ios
```

## compile

```bash
$ toolchain build python3 kivy
```

```bash
$ toolchain pip install plyer
```

## create project


```bash
$ toolchain create MyApp .
```

## open project

```bash
$ open MyApp-ios/myapp.xcodeproj
```
