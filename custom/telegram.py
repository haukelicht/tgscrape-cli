import os
import re
import json

from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError


class TelegramAPI:

    def __init__(self, api_id, api_hash):
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

    def dump(self, path):
        proj_data = {"api_id": self.api_id, "api_hash": self.api_hash}
        with open(os.path.join(path, '.tgscrape.proj'), 'w') as file:
            json.dump(proj_data, fp=file)
            file.close()

    def authenticate(self, path=None, session_file=None):

        if session_file is None:
            if path is None:
                raise ValueError("Argument 'path' cannot be None")

            self.session_path = os.path.join(path, 'tgscrape.session')
        else:
            self.session_path = session_file

        rm_session = False

        err_msg = 'Cannot authenticate with Telegram API: '

        try:
            client = TelegramClient(self.session_path, self.api_id, self.api_hash).start()
        except PhoneNumberInvalidError as e:
            rm_session = True
            raise ValueError(err_msg + 'invalid phone number!')
        except RuntimeError as e:
            rm_session = True
            raise ValueError(err_msg + 'invalid code provided!')
        except Exception as e:
            rm_session = True
            raise Exception(err_msg + '%s!' % type(e))
        finally:
            if rm_session:
                os.remove(self.session_path)

    def connect(self):

        err_msg = 'Cannot connect to Telegram API'
        try:
            client = TelegramClient(self.session_path, self.api_id, self.api_hash).start()
        except:
            raise RuntimeError('Cannot start Telegram Client!')
        else:
            with client:
                try:
                    client.connect()
                    is_connected = client.is_connected()
                except Exception as e:
                    raise Exception(err_msg + ': %s!' % type(e))
            if not is_connected:
                raise ConectionError(err_msg)

        try:
            client.disconnect()
        except Exception as e:
            raise RuntimeError('Cannot disconnect from Telegram API.')
