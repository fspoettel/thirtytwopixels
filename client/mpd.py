import os
from pathlib import Path
from subprocess import check_output


# @see https://beets.readthedocs.io/en/stable/plugins/fetchart.html
COVER_NAME = "cover"
COVER_EXTS = (".jpg", ".jpeg", ".png")
MUSIC_DIR = os.getenv("DIR_BEETS")


def get_playback_file():
    state = check_output(["mpc", "--format", "%file%", "current"]).decode("utf-8")

    lines = state.splitlines()[:1]
    if lines:
        file = Path(MUSIC_DIR) / lines[0]
        # mpd may be playing a file outside of `MUSIC_DIR`
        return file if file.exists() else None

    return None


def get_parent_dir(file):
    return file.resolve().parent if file else None


def get_cover_file(directory):
    cover = None
    for ext in COVER_EXTS:
        cover_path_lower = directory / "{}{}".format(COVER_NAME, ext.lower())
        cover_path_upper = directory / "{}{}".format(COVER_NAME, ext.upper())

        if cover_path_lower.is_file():
            cover = cover_path_lower
            break
        elif cover_path_upper.is_file():
            cover = cover_path_upper
            break

    if not cover:
        raise ValueError("No cover found")
    return cover


def get_cover():
    file = get_playback_file()
    if not file:
        raise IOError("Nothing is currently playing.")

    album = get_parent_dir(file)
    if not album:
        raise ValueError("Could not locate current playback in directory.")

    return get_cover_file(album)
