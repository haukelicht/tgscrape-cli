from datetime import datetime, timedelta, timezone
from telethon import functions, types
from telethon.client.telegramclient import TelegramClient
from custom.classes import ChatData


async def get_chat_data(client: TelegramClient, chat: str, until=None, lim=1000000000) -> ChatData:

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

    try:
        out['info'] = await client(functions.channels.GetFullChannelRequest(chat))
    except Exception as e:
        raise ValueError(e)

    id = out['info'].full_chat.id

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

    out['participants'] = await client(functions.channels.GetParticipantsRequest(
        channel=chat,
        filter=types.ChannelParticipantsRecent(),
        offset=0,
        limit=lim,
        hash=0
    ))

    return ChatData(id=id, username=chat, chat_info=out['info'], chat_messages=out['messages'], chat_participants=out['participants'])
