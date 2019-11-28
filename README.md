# tgscrape: A command line interface to collect data from Telegram via the Telegram API 

**Still Work in Progress!!!**


## Use

Initialize a new project and first steps
```
mkdir new_project
cd new_project
tgscrape --verbose init . --api-id <int> --api-hash <str>
# enter phone number
# enter confirmation code that is send to your Telegram account
tgscrape chats 'opencryptodiscussion' --out-path 'dump' --out-name '%s.json' 
```

Get help:
```
# view help
tgscrape --help
# view help for init subcommand
tgscrape init --help
# view help for chats subcommand
tgscrape chats --help
```

## Developing

Requirements:

- Python 3 and `pip`
- `virtualvenv`: `pip3 install virtualenv`


Use a virtual environment

```shell 
# create a virtual environment
virtualenv venv
# activate virtual environment
. venv/bin/activate
# install required packages
pip install -r requirements.txt
```

Develop locally

```shell
# initially and when modifying setup.py
pip install --editable .
# when installing third-party packages/modules with pip install <pkg>
pip freeze > requirements.txt
```


## Inspired by 

- [`tgscrape`](https://github.com/logr4y/tgscrape)