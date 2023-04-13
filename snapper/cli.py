"""
Module to define CLI using Typer
"""

import logging
import re
from dataclasses import dataclass
from typing import Any

import typer
from natsort import natsorted
from pydavinci import davinci
from pyfiglet import Figlet
from rich import print, traceback

from snapper import utils

utils.setup_rich_logging()

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

fig = Figlet(font="rectangles")
traceback.install()

resolve = davinci.Resolve()

app = typer.Typer()
print(fig.renderText("snapper"))
print("[bold]Create and manage DaVinci Resolve timeline revisions :fish:\n")


@dataclass(repr=True)
class ExtendedClip:

    clip = Any
    media_pool_path = Any

    def __repr__(self):
        return f"'Clip: {self.clip}, Media Pool Path: {self.media_pool_path})'"


def get_clip_with_path(item_name: str, item_type: str) -> ExtendedClip | None:
    """
    Gets a clip's 'media pool path'.

    There's currently no way in API to retrieve the path of an object in media pool.
    Use it to generate subfolders relative to existing items.

    Args:
        item_name (str): The item name whose path you're looking for
        item_type (str): The item type whose path you're looking for

    Returns:
        item_path
    """
    resolve = davinci.Resolve()

    # Start
    root = resolve.media_pool.root_folder
    resolve.media_pool.set_current_folder(root)

    current_path = []

    def walk_folders(folder):
        # Replace 'Master' with inital '/' in path
        logger.debug(f"[magenta]'/{'/'.join(current_path[1:])}'")

        current_path.append(folder.name)

        for clip in folder.clips:
            properties = clip.properties
            if not properties:
                continue

            if properties["Type"] == item_type:
                if properties["File Name"] == item_name:
                    final_path = "/" + "/".join(current_path[1:])
                    logger.debug(
                        f"[magenta]Found item '{properties['File Name']}'"
                        f"at path '{final_path}'"
                    )

                    extended_clip = ExtendedClip()
                    extended_clip.clip = clip
                    extended_clip.media_pool_path = final_path

                    raise StopIteration(extended_clip)

        for x in folder.subfolders:
            walk_folders(x)
            current_path.pop()

    logger.debug("[magenta]Walking media pool...")
    try:
        walk_folders(root)
    except StopIteration as exception_args:
        extended_clip = exception_args.args[0]
        return extended_clip

    return None


def get_folder_from_media_pool_path(media_pool_path: str, create=True):
    """
    Gets a folder object from a 'media_pool_path' in Resolve's media pool.

    Pass create to create the path if it doesn't exist.
    Since it's using a path, it can only create one subfolder at a time.
    Not a whole tree.

    Use it to create/ensure an output path.

    Args:
        folder_path (str): Path to create folder structure from

    Returns:
        folder (folder): The Resolve folder object
        of the last subfolder in provided path
    """

    # cross platformish
    media_pool_path = media_pool_path.replace("\\", "/")
    path_segments = media_pool_path.split("/")
    path_segments = [x for x in path_segments if x != ""]

    media_pool = resolve.media_pool
    root_folder = media_pool.root_folder

    def get_subfolder(parent_folder, subfolder_name: str):
        """
        Return a subfolder by name within a given parent folder.

        Args:
            current_folder (Folder): _description_
            subfolder_name (str): _description_

        Returns:
            Folder: Subfolder as media pool folder object
        """
        for x in parent_folder.subfolders:
            if x.name == subfolder_name:
                return x
        return None

    # Started from the bottom now we're here
    media_pool.set_current_folder(root_folder)
    current_folder = root_folder

    for i, seg in enumerate(path_segments):

        # If folder exists, navigate

        if sub := get_subfolder(current_folder, seg):
            logger.debug(f"[magenta]Found subfolder '{sub.name}'")
            media_pool.set_current_folder(sub)
            current_folder = media_pool.current_folder
            continue

        if not create:
            raise ValueError(
                f"Path '{media_pool_path}' doesn't exist."
                f"Stopped at missing subfolder: '{path_segments[i:]}'"
                "You can set 'create=True' to create the path if it should."
            )

        # If not, make the whole structure
        remaining_segs = path_segments[i:]

        for x in remaining_segs:

            current_folder = media_pool.current_folder
            logger.debug(
                f"[magenta]Creating subfolder '{x}' in '{current_folder.name}'"
            )
            new_folder = media_pool.add_subfolder(x, current_folder)
            if not media_pool.set_current_folder(new_folder):

                logger.error(
                    f"Couldn't create subfolder '{x}'"
                    f"for path '{media_pool_path}' in media pool"
                )
                return None

            current_folder = new_folder

        logger.debug("[magenta]Created folder structure")
        return current_folder

    logger.debug("[magenta]Found all folders. Nothing created")
    return current_folder


