import json
import sys
from functools import partial
from typing import Any, Dict, List, Optional

import requests
import requests.utils

from exceptions import *


class InstaloaderContext:
    def __init__(self, sleep: bool = True, quiet: bool = False,
                 max_connection_attempts: int = 3, request_timeout: Optional[float] = None):
        self.request_timeout = request_timeout
        self.username = None
        self.sleep = sleep
        self.quiet = quiet
        self.max_connection_attempts = max_connection_attempts
        self._graphql_page_length = 50
        self._root_rhx_gis = None

        # error log, filled with error() and printed at the end of Instaloader.main()
        self.error_log = []  # type: List[str]

        # Can be set to True for testing, disables supression of InstaloaderContext._error_catcher
        self.raise_all_errors = False

        # Cache profile from id (mapping from id to Profile)
        self.profile_id_cache = dict()  # type: Dict[int, Any]

    @property
    def is_logged_in(self) -> bool:
        return bool(self.username)

    def log(self, *msg, sep='', end='\n', flush=False):
        if not self.quiet:
            print(*msg, sep=sep, end=end, flush=flush)

    def error(self, msg, repeat_at_end=True):
        print(msg, file=sys.stderr)
        if repeat_at_end:
            self.error_log.append(msg)

    def close(self):
        """Print error log and close session"""
        if self.error_log and not self.quiet:
            print("\nErrors occured:", file=sys.stderr)
            for err in self.error_log:
                print(err, file=sys.stderr)
        self._session.close()

    def login(self, user, passwd):
        import http.client
        http.client._MAXHEADERS = 200
        session = requests.Session()
        session.cookies.update({'sessionid': '', 'mid': '', 'ig_pr': '1',
                                'ig_vw': '1920', 'ig_cb': '1', 'csrftoken': '',
                                's_network': '', 'ds_user_id': ''})
        session.headers.update(self._default_http_header())
        if self.request_timeout is not None:
            session.request = partial(session.request, timeout=self.request_timeout)  # type: ignore
        session.get('https://www.instagram.com/web/__mid/')
        csrf_token = session.cookies.get_dict()['csrftoken']
        session.headers.update({'X-CSRFToken': csrf_token})
        self.do_sleep()
        login = session.post('https://www.instagram.com/accounts/login/ajax/',
                             data={'password': passwd, 'username': user}, allow_redirects=True)
        try:
            resp_json = login.json()
        except json.decoder.JSONDecodeError:
            raise ConnectionException(
                "Login error: JSON decode fail, {} - {}.".format(login.status_code, login.reason))
