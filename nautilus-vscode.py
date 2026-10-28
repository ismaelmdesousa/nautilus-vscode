# SPDX-License-Identifier: MIT
# MIT License
#
# Copyright (c) 2026 Ismael M. de Sousa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gettext
import subprocess
from pathlib import Path

from gi.repository import Gio, GObject, Nautilus


translation = gettext.translation(
    "nautilus-vscode",
    localedir=Path(__file__).resolve().parent / "locale",
    fallback=True,
)
_ = translation.gettext


class OpenVSCode(GObject.GObject, Nautilus.MenuProvider):
    def open_folder(self, item, path):
        subprocess.Popen(["code", "--new-window", path])

    def create_item(self, folder, identifier):
        if not folder.is_directory():
            return []

        path = Gio.File.new_for_uri(folder.get_uri()).get_path()
        if path is None:
            return []

        item = Nautilus.MenuItem(
            name=identifier,
            label=_("Open in VS Code"),
            tip=_("Open this folder in Visual Studio Code"),
        )
        item.connect("activate", self.open_folder, path)
        return [item]

    def get_file_items(self, files):
        if len(files) != 1:
            return []
        return self.create_item(files[0], "OpenVSCode::folder")

    def get_background_items(self, folder):
        return self.create_item(folder, "OpenVSCode::background")
