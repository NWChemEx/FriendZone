# Copyright 2025 NWChemEx-Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from importlib.util import find_spec


def friends() -> list[str]:
    """Returns a list of potentially supported friends.

    :return: A list of names of potentially supported friends.
    :rtype: list[str]
    """
    friends_list = [
        "ase",
        "nwchem",
    ]
    return friends_list


def is_friend_enabled(friend: str) -> bool:
    """Wraps the process of determining if a particular friend was enabled.

    :param friend: Name of friend to check
    :type friend: str

    :return: True if FriendZone was configured with support for ``friend``
             and false otherwise.
    :rtype: bool
    """
    return friend in friends() and find_spec(friend) is not None
