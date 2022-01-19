from __future__ import annotations

from typing import AsyncIterator, Dict, List, Optional, TYPE_CHECKING

from .emoji import Emoji
from .models import RawInstance
from .models.emoji import RawEmoji
from .types.instance import (Meta as InstanceMetaPayload)

if TYPE_CHECKING:
    from .user import User
    from . import ConnectionState, User


class InstanceMeta:
    def __init__(self, data: InstanceMetaPayload, state: ConnectionState):
        self.maintainer_name: str = data['maintainer_name']
        self.maintainer_email: str = data['maintainer_email']
        self.version: str = data['version']
        self.name: str = data['name']
        self.uri: str = data['uri']
        self.description: str = data['description']
        self.langs: List[str] = data['langs']
        self.tos_url: Optional[str] = data['tos_url']
        self.repository_url: str = data['repository_url']
        self.feedback_url: str = data['feedback_url']
        self.secure: bool = bool(data['secure'])
        self.disable_registration: bool = bool(data['disable_registration'])
        self.disable_local_timeline: bool = bool(data['disable_local_timeline'])
        self.disable_global_timeline: bool = bool(data['disable_global_timeline'])
        self.drive_capacity_per_local_user_mb: int = data['drive_capacity_per_local_user_mb']
        self.drive_capacity_per_remote_user_mb: int = data['drive_capacity_per_remote_user_mb']
        self.email_required_for_signup: bool = bool(data['email_required_for_signup'])
        self.enable_hcaptcha: bool = bool(data['enable_hcaptcha'])
        self.enable_recaptcha: bool = bool(data['enable_recaptcha'])
        self.recaptcha_site_key: str = data['recaptcha_site_key']
        self.sw_publickey: str = data['sw_publickey']
        self.mascot_image_url: str = data['mascot_image_url']
        self.error_image: str = data['error_image_url']
        self.max_note_text_length: int = data['max_note_text_length']
        self.emojis: List[Emoji] = [Emoji(RawEmoji(i), state=state) for i in data['emojis']]
        self.ads: list = data['ads']
        self.enable_email: bool = bool(data['enable_email'])
        self.enable_twitter_integration = bool(data['enable_twitter_integration'])
        self.enable_github_integration: bool = bool(data['enable_github_integration'])
        self.enable_discord_integration: bool = bool(data['enable_discord_integration'])
        self.enable_service_worker: bool = bool(data['enable_service_worker'])
        self.translator_available: bool = bool(data['translator_available'])
        self.pinned_page: Optional[List[str]] = data.get('pinned_page')
        self.cache_remote_files: Optional[bool] = data.get('cache_remote_files')
        self.proxy_remote_files: Optional[bool] = data.get('proxy_remote_files')
        self.require_setup: Optional[bool] = data.get('require_setup')
        self.features: Optional[Dict[str, bool]] = data.get('features')


class Instance:
    def __init__(self, raw_data: RawInstance, state: ConnectionState):
        """
        インスタンス情報
        
        Parameters
        ----------
        raw_data : RawInstance
            インスタンス情報の入った dict
        state: ConnectionState
            botのコネクション
        """

        self.__raw_data: RawInstance = raw_data
        self.__state: ConnectionState = state

    @property
    def host(self):
        return self.__raw_data.host

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def software_name(self):
        return self.__raw_data.software_name

    @property
    def software_version(self):
        return self.__raw_data.software_version

    @property
    def icon_url(self):
        return self.__raw_data.icon_url

    @property
    def favicon_url(self):
        return self.__raw_data.favicon_url

    @property
    def theme_color(self):
        return self.__raw_data.theme_color

    def get_users(self,
                  limit: int = 10,
                  *,
                  offset: int = 0,
                  sort: Optional[str] = None,
                  state: str = 'all',
                  origin: str = 'local',
                  username: Optional[str] = None,
                  hostname: Optional[str] = None,
                  get_all: bool = False
                  ) -> AsyncIterator[User]:
        """

        Parameters
        ----------
        limit: int
        offset:int
        sort:str
        state:str
        origin:str
        username:str
        hostname:str
        get_all:bool

        Returns
        -------
        AsyncIterator[User]
        """
        return self.__state.get_users(limit=limit, offset=offset, sort=sort, state=state, origin=origin, username=username,
                                      hostname=hostname, get_all=get_all)