@app.command()
def new(
    dry_run: bool = typer.Option(
        False,
        help="Don't duplicate the timeline, just return the next version name",
    )
):
    """Create a new timeline snapshot"""

    print("[cyan]Getting current timeline :bulb:")
    current_timeline = resolve.active_timeline
    current_timeline_name = current_timeline.name
    logger.debug(f"[magenta]Current timeline name: '{current_timeline_name}'")

    def get_next_version_name():
        """Get the next version number for current timeline"""

        versions = []
        for timeline in resolve.project.timelines:

            if timeline is not None:

                logger.debug(f'[magenta]Found timeline: "{timeline.name}"')
                if re.search(
                    rf"^({re.escape(current_timeline_name)})(\s)(V\d+)",
                    timeline.name,
                    re.IGNORECASE,
                ):
                    logger.debug(f"[magenta]Found snapshot: {timeline.name}")
                    versions.append(timeline.name)

        # If none exist, start first
        if not versions:

            logger.debug("[magenta]No snapshots exist. Starting first.")
            return f"{current_timeline_name} V1"

        # Get last snapshot version
        last_version = natsorted(versions).pop()
        logger.debug(f"[magenta]Last snapshot version: {last_version}")

        # Increment snapshot version number
        next_version = re.sub(
            r"[0-9]+$",
            lambda x: f"{str(int(x.group())+1).zfill(len(x.group()))}",
            last_version,
        )

        next_version = str(next_version)
        logger.debug(f"[magenta]Next snapshot version: '{next_version}'")
        return next_version

    print("[cyan]Getting next snapshot version :mag_right:")
    next_version_name = get_next_version_name()

    if dry_run:

        print(
            "[bold][yellow]Dry-run enabled:[/bold]"
            "No timeline snapshot will be created."
        )
        utils.app_exit(0)

    print("[yellow]Cloning timeline :dna:")
    current_timeline.name = next_version_name  # Rename original
    current_timeline.duplicate_timeline(current_timeline_name)
    print(
        "[green]Latest snapshot:"
        f"[bold]'{next_version_name}'[/bold] :heavy_check_mark:"
    )

    print("[cyan]Selecting '@Snapshots' subfolder :file_folder:")
    extended_clip = get_clip_with_path(next_version_name, "Timeline")

    if not extended_clip:

        logger.warning(
            "[yellow]Couldn't get timeline path to make snapshot subfolder!"
            "Locate and tidy up manually"
        )
        utils.app_exit(1, -1)

    snapshots_path = extended_clip.media_pool_path + "/@Snapshots"
    snapshots_folder = get_folder_from_media_pool_path(snapshots_path)

    if not snapshots_folder:

        logger.warning(
            "[yellow]Couldn't get snapshots folder." "Locate and tidy up manually"
        )
        utils.app_exit(1, -1)

    assert resolve.media_pool.move_clips([extended_clip.clip], snapshots_folder)

    utils.app_exit(0, 2)


@app.callback()
def main(
    verbose: bool = typer.Option(False, help="Log debug messages"),
):
    """
    Do yourself a favour and create frequent timeline snapshots.
    Don't leave messy little experiments at the end of your timelines.
    Keep it tidy. Keep it clean.

    Just type: "snapper new"
    """

    if verbose:
        logger.setLevel("DEBUG")


if __name__ == "__main__":
    app()
