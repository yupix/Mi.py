from typing import Any, Dict, Optional

from pydantic import BaseModel

from mi import config, exception
from mi.utils import api


class DriveAction(object):
    @staticmethod
    def upload(
            name: str = None,
            to_file: str = None,
            to_url: str = None,
            *,
            force: bool = False,
            is_sensitive: bool = False
    ) -> 'Drive':
        """
        Parameters
        ----------
        is_sensitive : bool
            この画像がセンシティブな物の場合Trueにする
        force : bool
            Trueの場合同じ名前のファイルがあった場合でも強制的に保存する
        to_file : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name: str
            ファイル名(拡張子があるなら含めて)
        to_url : str
            アップロードしたいファイルのURL

        Returns
        -------
        Drive: Drive
            upload後のレスポンスをDrive型に変更して返します
        """

        if to_file and to_url is None:  # ローカルからアップロードする
            with open(to_file, 'rb') as f:
                file = f.read()
            args = {'isSensitive': is_sensitive, 'force': force, 'name': f'{name}'}
            file = {'file': file}
            res = api('/api/drive/files/create', json_data=args, files=file, auth=True).json()
        elif to_file is None and to_url:  # URLからアップロードする
            args = {'url': to_url, 'force': force, 'isSensitive': is_sensitive}
            res = api('/api/drive/files/upload-from-url', json_data=args, auth=True).json()
        else:
            raise exception.InvalidParameters('path または url のどちらかは必須です')
        return Drive(**res)


class Properties(BaseModel):
    width: int
    height: int
    avgColor: str


class Folder(BaseModel):
    id: str
    createdAt: str
    name: str
    foldersCount: int
    filesCount: int
    parentId: str
    parent: Dict[str, Any]


class File(BaseModel):
    id: str
    createdAt: str
    name: str
    type: str
    md5: str
    size: int
    isSensitive: bool
    blurhash: str
    properties: Properties
    url: str
    thumbnailUrl: str
    comment: str
    folderId: str
    folder: Folder
    userId: str
    user: Dict[str, Any]


class Drive(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    md5: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None
    folder_id: Optional[str] = None
    is_sensitive: Optional[bool] = False
    blurhash: Optional[str] = None
    __drive_action = DriveAction()

    class Config:
        arbitrary_types_allowed = True

    def upload(self, path: str, name: str = None, force: bool = False, is_sensitive: bool = False, url: str = None) -> 'Drive':
        """
        parameters
        ----------
        is_sensitive : bool
            この画像がセンシティブな物の場合trueにする
        force : bool
            trueの場合同じ名前のファイルがあった場合でも強制的に保存する
        path : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name: str
            ファイル名(拡張子があるなら含めて)
        url : str
            urlから画像をアップロードする

        returns
        -------
        drive: drive
            upload後のレスポンスをdrive型に変更して返します
        """

        return self.__drive_action.upload(path, name, force, is_sensitive, url)
