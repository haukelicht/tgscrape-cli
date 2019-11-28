import click
import os
import json

from custom.telegram import TelegramAPI


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
              type=click.Path(),
              help='Set path of working directory.'
              )
@pass_context
def cli(context, verbose, set_pwd):
    context.verbose = verbose
    if set_pwd is None:
        set_pwd = os.getcwd()
    context.set_pwd = set_pwd


@cli.command()
@click.argument('path',
                type=click.Path(exists=True),
                required=False,
                default='.'
                )
@click.option('--init-location',
              type=click.Path(exists=True),
              required=False,
              default='.',
              help='Path where to write tgscrape.session and .tgscrape.proj files.'
              )
@click.option('--api-id',
              type=str,
              required=False,
              default='',
              help='Your telegram API key.'
              )
@click.option('--api-hash',
              type=str,
              required=False,
              default='',
              help='Your telegram API secret.'
              )
@click.option('--phone',
              type=str,
              required=False,
              default='',
              help='Your telegram phone number (needs to start with a country code, e.g. +41).'
              )
@click.option('--session-file',
              type=str,
              required=False,
              default='tgscrape.session',
              help='Path of an existing telethon .session file.'
              )
@pass_context
def init(context, path, init_location, api_id, api_hash, phone, session_file):
    """Initialize a new tgscrape project.

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
                file.close
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
            api_conn.dump(path=init_location)

    # authenticate if session file not provided
    if not os.path.isfile(session_file):
        try:
            api_conn.authenticate(path=init_location)
        except Exception as e:
            raise click.ClickException(e)

    try:
        api_conn.connect()
        click.echo(f'Session information stored in {api_conn.session_file} seems to be invalid.\nRe-authentication required:')
    except:
        try:
            api_conn.authenticate(session_file=session_file)
        except Exception as e:
            raise click.ClickException(e)

    if context.verbose:
        click.echo(f'Successfully initialized tgscrape project on path {path}')
        click.echo(f'Session information written to {session_file}')
        click.echo(f'Project data written to {proj_file}')
