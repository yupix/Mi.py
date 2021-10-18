from typing import Any, Dict, Optional

from pydantic import BaseModel

from mi import conn


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

        if url is None and self.url:
            url = self.url

        return Drive(**conn.file_upload(name, path, url, force=force, is_sensitive=is_sensitive))
