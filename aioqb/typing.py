"""
Copyright (c) 2008-2021 synodriver <synodriver@gmail.com>
"""
from typing import Callable

JsonDumps = Callable[[dict], str]
JsonLoads = Callable[[str], dict]
