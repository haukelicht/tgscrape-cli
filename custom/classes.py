from telethon.tl.types import Channel
from telethon.tl.types import ChannelFull, PeerNotifySettings, ChatInviteEmpty, PhotoEmpty
from telethon.tl.types.messages import ChannelMessages, ChatFull
from telethon.tl.types.channels import ChannelParticipants
from datetime import datetime
import json
from telethon.tl.tlobject import _json_default


class ChatData(Channel):
    def __init__(self, id: int, username: str, chat_info: [ChatFull, type(None)], chat_messages: [ChannelMessages, type(None)], chat_participants: [ChannelParticipants, type(None)]):
        """
        :type id: int
        :type username: str
        :type chat_info: telethon.tl.types.messages.ChatFull
        :type chat_messages: telethon.tl.types.messages.ChannelMessages
        :type chat_participants: telethon.tl.types.channels.ChannelParticipants
        :type created_at: datetime.datetime
        """
        if not isinstance(id, int):
            raise ValueError('Value passed to constructor argument "id" needs to be an integer')

        self.id = id

        if not isinstance(username, str):
            raise ValueError('Value passed to constructor argument "username" needs to be a string')

        self.username = username

        if chat_info is None:
            self.chat_info = ChatFull(
                full_chat=ChannelFull(
                    id=id,
                    about='not valid',
                    pts=0,
                    read_inbox_max_id=0,
                    read_outbox_max_id=0,
                    unread_count=0,
                    chat_photo=PhotoEmpty(id=0),
                    bot_info=[],
                    notify_settings=PeerNotifySettings(),
                    exported_invite=ChatInviteEmpty()
                ),
                chats=[],
                users=[]
            )
        else:
            if not isinstance(chat_info, ChatFull):
                raise TypeError('Argument passed to constructor parameter "chat_info" must be None or an object of type <telethon.tl.types.ChatFull>')
            if not chat_info.to_dict()['full_chat']['id'] == id:
                raise ValueError('Argument passed to constructor parameter "id" and value .to_dict()[\'full_chat\'][\'id\'] of object passed to argument "chat_info" do not match')
            if not len(chat_info.to_dict()['chats']) == 1:
                raise AttributeError('List .to_dict()[\'full_chat\'][\'id\'] of object passed to argument "chat_info" contains more than one object')
            if not chat_info.to_dict()['chats'][0]['username'] == username:
                raise ValueError('Argument passed to constructor parameter "username" and value .to_dict()[\'chats\'][0][\'username\'] of object passed to argument "chat_info" do not match')
            self.chat_info = chat_info

        if chat_messages is None:
            self.chat_messages = ChannelMessages(pts=0, count=0, messages=[], chats=[], users=[])
        else:
            if not isinstance(chat_messages, ChannelMessages):
                raise TypeError('Argument passed to constructor parameter "channel_message" must be None or an object of type <telethon.tl.types.messages.ChannelMessages>')
            self.chat_messages = chat_messages

        if chat_participants is None:
            self.chat_participants = ChannelParticipants(count=0, participants=[], users=[])
        else:
            if not isinstance(chat_participants, ChannelParticipants):
                raise TypeError('Argument passed to constructor parameter "chat_participants" must be None or an object of type <telethon.tl.types.channels.ChannelParticipants>')
            self.chat_participants = chat_participants

        self.created_at = datetime.now()

    def to_dict(self):
        out = dict()
        out['_'] = 'ChatData'
        for attr in self.__dict__.keys():
            try:
                out[attr] = getattr(self, attr).to_dict()
            except:
                out[attr] = getattr(self, attr)
        return out

    def to_json(self, fp=None, default=_json_default, **kwargs):
        """
        Represent the current `ChannelData` as JSON.
        If ``fp`` is given, the JSON will be dumped to said
        file pointer, otherwise a JSON string will be returned.
        Note that bytes and datetimes cannot be represented
        in JSON, so if those are found, they will be base64
        encoded and ISO-formatted, respectively, by default.
        """
        d = self.to_dict()
        if fp:
            return json.dump(d, fp, default=default, **kwargs)
        else:
            return json.dumps(d, default=default, **kwargs)
