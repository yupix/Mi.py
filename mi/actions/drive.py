from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.api.drive import DriveManager, FileManager, FolderManager

if TYPE_CHECKING:
    from mi.state import ConnectionState
    from mi.http import HTTPClient

__all__ = ['FolderActions', 'DriveActions']


class FolderActions:
    def __init__(
            self, client: 'ConnectionState',
            http: HTTPClient,
            loop: asyncio.AbstractEventLoop,
            *,
            folder_id: Optional[str] = None
    ):
        self.client = client
        self.http = http
        self.loop = loop
        self.action: FolderManager = FolderManager(self.client, self.http, self.loop, folder_id=folder_id)


class DriveActions:
    def __init__(
            self, state: 'ConnectionState',
            http: HTTPClient,
            loop: asyncio.AbstractEventLoop,
    ):
        self.state = state
        self.http = http
        self.loop = loop
        self.action: DriveManager = DriveManager(self.state, self.http, self.loop)
        self.folder: FolderActions = FolderActions(self.state, self.http, self.loop)
        self.files: FileManager = FileManager(state, http, loop)

    def get_folder_instance(self, folder_id: str) -> FolderActions:
        return FolderActions(self.state, self.http, self.loop, folder_id=folder_id)
