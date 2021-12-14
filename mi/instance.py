from __future__ import annotations

from typing import Dict, Iterator, List, Optional, TYPE_CHECKING

from .types.instance import (Instance as InstancePayload,
                             Meta as InstanceMetaPayload)
from .emoji import Emoji

if TYPE_CHECKING:
    from .user import User
    from . import ConnectionState


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
        self.emojis: List[Emoji] = [Emoji(i, state=state) for i in data['emojis']]
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
    def __init__(self, data: InstancePayload, state: ConnectionState):
        """
        インスタンス情報
        
        Parameters
        ----------
        data : InstancePayload
            インスタンス情報の入った dict
        state: ConnectionState
            botのコネクション
        """

        self.host: Optional[str] = data.get("host")
        self.name: Optional[str] = data.get("name")
        self.software_name: Optional[str] = data.get("software_name")
        self.software_version: Optional[str] = data.get("software_version")
        self.icon_url: Optional[str] = data.get("icon_url")
        self.favicon_url: Optional[str] = data.get("favicon_url")
        self.theme_color: Optional[str] = data.get("theme_color")
        self._state = state

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
                  ) -> Iterator[User]:
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
        Iterator[User]
        """
        return self._state.get_users(limit=limit, offset=offset, sort=sort, state=state, origin=origin, username=username,
                                     hostname=hostname, get_all=get_all)
