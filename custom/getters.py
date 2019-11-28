from datetime import datetime, timedelta, timezone
from telethon import functions, types
from telethon.client.telegramclient import TelegramClient
from custom.classes import ChatData


async def get_chat_data(client: TelegramClient, chat: str, until=None, lim=0, info=True, messages=True, participants=True) -> ChatData:

    """Request telegram chat info, chat history and participants
    :param client: object of class telethon.client.telegramclient.TelegramClient
    :param chat: (str)
    :param until: object of class datetime.datetime
    :param lim: integer
    :param tsfmt: string specifying the time stamp format
    :return: an instance of tgscrape.classes.ChannelData
    :rtype: tgscrape.classes.ChannelData
    """

    if until is None:
        until = datetime.today().date() + timedelta(days=1)
        until = datetime.combine(until, datetime.min.time(), timezone.utc)

    out = dict()

    if info:
        try:
            out['info'] = await client(functions.channels.GetFullChannelRequest(chat))
        except Exception as e:
            raise e
        id = out['info'].full_chat.id
    else:
        out['info'] = None
        id = 0

    if messages:
        try:
            out['messages'] = await client(functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=until,
                add_offset=0,
                limit=lim,
                min_id=0,
                max_id=0,
                hash=0
            ))
        except Exception as e:
            raise e
    else:
        out['messages'] = None

    if participants:
        try:
            out['participants'] = await client(functions.channels.GetParticipantsRequest(
                channel=chat,
                filter=types.ChannelParticipantsRecent(),
                offset=0,
                limit=lim,
                hash=0
            ))
        except Exception as e:
            raise e
    else:
        out['participants'] = None

    return ChatData(id=id, username=chat, chat_info=out['info'], chat_messages=out['messages'], chat_participants=out['participants'])
