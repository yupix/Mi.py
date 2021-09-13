from typing import Any, Dict, Optional

from pydantic import BaseModel

from mi import config
from mi.utils import api


class DriveAction(object):
    def upload(self, path: str, name: str = None, force: bool = False, is_sensitive: bool = False) -> 'Drive':
        """

        Parameters
        ----------
        is_sensitive : bool
            この画像がセンシティブな物の場合Trueにする
        force : bool
            Trueの場合同じ名前のファイルがあった場合でも強制的に保存する
        path : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name: str
            ファイル名(拡張子があるなら含めて)

        Returns
        -------
        Drive: Drive
            upload後のレスポンスをDrive型に変更して返します
        """
        with open(path, 'rb') as f:
            file = f.read()
        args = {'i': f'{config.i.token}', 'isSensitive': is_sensitive, 'force': force, 'name': f'{name}'}
        file = {'file': file}
        res = api(config.i.origin_uri, '/api/drive/files/create', data=args, files=file).json()
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


class Drive(BaseModel, DriveAction):
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
