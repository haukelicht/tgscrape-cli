import click
import os
import re
import json
from datetime import datetime

from custom.telegram import TelegramAPI
from custom.readers import read_entities
from custom.getters import get_chat_data


class Context(object):
    """CLI context

    The CLI context sets attributes that are available to all subcommands
    It is passed to subcommands of a command group by calling @pass_context, 
    which is defined by calling
     `pass_context = click.make_pass_decorator(Context, ensure=True)`,
    and by making `context` the first parameter of all subcommand functions 

    The command group is define using the decorator @click.group()
    Subcommands are defined using the decorator @cli.command() 
    """

    def __init__(self):
        self.verbose = False


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group()
@click.option('--verbose',
              is_flag=True,
              help='Print log messages to std out.'
              )
@click.option('--set-pwd',
              type=str,
              help='Set path of working directory.'
              default='.'
              )
@pass_context
def cli(context, verbose, set_pwd):
    context.verbose = verbose
    if set_pwd is '.':
        set_pwd = os.getcwd()
    context.set_pwd = os.path.expanduser(set_pwd)


@cli.command()
@click.argument('path',
                type=str,
                required=False,
                default='.'
                )
@click.option('--init-location',
              type=click.Path(exists=True),
              required=False,
              default='.',
              help='Path where to write tgscrape.session and .tgscrape.proj files. Default is current working directory'
              )
@click.option('--api-id',
              type=int,
              required=False,
              default=0,
              help='Your telegram API ID.'
              )
@click.option('--api-hash',
              type=str,
              required=False,
              default='',
              help='Your telegram API hash.'
              )
@click.option('--session-file',
              type=str,
              required=False,
              default='tgscrape.session',
              help='Path of an existing Telethon session file.'
              )
@pass_context
def init(context, path, init_location, api_id, api_hash, session_file):
    """
    Initialize a tgscrape project.

    Calling `tgscrape init` verifies the user's Telegram API credentials.
    If these credentials are valid, a 'tgscrape.session' file (a Telethon .session file, see https://docs.telethon.dev/en/latest/concepts/sessions.html)
    is written to the path set by option --init-location.
    Thereby, future calls of `tgscrape` can use the valid session file to connect to the Telegram API.


    There are two alternative ways to init tgscrape:

        1. Credentials can be passed to options --api-id and --api-hash, respectively, 
        so that only a phone number and confirmation code need to be passed interactively.

        2. An existing and valid Telethon .session file can be passed by passing its path to option --session-file.


    When called without any options, `tgscrape init` first checks whether a '.tgscrape.proj' file exists in the current working directory.
    If that's not the case, the program exits.
    Otherwise, next it checks whether a 'tgscrape.session' exists in the current working directory.
    If that's the case, the program tries to use it to connect to the Telegram API.
    If that attempt fails, the program exits with an error and exit status 0.
    Otherwise it exits with status 1.

    If no 'tgscrape.session' file exists in the current working directory,
    the user is prompted for their phone number and the confirmation code that is send to their Telegram account.


    Arguments:

      PATH  The path of the tgscrape project to initialize. Defaults to the current working directory (i.e., ./)
    """

    if not os.path.isdir(path):
        raise click.ClickException("Argument PATH passed to `tgscrape init` needs to be an existing path on your file system!")

    if path == '.':
        path = context.set_pwd

    proj_file = os.path.join(init_location, '.tgscrape.proj')
    msg = f' .tgscrape.proj file found on path --init-location {init_location}'
    if os.path.isfile(proj_file):
        try:
            with open(proj_file, 'r') as file:
                proj = json.load(file)
                file.close()
        except:
            raise click.ClickException('Cannot load' + msg)
        else:
            api_conn = TelegramAPI(api_id=proj['api_id'], api_hash=proj['api_hash'])
    else:
        click.echo('No' + msg)
        click.echo('Trying to create one using values passed to --api-id and --api-hash')
        try:
            api_conn = TelegramAPI(api_id=api_id, api_hash=api_hash)
        except ValueError as e:
            raise click.ClickException(e)
        except Exception as e:
            click.echo('Unknown error occurred when trying to set API credentials:')
            raise click.ClickException(e)
        else:
            api_conn.dump_proj(path=init_location)

    click.echo(api_conn.session_file)

    # authenticate if session file not provided
    if not os.path.isfile(session_file):
        try:
            api_conn.authenticate(path=init_location)
        except Exception as e:
            raise click.ClickException(e)

    if hasattr(api_conn, 'client'):
        click.echo(typeof(api_conn.client))
    else:
        click.echo('no client')

    try:
        api_conn.connect()
    except RuntimeError as e:
        try:
            api_conn.authenticate(session_file=session_file)
        except Exception as e:
            raise click.ClickException(e)
        else:
            try:
                api_conn.connect()
            except RuntimeError as e:
                raise click.ClickException(e)
    except Exception as e:
        raise click.ClickException(e)

    if hasattr(api_conn, 'is_connected'):
        click.echo(api_conn.is_connected)

    try:
        api_conn.disconnect()
    except RuntimeError as e:
        raise click.ClickException(e)
    except Exception as e:
        raise click.ClickException('Unknown error raised when trying to disconnect client: ' + type(e))

    if context.verbose:
        click.echo(f'Successfully initialized tgscrape project on path {init_location}')
        click.echo(f'Session information written to {api_conn.session_file}')
        click.echo(f'Project data written to {proj_file}')


