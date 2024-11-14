# install

```bash
$ pip install briefcase
```

# hello world

## init

```bash
$ briefcase new
```

follow by answering questions

```bash
Formal Name [Hello World]: <enter>

App Name [helloworld]: <enter>

Bundle Identifier [com.example]: <enter>

Project Name [Hello World]: <enter>

Description [My first application]: <enter>

Author [Jane Developer]: <enter>

Author's Email [jane@example.com]: <enter>

Application URL [https://example.com/helloworld]: <enter>

What license do you want to use for this project's code?

  1) BSD license
  2) MIT license
  3) Apache Software License
  4) GNU General Public License v2 (GPLv2)
  5) GNU General Public License v2 or later (GPLv2+)
  6) GNU General Public License v3 (GPLv3)
  7) GNU General Public License v3 or later (GPLv3+)
  8) Proprietary
  9) Other

Project License [1]: 1

What GUI toolkit do you want to use for this project?

  1) Toga
  2) PySide6       (does not support iOS/Android deployment)
  3) PursuedPyBear (does not support iOS/Android deployment)
  4) Pygame        (does not support iOS/Android deployment)
  5) None

GUI Framework [1]: 1 <enter>
```

## create app

```bash
$ briefcase create iOS
```

## build

```bash
$ briefcase build iOS
```

output

```bash
[helloworld] Updating app metadata...
Setting main module... done

[helloworld] Building Xcode project...
Building... done

[helloworld] Built build/helloworld/ios/xcode/build/Debug-iphonesimulator/Hello World.app
```

## run it

```bash
$ briefcase run iOS
```
