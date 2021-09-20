from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QCheckBox,
)
from PyQt5.QtGui import QIcon, QFont
import sys
from pathlib import Path
from appdirs import user_data_dir
from argparse import ArgumentParser
from subprocess import Popen
import logging
import os
from platform import system, release
from shutil import copyfile, rmtree
import shutil
import os


def _mkdir(newdir):
    """works the way a good mkdir should :)
    - already exists, silently complete
    - regular file in the way, raise an exception
    - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError(
            "a file with the same name as the desired "
            "dir, '%s', already exists." % newdir
        )
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            _mkdir(head)
        # print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)


def copytree(src, dst, symlinks=False):
    """Recursively copy a directory tree using copy2().

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.

    XXX Consider this example code rather than the ultimate tool.

    """
    names = os.listdir(src)
    # os.makedirs(dst)
    _mkdir(dst)  # XXX
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Exception as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass


# ensure the user is not running windows vista
if system() == "Windows" and int(release()) < 7:
    sys.exit("Windows Vista or lower is not supported!")
elif system() != "Windows":
    sys.exit("This program is only for Windows!")

FROZEN = getattr(sys, "frozen", False)

if FROZEN:
    # we are running in a bundle
    bundle_dir = Path(sys._MEIPASS)
else:
    # we are running in a normal Python environment
    bundle_dir = Path(__file__).parent

install_dir = Path(user_data_dir("Random Person Generator", "C_ffeeStain"))

if not install_dir.exists():
    install_dir.mkdir(parents=True)

with open(bundle_dir / "install/VERSION") as f:
    app_version = f.readlines()[1].strip()

if FROZEN:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s :: %(message)s",
        filename=str(install_dir / "installer.log"),
    )
else:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s :: %(message)s",
        filename="installer.log",
    )

logger = logging.getLogger(__name__)

logger.debug("Starting installer version {}...".format(app_version))

# add command line arguments
arg_parser = ArgumentParser(description="Installer for Random Person Generator")
arg_parser.add_argument(
    "--update",
    action="store_true",
    help="Update the application instead of installing it",
)
arguments = arg_parser.parse_args()


class Installer(QMainWindow):
    """Installs the main program."""

    def install(self):
        if arguments.update:
            logger.warn("Auto-update not implemented yet!")
            # TODO: add update code
            sys.exit(1)
        logger.debug("Installing...")
        if FROZEN:
            logger.debug("Copying files...")
            # copy the files
            os.mkdir(str(install_dir / "information"))
            for file in bundle_dir.glob("information/*"):
                logger.debug("Copying '{}'...".format(file))
                copyfile(str(file), str(install_dir / file.name))
            # run pyinstaller on main.py in the bundle folder
            logger.debug("Running pyinstaller...")
            Popen(
                [
                    '"./pyinstaller.exe"',
                    f"{bundle_dir / 'main.spec'}",
                ]
            ).wait()
            # copy the executable's folder
            logger.debug("Copying executable...")
            copyfile(
                str(bundle_dir / "dist" / "main.exe"),
                str(install_dir / "main.exe"),
            )
            # delete the old folders
            logger.debug("Deleting old folders...")
            rmtree(str(bundle_dir / "dist"))
            rmtree(str(bundle_dir / "build"))

            logger.debug("Done!")

    def browse_install_path(self, _):
        """Opens a file dialog to select the install path."""
        path = QFileDialog.getExistingDirectory(
            self, "Select install directory", str(install_dir)
        )
        if path:
            self.install_path_edit.setText(path)

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        logger.debug("Initializing installer window...")

        self.setWindowTitle("Program Installer")
        self.setWindowIcon(QIcon(str(bundle_dir / "icon.png")))
        self.setFixedSize(400, 225)
        self.center()
        self.setFont(QFont("Arial", 8))

        self.title = QLabel("Random Person Generator - Installer", self)
        self.title.setFont(QFont("Arial", 14))
        self.title.adjustSize()
        self.title.move(int(self.width() / 2 - self.title.width() / 2), 10)

        self.install_path_label = QLabel("Install Path:", self)
        self.install_path_label.move(20, 45)

        self.install_path_edit = QLineEdit(self)
        self.install_path_edit.move(80, 50)
        self.install_path_edit.setFixedWidth(300)
        self.install_path_edit.setFixedHeight(20)
        self.install_path_edit.setText(str(install_dir))
        self.install_path_edit.setStyleSheet("color: grey;")
        self.install_path_edit.setReadOnly(True)

        self.install_path_browse_button = QPushButton("Browse", self)
        self.install_path_browse_button.setFont(QFont("Arial", 8))
        self.install_path_browse_button.adjustSize()
        self.install_path_browse_button.move(
            int(
                self.install_path_edit.x()
                + self.install_path_edit.width() / 2
                - self.install_path_browse_button.width() / 2
            ),
            int(self.install_path_edit.y() + self.install_path_edit.height() + 5),
        )
        self.install_path_browse_button.clicked.connect(self.browse_install_path)

        self.add_shortcut = QCheckBox("Add shortcut to desktop", self)
        self.add_shortcut.adjustSize()
        self.add_shortcut.move(20, 110)

        self.add_to_start_menu = QCheckBox("Add to Start Menu", self)
        self.add_to_start_menu.adjustSize()
        self.add_to_start_menu.move(20, 140)

        self.install_button = QPushButton("Install", self)
        self.install_button.adjustSize()
        self.install_button.clicked.connect(self.install)
        self.install_button.move(
            int(self.width() / 2 - self.install_button.width() / 2),
            self.height() - self.install_button.height() - 20,
        )

    def center(self):
        """Centers the window on the screen."""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
installer = Installer(None)
installer.show()
sys.exit(app.exec_())
