"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""


class BaseQbittorrentException(Exception):
    pass


class IPBanedException(BaseQbittorrentException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return f'{self.__class__.__name__}: {self.msg}'


class HashNotFoundException(BaseQbittorrentException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return f'{self.__class__.__name__}: {self.msg}'


class ApiFailedException(BaseQbittorrentException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return f'{self.__class__.__name__}: {self.msg}'
