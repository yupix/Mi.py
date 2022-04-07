from typing import List, Optional

from mi.framework.http import HTTPSession
from mi.framework.router import Route
from mi.wrapper.models import RawFile


class MiFile:
    def __init__(self, path: Optional[str] = None,
                 file_id: Optional[str] = None,
                 name: Optional[str] = None,
                 folder_id: Optional[str] = None,
                 comment: Optional[str] = None,
                 is_sensitive: bool = False,
                 force: bool = False
                 ):
        self.name = name
        self.folder_id = folder_id
        self.comment = comment
        self.is_sensitive = is_sensitive
        self.force = force
        self.path = path
        self.file_id = file_id


async def check_upload(files: List[MiFile]):
    _files = []
    for file in files:
        if file.path:
            endpoint = Route('POST', '/api/drive/files/create')
            data = {'file': open(file.path, 'rb'),
                    'name': file.name,
                    'folderId': file.folder_id,
                    'isSensitive': file.is_sensitive,
                    'comment': file.comment,
                    'force': file.force}
            _files.append(RawFile(await HTTPSession.request(endpoint, auth=True, data=data, lower=True)).id)
        else:
            _files.append(file.file_id)

    return _files


async def get_file_ids(files: List[MiFile]):
    return await check_upload(files)
