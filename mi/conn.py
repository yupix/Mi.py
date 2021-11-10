import typing
from functools import cache

import requests

from mi.next_utils import check_multi_arg

from mi import exception
from mi.exception import InvalidParameters, NotExistRequiredParameters
from mi.utils import api, remove_dict_empty, upper_to_lower


class Controller:
    @staticmethod
    async def delete_chat(message_id: str) -> requests.models.Response:
        args = {"messageId": f"{message_id}"}
        return api("/api/messaging/messages/delete", json_data=args, auth=True)

    @staticmethod
    def get_user_notes(
        user_id: str,
        *,
        since_id: str = None,
        include_my_renotes: bool = True,
        include_replies: bool = True,
        with_files: bool = False,
        until_id: str = None,
        limit: int = 10,
        get_all: bool = False,
        exclude_nsfw: bool = True,
        file_type: list = None,
        since_date: int = 0,
        until_data: int = 0,
    ) -> typing.Iterator[dict]:
        if limit > 100:
            raise InvalidParameters("limit は100以上を受け付けません")

        args = remove_dict_empty(
            {
                "userId": user_id,
                "includeReplies": include_replies,
                "limit": limit,
                "sinceId": since_id,
                "untilId": until_id,
                "sinceDate": since_date,
                "untilDate": until_data,
                "includeMyRenotes": include_my_renotes,
                "withFiles": with_files,
                "fileType": file_type,
                "excludeNsfw": exclude_nsfw,
            }
        )
        if get_all:
            loop = True
            while loop:
                get_data = api("/api/users/notes", json_data=args, auth=True).json()
                if len(get_data) <= 0:
                    break
                args["untilId"] = get_data[-1]["id"]
                for data in get_data:
                    yield upper_to_lower(
                        data, replace_list={"user": "author", "text": "content"}
                    )
        else:
            get_data = api("/api/users/notes", json_data=args, auth=True).json()
            for data in get_data:
                yield upper_to_lower(
                    data, replace_list={"user": "author", "text": "content"}
                )

    @staticmethod
    @cache
    def get_instance_meta() -> dict:
        """
        BOTのアカウントがあるインスタンス情報をdictで返します。一度実行するとキャッシュされます。

        Returns
        -------
        dict:
            インスタンス情報
        """
        return api("/api/meta").json()

    def fetch_instance_meta(self) -> dict:
        """
        BOTのアカウントがある最新のインスタンス情報をdictで返します

        Returns
        -------
        dict:
            インスタンス情報
        """
        self.get_instance_meta.cache_clear()
        return api("/api/meta").json()

    @cache
    def get_user(
        self, user_id: str = None, username: str = None, host: str = None
    ) -> dict:
        """
        ユーザーのプロフィールを取得します。一度のみサーバーにアクセスしキャッシュをその後は使います。
        fetch_userを使った場合はキャッシュが廃棄され再度サーバーにアクセスします。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        dict:
            ユーザー情報
        """
        return self.fetch_user(user_id, username, host)

    def fetch_user(
        self, user_id: str = None, username: str = None, host: str = None
    ) -> dict:
        """
        サーバーにアクセスし、ユーザーのプロフィールを取得します。基本的には get_userをお使いください。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        dict:
            ユーザー情報
        """
        if not check_multi_arg(user_id, username):
            raise NotExistRequiredParameters("user_id, usernameどちらかは必須です")

        data = remove_dict_empty(
            {"userId": user_id, "username": username, "host": host}
        )
        self.get_user.cache_clear()
        return api("/api/users/show", json_data=data, auth=True).json()

    @staticmethod
    def get_followers(
        user_id: str = None,
        username: str = None,
        host: str = None,
        since_id: str = None,
        until_id: str = None,
        limit: int = 10,
        get_all: bool = False,
    ) -> typing.Iterator[dict]:
        """
        与えられたユーザーのフォロワーを取得します

        Parameters
        ----------
        user_id : str, default=None
            ユーザーのid
        username : str, default=None
            ユーザー名
        host : str, default=None
            ユーザーがいるインスタンスのhost名
        since_id : str, default=None
        until_id : str, default=None
            前回の最後の値を与える(既に実行し取得しきれない場合に使用)
        limit : int, default=10
            取得する情報の最大数 max: 100
        get_all : bool, default=False
            全てのフォロワーを取得する

        Yields
        ------
        dict
            フォロワーの情報

        Raises
        ------
        InvalidParameters
            limit引数が不正な場合
        """
        if not check_multi_arg(user_id, username):
            raise NotExistRequiredParameters("user_id, usernameどちらかは必須です")

        if limit > 100:
            raise InvalidParameters("limit は100以上を受け付けません")

        data = remove_dict_empty(
            {
                "userId": user_id,
                "username": username,
                "host": host,
                "sinceId": since_id,
                "untilId": until_id,
                "limit": limit,
            }
        )
        if get_all:
            loop = True
            while loop:
                get_data = api("/api/users/followers", json_data=data, auth=True).json()
                if len(get_data) > 0:
                    data["untilId"] = get_data[-1]["id"]
                else:
                    break
                yield get_data
        else:
            get_data = api("/api/users/followers", json_data=data, auth=True).json()
            yield get_data

    @staticmethod
    def file_upload(
        name: str = None,
        to_file: str = None,
        to_url: str = None,
        *,
        force: bool = False,
        is_sensitive: bool = False,
    ) -> dict:
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
            with open(to_file, "rb") as f:
                file = f.read()
            args = {"isSensitive": is_sensitive, "force": force, "name": f"{name}"}
            file = {"file": file}
            res = api(
                "/api/drive/files/create", json_data=args, files=file, auth=True
            ).json()
        elif to_file is None and to_url:  # URLからアップロードする
            args = {"url": to_url, "force": force, "isSensitive": is_sensitive}
            res = api(
                "/api/drive/files/upload-from-url", json_data=args, auth=True
            ).json()
        else:
            raise exception.InvalidParameters("path または url のどちらかは必須です")
        return res

    @staticmethod
    def get_announcements(limit: int, with_unreads: bool, since_id: str, until_id: str):
        """

        Parameters
        ----------
        limit: int
            最大取得数
        with_unreads: bool
            既読済みか否か
        since_id: str
        until_id: str
            前回の最後の値を与える(既に実行し取得しきれない場合に使用)

        Returns
        -------

        """

        if limit > 100:
            raise InvalidParameters("limit は100以上を受け付けません")

        args = {
            "limit": limit,
            "withUnreads": with_unreads,
            "sinceId": since_id,
            "untilId": until_id,
        }
        return api("/api/announcements", args, auth=True)
