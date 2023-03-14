"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""


class BaseQbittorrentException(Exception):
    pass


class IPBanedException(BaseQbittorrentException):
    """
    IP被ban
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)


class HashNotFoundException(BaseQbittorrentException):
    """
    找不到这个hash
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)


class ApiFailedException(BaseQbittorrentException):
    """
    其他原因导致的api调用失败
    """

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)
