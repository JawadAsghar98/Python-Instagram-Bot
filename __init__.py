"""Download pictures (or videos) along with their captions and other metadata from Instagram."""


__version__ = '4.3'


try:
    # pylint:disable=wrong-import-position
    import win_unicode_console  # type: ignore
except ImportError:
    pass
else:
    win_unicode_console.enable()