# tgscrape: A command line interface to collect data from Telegram via the Telegram API 

**Still Work in Progress!!!**

## Install 

```shell
git clone -- tgscrape https://github.com/haukelicht/tgscrape-cli.git
# navigate to your local 
cd tgscrape
pip install .
pip install -r requirements.txt
tgscrape --help
```

## Use

## Initialize a tgscrape project

In order to use `tgscrape`, you need a valid Telegram API ID and hash.
Follow these instructions: https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
 
Initialize a new project and first steps

```shell
mkdir new_project
cd new_project
tgscrape --verbose init . --api-id <int> --api-hash <str>
# enter phone number
# enter confirmation code that is send to your Telegram account
```
**Important**: authenticating with `tgscrape init` writes two files to your current working directory

- 'tgscrape.session' (a Telethon session file)
- '.tgscrape.proj' (a hiden file containing your API ID and hast)

Make sure to not share these files with any third-party
Most importantly, **add them to your .gitignore**!

```
echo "tgscrape.session" >> .gitignore
echo ".tgscrape.proj" >> .gitignore
```

### Try it out

```shell
tgscrape chats 'opencryptodiscussion' --out-path 'dump' --out-name '%s.json' 
```
This writes a formatted JSON file named 'opencryptodiscussion.json' to your current working directory

### Get help

```shell
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


## Credit

- developed using [`click`](https://palletsprojects.com/p/click/)
- not inspired by [`tgscrape`](https://github.com/logr4y/tgscrape), same name though (found out only later ¯\_(ツ)_/¯)