from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mi.wrapper.drive import DriveManager, FileManager, FolderManager

if TYPE_CHECKING:
    pass

__all__ = ['FolderActions', 'DriveActions']


class FolderActions:
    def __init__(
            self,
            folder_id: Optional[str] = None
    ):
        self.action: FolderManager = FolderManager(folder_id=folder_id)


class DriveActions:
    def __init__(
            self
    ):
        self.action: DriveManager = DriveManager()
        self.folder: FolderActions = FolderActions()
        self.files: FileManager = FileManager()

    def get_folder_instance(self, folder_id: str) -> FolderActions:
        return FolderActions(folder_id=folder_id)
