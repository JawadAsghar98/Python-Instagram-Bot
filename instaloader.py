from typing import Any, Callable, Optional
import instaloadercontext
from structures import (Post, Profile)


class Instaloader:
    def __init__(self,
                 sleep: bool = True,
                 quiet: bool = False,
                 user_agent: Optional[str] = None,
                 dirname_pattern: Optional[str] = None,
                 filename_pattern: Optional[str] = None,
                 post_metadata_txt_pattern: str = None,
                 max_connection_attempts: int = 3,
                 request_timeout: Optional[float] = None,
                 commit_mode: bool = False):

        self.context = instaloadercontext.InstaloaderContext(sleep, quiet, user_agent, max_connection_attempts)

        # configuration parameters
        self.dirname_pattern = dirname_pattern or "{target}"
        self.filename_pattern = filename_pattern or "{date_utc}_UTC"
        self.post_metadata_txt_pattern = '{caption}' if post_metadata_txt_pattern is None \
            else post_metadata_txt_pattern
        self.commit_mode = commit_mode

        # Used to keep state in commit mode
        self._committed = None  # type: Optional[bool]

    def close(self):
        """Close associated session objects and repeat error log."""
        self.context.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def login(self, user: str, passwd: str) -> None:
        self.context.login(user, passwd)

    def download_saved_posts(self, max_count: int = None, fast_update: bool = False,
                             post_filter: Optional[Callable[[Post], bool]] = None) -> None:
        self.context.log("Retrieving saved posts...")
        count = 1
        assert self.context.username is not None
        for post in Profile.from_username(self.context, self.context.username).get_saved_posts():
            if max_count is not None and count > max_count:
                break
            if post_filter is not None and not post_filter(post):
                self.context.log("<{} skipped>".format(post), flush=True)
                continue
            self.context.log("[{:>3}] ".format(count), end=str(), flush=True)
            count += 1
            with self.context.error_catcher('Download saved posts'):
                downloaded = self.download_post(post, target=':saved')
                if fast_update and not downloaded:
                    break
