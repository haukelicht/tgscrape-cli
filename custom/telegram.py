import os
import re
import json

from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError


class TelegramAPI:

    def __init__(self, api_id, api_hash, session_file=None):
        # try:
        #     this_phone = PhoneNumber(phone)
        # except ValueError as e:
        #     raise e
        # except Exception as e:
        #     raise e

        # # this_phone = this_phone.sanitize()
        # self.phone = phone

        if isinstance(api_id, int):
            self.api_id = api_id
        elif api_id == '':
            raise ValueError('No value passed to option --api-id (required if --session-file is not used)')
        elif re.search(r'[^[0-9a-z]]', api_id):
            raise ValueError('Value passed to option --api-id cannot contain spaces!')
        else:
            self.api_id = int(api_id)

        if api_hash == '':
            raise ValueError('No value passed to option --api-hash (required if --session-file is not used)')
        elif re.search(r'[^[0-9a-z]]', api_hash):
            raise ValueError('Value passed to option --api-hash cannot contain spaces!')
        else:
            self.api_hash = api_hash

        self.session_file = session_file

    def dump_proj(self, path):
        proj_data = {"api_id": self.api_id, "api_hash": self.api_hash}
        with open(os.path.join(path, '.tgscrape.proj'), 'w') as file:
            json.dump(proj_data, fp=file)
            file.close()

    def authenticate(self, path=None):

        if self.session_file is None:
            if path is None:
                raise ValueError("Argument 'path' cannot be None")

            session_file = os.path.join(path, 'tgscrape.session')

        err_msg = 'Cannot authenticate with Telegram API: '

        try:
            client = TelegramClient(self.session_file, self.api_id, self.api_hash).start()
        except PhoneNumberInvalidError as e:
            raise ValueError(err_msg + 'invalid phone number!')
        except RuntimeError as e:
            raise ValueError(err_msg + 'invalid code provided!')
        except Exception as e:
            raise Exception(err_msg + '%s!' % type(e))

    def connect(self):

        err_msg = 'Cannot connect to Telegram API'
        try:
            self.client = TelegramClient(self.session_file, self.api_id, self.api_hash).start()
        except:
            raise RuntimeError('Cannot start Telegram Client!')
        else:
            self.is_connected = False
            with self.client as client:
                try:
                    client.connect()
                    is_connected = client.is_connected()
                    self.is_connected = is_connected
                except Exception as e:
                    raise Exception(err_msg + ': %s!' % type(e))
            if not self.is_connected:
                raise ConectionError(err_msg)

    def disconnect(self):
        try:
            with self.client as client:
                client.disconnect()
        except Exception as e:
            raise RuntimeError('Cannot disconnect from Telegram API.')
        else:
            self.is_connected = False
