import json

import requests

from mi import Instance
from mi.utils import set_auth_i, upper_to_lower


class UserProfile(object):
    def __init__(self,
                 id_: str = None,
                 name: str = None,
                 username: str = None,
                 host: str = None,
                 avatar_url: str = None,
                 avatar_blurhash: str = None,
                 avatar_color: str = None,
                 is_admin: bool = False,
                 is_moderator: bool = False,
                 is_bot: bool = False,
                 is_cat: bool = False,
                 is_lady: bool = False,
                 is_verified: bool = False,
                 is_premium: bool = False,
                 emojis: list = None,
                 online_status: str = None,
                 url: str = None,
                 uri: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 banner_url: str = None,
                 banner_blurhash: str = None,
                 banner_color: str = None,
                 is_locked: bool = False,
                 is_silenced: bool = False,
                 is_suspended: bool = False,
                 description: str = None,
                 location: str = None,
                 birthday: str = None,
                 lang: str = None,
                 fields: list = None,
                 followers_count: int = 0,
                 following_count: int = 0,
                 notes_count: int = 0,
                 pinned_note_ids: list = None,
                 pinned_notes: list = None,
                 pinned_page_id: list = None,
                 pinned_page: list = None,
                 two_factor_enabled: bool = False,
                 use_password_less_login: bool = False,
                 security_keys: bool = False,
                 twitter: str = None,
                 github: str = None,
                 discord: str = None,
                 avatar_id: str = None,
                 banner_id: str = None,
                 auto_watch: bool = False,
                 inject_featured_note: bool = False,
                 receive_announcement_email: bool = False,
                 always_mark_nsfw: bool = False,
                 careful_bot: bool = False,
                 careful_massive: bool = False,
                 auto_accept_followed: bool = False,
                 no_crawle: bool = False,
                 is_explorable: bool = False,
                 is_deleted: bool = False,
                 hide_online_status: bool = False,
                 has_unread_specified_notes: bool = False,
                 has_unread_mentions: bool = False,
                 has_unread_announcement: bool = False,
                 has_unread_antenna: bool = False,
                 has_unread_channel: bool = False,
                 has_unread_messaging_message: bool = False,
                 has_unread_notification: bool = False,
                 has_pending_received_follow_request: bool = False,
                 pending_received_follow_requests_count: bool = False,
                 client_data: dict = None,
                 integrations: dict = None,
                 muted_words: list = None,
                 muting_notification_types: list = None,
                 email_notification_types: list = None,
                 email: str = None,
                 email_verified: bool = False,
                 security_keys_list: list = None
                 ):
        self.id_ = id_
        self.name = name
        self.username = username
        self.host = host
        self.avatar_url = avatar_url
        self.avatar_blurhash = avatar_blurhash
        self.avatar_color = avatar_color
        self.is_admin = is_admin
        self.is_moderator = is_moderator
        self.is_bot = is_bot
        self.is_cat = is_cat
        self.is_lady = is_lady
        self.is_verified = is_verified
        self.is_premium = is_premium
        self.emojis = emojis
        self.online_status = online_status
        self.url = url
        self.uri = uri
        self.created_at = created_at
        self.updated_at = updated_at
        self.banner_url = banner_url
        self.banner_blurhash = banner_blurhash
        self.banner_color = banner_color
        self.is_locked = is_locked
        self.is_silenced = is_silenced
        self.is_suspended = is_suspended
        self.description = description
        self.location = location
        self.birthday = birthday
        self.lang = lang
        self.fields = fields
        self.followers_count = followers_count
        self.following_count = following_count
        self.notes_count = notes_count
        self.pinned_note_ids = pinned_note_ids
        self.pinned_notes = pinned_notes
        self.pinned_page_id = pinned_page_id
        self.pinned_page = pinned_page
        self.two_factor_enabled = two_factor_enabled
        self.use_password_less_login = use_password_less_login
        self.security_keys = security_keys
        self.twitter = twitter
        self.github = github
        self.discord = discord
        self.avatar_id = avatar_id
        self.banner_id = banner_id
        self.auto_watch = auto_watch
        self.inject_featured_note = inject_featured_note
        self.receive_announcement_email = receive_announcement_email
        self.always_mark_nsfw = always_mark_nsfw
        self.careful_bot = careful_bot
        self.careful_massive = careful_massive
        self.auto_accept_followed = auto_accept_followed
        self.no_crawle = no_crawle
        self.is_explorable = is_explorable
        self.is_deleted = is_deleted
        self.hide_online_status = hide_online_status
        self.has_unread_specified_notes = has_unread_specified_notes
        self.has_unread_mentions = has_unread_mentions
        self.has_unread_announcement = has_unread_announcement
        self.has_unread_antenna = has_unread_antenna
        self.has_unread_channel = has_unread_channel
        self.has_unread_messaging_message = has_unread_messaging_message
        self.has_unread_notification = has_unread_notification
        self.has_pending_received_follow_request = has_pending_received_follow_request
        self.pending_received_follow_requests_count = pending_received_follow_requests_count
        self.client_data = client_data
        self.integrations = integrations
        self.muted_words = muted_words
        self.muting_notification_types = muting_notification_types
        self.email_notification_types = email_notification_types
        self.email = email
        self.email_verified = email_verified
        self.security_keys_list = security_keys_list


