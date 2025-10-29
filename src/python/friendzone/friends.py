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

import logging

logger = logging.getLogger(__name__)


def friends() -> dict[str, bool]:
    """Returns a dictionary of potential friends and whether they were enabled.

    :return: Key-value pairs where the key is the name of a potential
             friend and the value is whether that friend was enabled or not
    """
    friends_list = {"ase": False, "nwchem": False}

    try:
        import ase

        friends_list["ase"] = True
    except ImportError:
        logger.warning("Module not enabled: ase")

    try:
        import networkx
        import qcelemental
        import qcengine

        friends_list["nwchem"] = True
    except ImportError:
        logger.warning("Module not enabled: nwchem")

    return friends_list


def is_friend_enabled(friend: str) -> bool:
    """Wraps the process of determining if a particular friend was enabled.

    :return: True if FriendZone was configured with support for ``friend``
             and false otherwise.
    :rtype: bool
    """
    all_friends = friends()

    if friend in all_friends:
        return all_friends[friend]

    return False
