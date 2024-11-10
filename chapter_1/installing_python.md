# installation

Get pyenv installed

Check out Pyenv where you want it installed. A good place to choose is $HOME/.pyenv (but you can install it somewhere else):

```sh
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

Optionally, try to compile a dynamic Bash extension to speed up Pyenv. Don't worry if it fails; Pyenv will still work normally:

```sh
$ cd ~/.pyenv && src/configure && make -C src
```

Adding required env settings to global `bashrc` file

```sh
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

# add new python versions

### Python 3.10

```sh
$ pyenv install 3.10.4
```

### Python 3.7

```sh
$ pyenv install 3.7.4
```

### Verify

Verify installed Python versions

```sh
$ pyenv versions
````

output

```sh
$ pyenv versions
*system(set by /home/darkman66/•pyenv/version)
3.7.4
3.10.4
$
```
