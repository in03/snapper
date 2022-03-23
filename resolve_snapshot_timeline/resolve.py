import imp
import logging
import sys

from rich import print

from resolve_snapshot_timeline import utils

utils.setup_rich_logging()
logger = logging.getLogger(__name__)

utils.install_rich_tracebacks()


class ResolveObjects:
    def __init__(self):
        self._populate_variables()

    def _get_resolve(self):

        ext = ".so"
        if sys.platform.startswith("darwin"):
            path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
            ext = ".dll"
        elif sys.platform.startswith("linux"):
            path = "/opt/resolve/libs/Fusion/"
        else:
            raise Exception("Unsupported system! " + sys.platform)

        bmd = imp.load_dynamic("fusionscript", path + "fusionscript" + ext)
        resolve = bmd.scriptapp("Resolve")

        if not resolve:
            return None

        try:
            sys.modules[__name__] = resolve
        except ImportError:
            return None

        return resolve

    def _populate_variables(self):

        try:

            self.resolve = self._get_resolve()
            if self.resolve is None:
                raise TypeError

        except:

            logger.warning(
                "[red] :warning: Couldn't access the Resolve Python API. Is DaVinci Resolve running?[/]"
            )
            utils.app_exit(1, -1)

        try:

            self.project = self.resolve.GetProjectManager().GetCurrentProject()
            if self.project is None:
                raise TypeError

        except:

            logger.warning(
                "[red] :warning: Couldn't get current project. Is a project open in Resolve?[/]"
            )
            utils.app_exit(1, -1)

        try:

            self.timeline = self.project.GetCurrentTimeline()
            if self.timeline is None:
                raise TypeError
        except:

            logger.warning(
                "[red] :warning: Couldn't get current timeline. Is a timeline open in Resolve?[/]"
            )
            utils.app_exit(1, -1)

        try:

            self.media_pool = self.project.GetMediaPool()
            if self.media_pool is None:
                raise TypeError

        except:

            logger.warning("[red] :warning: Couldn't get Resolve's media pool.[/]")
            utils.app_exit(1, -1)
