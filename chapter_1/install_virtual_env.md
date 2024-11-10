# virtualenv

By default it's installed as part of pyenv. Create venv stack


## Creating

```
virtualenv ~/example
```


## Using

To activate 

```
source ~/example/bin/activate
```


# Virtual env wrapper

Better and cleaner

## Installation

```
pip install virtualenvwrapper
echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python' >> ~/.bashrc
echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc
echo 'export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv' >> ~/.bashrc 
source /usr/local/bin/virtualenvwrapper.sh
```
