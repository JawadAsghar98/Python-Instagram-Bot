from typing import Any, Dict, Iterator, List, Optional, Union

from exceptions import *
from instaloadercontext import InstaloaderContext


class Post:

    def __init__(self, context: InstaloaderContext, node: Dict[str, Any],
                 owner_profile: Optional['Profile'] = None):
        assert 'shortcode' in node or 'code' in node

        self._context = context
        self._node = node
        self._owner_profile = owner_profile
        self._full_metadata_dict = None  # type: Optional[Dict[str, Any]]
        self._rhx_gis_str = None         # type: Optional[str]
        self._location = None            # type: Optional[PostLocation]



    @property
    def owner_username(self) -> str:
        """The Post's lowercase owner name."""
        return self.owner_profile.username

    @property
    def owner_id(self) -> int:
        """The ID of the Post's owner."""
        return self.owner_profile.userid

    @property
    def profile(self) -> str:
        """Synonym to :attr:`~Post.owner_username`"""
        return self.owner_username


class Profile:
    def __init__(self, context: InstaloaderContext, node: Dict[str, Any]):
        assert 'username' in node
        self._context = context
        self._has_public_story = None  # type: Optional[bool]
        self._node = node
        self._has_full_metadata = False
        self._rhx_gis = None
        self._iphone_struct_ = None
        if 'iphone_struct' in node:
            # if loaded from JSON with load_structure_from_file()
            self._iphone_struct_ = node['iphone_struct']

    @classmethod
    def from_username(cls, context: InstaloaderContext, username: str):
        profile = cls(context, {'username': username.lower()})
        profile._obtain_metadata()  # to raise ProfileNotExistException now in case username is invalid
        return profile

    @classmethod
    def from_id(cls, context: InstaloaderContext, profile_id: int):
        if profile_id in context.profile_id_cache:
            return context.profile_id_cache[profile_id]
        data = context.graphql_query('7c16654f22c819fb63d1183034a5162f',
                                     {'user_id': str(profile_id),
                                      'include_chaining': False,
                                      'include_reel': True,
                                      'include_suggested_users': False,
                                      'include_logged_out_extras': False,
                                      'include_highlight_reels': False},
                                     rhx_gis=context.root_rhx_gis)['data']['user']
        if data:
            profile = cls(context, data['reel']['owner'])
        else:
            raise ProfileNotExistsException("No profile found, the user may have blocked you (ID: " +
                                            str(profile_id) + ").")
        context.profile_id_cache[profile_id] = profile
        return profile