class User(object):
    __slots__ = (
        'id',
        'name',
        'username',
        'host',
        'avatar_url',
        'avatar_blurhash',
        'avatar_color',
        'instance',
        'emojis',
        'is_admin',
        'is_bot',
        'auth_i',
        'token',
        'origin_uri',
        'online_status',
        'is_bot',
        'is_lady',
        'is_cat',
        'is_moderator',
        'is_verified',
        'url',
        'uri',
    )

    def __init__(self,
                 id_: str = None,
                 name: str = None,
                 username: str = None,
                 host: str = None,
                 avatar_url: str = None,
                 avatar_blurhash: str = None,
                 avatar_color: str = None,
                 instance: dict = None,
                 emojis=None,
                 is_admin=False,
                 is_moderator: bool = False,
                 is_bot: bool = False,
                 is_cat: bool = False,
                 is_lady: bool = False,
                 is_verified: bool = False,
                 online_status: str = None,
                 url: str = None,
                 uri: str = None,
                 auth_i: dict = None,
                 ):
        self.id = id_
        self.name = name
        self.username = username
        self.host = host
        self.avatar_url = avatar_url
        self.avatar_blurhash = avatar_blurhash
        self.avatar_color = avatar_color
        self.instance = Instance(**upper_to_lower(instance))
        self.emojis = emojis
        self.is_admin = is_admin
        self.auth_i = auth_i
        self.token = None
        self.origin_uri: None
        self.online_status = None
        self.is_bot = is_bot
        self.is_lady = is_lady
        self.is_cat = is_cat
        self.is_moderator = is_moderator
        self.is_verified = is_verified
        self.online_status = online_status
        self.url = url
        self.uri = uri

    @classmethod
    def from_dict(cls, data: dict):
        self = cls.__new__(cls)
        self.id = data.get('id')
        self.name = data.get('name', data.get('username', None))
        self.username = data.get('username')
        self.host = data.get('host')
        self.avatar_url = data.get('avatarUrl')
        self.avatar_blurhash = data.get('avatarBlurhash')
        self.avatar_color = data.get('avatarColor')
        self.instance = Instance(**upper_to_lower(data))
        self.emojis = data.get('emojis')
        self.is_admin = data.get('is_admin')

    def get_i(self):
        set_auth_i(self, self.auth_i, True)
        data = json.dumps({'i': self.token})
        res = requests.post(self.origin_uri + '/api/i', data=data)
        user = UserProfile(**upper_to_lower(json.loads(res.text)))
        return user
