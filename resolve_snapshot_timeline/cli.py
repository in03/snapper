#!/usr/bin/python3.6

import logging
import re

from rich import print
import typer

from natsort import natsorted

from resolve_snapshot_timeline import utils
from resolve_snapshot_timeline.resolve import ResolveObjects

utils.setup_rich_logging()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

app = typer.Typer()

print("\n[bold green u]RESOLVE SNAPSHOT TIMELINE[/bold green u] :camera:\n")


@app.command()
def new(
    dry_run: bool = typer.Option(
        False, help="Don't duplicate the timeline, just return the next version name"
    )
):
    """Create a new timeline snapshot"""

    project_manager = r_.resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()

    logger.info(f"[cyan]Getting current timeline :bulb:")

    current_timeline = project.GetCurrentTimeline()
    current_timeline_name = current_timeline.GetName()

    def get_next_version_name():
        """Get the next version number for current timeline"""

        timeline_count = project.GetTimelineCount()

        versions = []
        for i in range(0, timeline_count):

            timeline_index = project.GetTimelineByIndex(i + 1)
            timeline_name = timeline_index.GetName()

            if timeline_name is not None:

                logger.debug(f'[magenta]Found timeline: "{timeline_name}"')
                if re.search(
                    rf"^({current_timeline_name})(\s)(V\d+)",
                    timeline_name,
                    re.IGNORECASE,
                ):
                    logger.debug(f"[magenta]Found snapshot: {timeline_name}")
                    versions.append(timeline_name)

        # If none exist, start first
        if len(versions) == 0:

            logger.debug(f"[magenta]No snapshots exist. Starting first.")
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

    logger.info(f"[cyan]Getting next snapshot version :mag_right:")
    next_version_name = get_next_version_name()

    if dry_run:

        logger.warning(
            "[bold][yellow]Dry-run enabled:[/bold] No timeline snapshot will be created."
        )
        utils.app_exit(0)

    logger.info(f"[yellow]Cloning timeline :dna:")
    current_timeline.SetName(next_version_name)  # Rename original
    current_timeline.DuplicateTimeline(current_timeline_name)

    logger.info(f"[green]Done! :heavy_check_mark:")


def tidy_into_snapshots_folder():
    """Tidy loose timeline snapshots into a versions folder"""
    # TODO: Implement version tidy up script


@app.callback()
def main(
    verbose: bool = typer.Option(False, help="Log debug messages"),
    quiet: bool = typer.Option(False, help="Log nothing"),
):
    """
    Do yourself a favour and create frequent timeline snapshots :camera_flash:
    Don't leave messy little experiments at the end of your timelines :no_entry:
    Keep it tidy. Keepy it clean. :sparkles:
    """

    if verbose:
        logger.setLevel("DEBUG")

    if quiet:
        logger.setLevel("WARNING")

    # Get resolve variables
    global r_
    r_ = ResolveObjects()


if __name__ == "__main__":
    app()