@cli.command()
@click.argument('entities',
                type=str,
                required=True
                )
@click.option('--out-path',
              type=str,
              required=False,
              default='.',
              help='Path where to write chat data. Default is current working directory.'
              )
@click.option('--out-name',
              type=str,
              required=False,
              default='',
              help="Name stem of file with chat data (chat name will be prefixed). Default is '<chat>_<%Y-%m-%dT%H%M%S>.json'"
              )
@click.option('--no-info', is_flag=True, help="Do not get chat channel information data.", default=True)
@click.option('--no-messages', is_flag=True, help="Do not get chat messages data.", default=True)
@click.option('--no-participants', is_flag=True, help="Do not get chat participants data.", default=True)
@click.option('--check-track',
              is_flag=True,
              help="Check whether to track a chat (chat-level boolean flag in YAML/JSON dictionary with key 'track')."
              )
@click.option('--indent',
              type=int,
              required=False,
              default=4,
              help='Indentation level of output JSON. Default is 4'
              )
@pass_context
def chats(
    context,
    entities,
    out_path,
    out_name,
    no_info,
    no_messages,
    no_participants,
    check_track,
    indent
):
    """
    Scrape the info, chat history and participants data from (public) a list of chat groups.

    Calling `tgscrape chats ...` scrapes data from specified chat groups the user has access to.
    (This includes all public Telegram chat groups.)

    There are currently three alternative ways implemented to pass chat group names to the ENTITIES argument:

        1. a comma-separated list of chat group names (e.g. `chat1,chat2,chat3`)

        2. a YAML file that maps chat group names as values 
        to individual "chat" keys at the top-level of the YAML file
        (e.g., `chat: "<chat group name>"`)

        3. a JSON file that maps chat group names as values 
        to individual "chat" keys at the top-level of the YAML file
        (e.g., `[{"chat": "<chat1>", ...}, {"chat": "<chat2>", ...}, ...]`)

    By default (i.e. when called without any options set), 

        `tgscrape chats ENTITIES`

    returns the complete chat info, message history and participants data 
    for each chat passed to argument ENTITIES
    as a formatted JSON string to std out.
    (It thus can be piped to a file `... > file.json`)

    If provided with a file name stem (--out-name) and a directory path (--out-path, default is current working directory),
    the formatted JSON will be written to file.

    Arguments:    

        ENTITIES  Names of the chat groups to scrape.

    """
    if out_path is not '.':
        if not os.path.isdir(out_path):
            os.mkdir(out_path)

    try:
        chats = read_entities(entities, 'chat', check_track)
    except Exception as e:
        raise click.ClickException(e)

    proj_file = os.path.join('.', '.tgscrape.proj')
    err_msg = f' %s file found on path ./'
    if not os.path.isfile(proj_file):
        raise click.ClickException('No' + err_msg % '.tgscrape.proj')

    try:
        with open(proj_file, 'r') as file:
            proj = json.load(file)
            file.close()
    except:
        raise click.ClickException('Cannot load' + err_msg % '.tgscrape.proj')

    session_file = os.path.join('.', 'tgscrape.session')
    if not os.path.isfile(session_file):
        raise click.ClickException('No' + err_msg % 'tgscrape.session')

    api_conn = TelegramAPI(
        api_id=proj['api_id'],
        api_hash=proj['api_hash'],
        session_file=session_file
    )

    try:
        api_conn.connect()
    except Exception as e:
        raise click.ClickException(e)

    out = dict()
    with api_conn.client as client:
        for chat in chats:
            try:
                if context.verbose:
                    click.echo('Trying to get data for chat ' + chat)
                data = client.loop.run_until_complete(
                    get_chat_data(
                        client,
                        chat,
                        info=no_info,
                        messages=no_messages,
                        participants=no_participants
                    )
                )
            except Exception as e:
                click.echo('Could not get data for chat ' + chat + ': ' + repr(e))
            else:
                if out_name is '':
                    data_str = data.to_json(indent=indent)
                    ind = ' ' * indent
                    re.sub(r'\n', '\n' + ind, data_str)
                    click.echo('{\n' + ind + f'"chat": "{chat}",' + '\n' + ind + f'"chat_data": {data_str}' + '\n}')
                else:
                    try:
                        if re.search(r'%s', out_name):
                            file = out_name % chat
                        else:
                            file = out_name
                    except:
                        file = f'{chat}_{datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.json'

                    fp = os.path.join(out_path, file)
                    try:
                        with open(fp, 'w', encoding='utf-8') as dest:
                            data.to_json(dest, indent=indent)
                    except:
                        out[chat] = data.to_json()

        client.disconnect()
