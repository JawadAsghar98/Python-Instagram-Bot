import sys
from typing import List, Optional
from instaloader import Instaloader


def _main(instaloader: Instaloader, targetlist: List[str],
          username: Optional[str] = None, password: Optional[str] = None,
          sessionfile: Optional[str] = None,
          fast_update: bool = False,
          max_count: Optional[int] = None,
          storyitem_filter_str: Optional[str] = None) -> None:
    post_filter = None

    if username is not None:
        try:
            instaloader.load_session_from_file(username, sessionfile)
        except FileNotFoundError as err:
            if sessionfile is not None:
                print(err, file=sys.stderr)
            instaloader.context.log("Session file does not exist yet - Logging in.")
        if not instaloader.context.is_logged_in or username != instaloader.test_login():
            if password is not None:
                instaloader.login(username, password)
            else:
                instaloader.interactive_login(username)
        instaloader.context.log("Logged in as %s." % username)
    # since 4.2.9 login is required for geotags
    if instaloader.download_geotags and not instaloader.context.is_logged_in:
        instaloader.context.error("Warning: Use --login to download geotags of posts.")
    # Try block for KeyboardInterrupt (save session on ^C)
    profiles = set()
    anonymous_retry_profiles = set()
    try:
        # Generate set of profiles, already downloading non-profile targets
        for target in targetlist:

            target = target.rstrip('/')
            with instaloader.context.error_catcher(target):

                if target == ":saved":
                    instaloader.download_saved_posts(fast_update=fast_update, max_count=max_count,
                                                     post_filter=post_filter)
                else:

                    profile = instaloader.check_profile_id(target)
                    profiles.add(profile)
                    # Not only our profile.has_blocked_viewer condition raises ProfileNotExistsException,
                    # check_profile_id() also does, since access to blocked profile may be responded with 404.

    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
    # Save session if it is useful
    if instaloader.context.is_logged_in:
        instaloader.save_session_to_file(sessionfile)
    # User might be confused if Instaloader does nothing
    if not targetlist:
        if instaloader.context.is_logged_in:
            # Instaloader did at least save a session file
            instaloader.context.log("No targets were specified, thus nothing has been downloaded.")


def main():
    if __name__ == "__main__":
        main()
