# nautilus-vscode

**English** | [Português brasileiro](README.pt-BR.md)

A Nautilus (GNOME Files) extension that adds **Open in VS Code** to the
context menu of a folder and to the background context menu inside the
current folder. It opens the folder in a new Visual Studio Code window.

## Requirements

- Debian with GNOME and Nautilus 43 or later.
- Visual Studio Code with the `code` command available in the Nautilus environment.
- Python extension support for Nautilus:

```bash
sudo apt install python3-nautilus
```

Check that the editor command is available:

```bash
command -v code
```

The extension supports local folders. Remote folders, such as `smb://` and
`sftp://` locations, do not show the menu item.

## Tested environment

The author manually tested the system-wide installation in
`/usr/share/nautilus-python/extensions/` on the following environment:

| Component | Version |
| --- | --- |
| Debian GNU/Linux | 13.7 (trixie) |
| GNOME Shell | 48.7 |
| Nautilus (Files) | 48.3 |
| python3-nautilus | 4.0.1 |

These versions were read from the current test environment's system metadata
and installed packages.

## Installation

Run these commands from the root of this repository. Choose one of the
installation options below to avoid loading two copies of the extension.
The Python file does not need to be executable.

### Compile translations

Install the tool and compile all translation catalogs before copying the files:

```bash
sudo apt install gettext
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    mkdir -p "locale/$language/LC_MESSAGES"
    msgfmt --check "$catalog" -o "locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
```

### Current user only

The default directory is `~/.local/share/nautilus-python/extensions/`.
If `XDG_DATA_HOME` is set, use it instead of `~/.local/share`.

```bash
install -Dm644 nautilus-vscode.py "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/nautilus-vscode.py"
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    install -Dm644 "locale/$language/LC_MESSAGES/nautilus-vscode.mo" "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
```

### System-wide, for all users

On Debian, install into `/usr/share/nautilus-python/extensions/`:

```bash
sudo install -Dm644 nautilus-vscode.py /usr/share/nautilus-python/extensions/nautilus-vscode.py
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    sudo install -Dm644 "locale/$language/LC_MESSAGES/nautilus-vscode.mo" "/usr/share/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
```

The author has manually tested the system-wide installation in GNOME/Nautilus.
Each user must have access to the `code` command in their session.

### Load the extension

After installing or updating, quit Nautilus:

```bash
nautilus -q
```

Open **Files** again. For a system-wide installation, each user needs to
restart their own Nautilus process to load the extension.

## Usage and verification

1. Right-click a local folder.
2. Select **Open in VS Code** and check that the folder opens in a new window.
3. Open a folder, right-click an empty area, and repeat.

The item appears when a single folder is selected or in the background
context menu. It does not appear for files or multiple selected folders.
Nautilus determines the position of the item.

The extension does not change the default application for folders or require
VS Code to be associated with the `inode/directory` MIME type.

## Updating

Recompile the translations and copy the `.py` and `.mo` files using the
commands for your chosen installation. Restart Nautilus with `nautilus -q`.

## Uninstallation

### User installation

```bash
rm -- "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/nautilus-vscode.py"
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    rm -f -- "${XDG_DATA_HOME:-$HOME/.local/share}/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
nautilus -q
```

### System-wide installation

```bash
sudo rm -- /usr/share/nautilus-python/extensions/nautilus-vscode.py
for catalog in po/*.po; do
    language=$(basename "$catalog" .po)
    sudo rm -f -- "/usr/share/nautilus-python/extensions/locale/$language/LC_MESSAGES/nautilus-vscode.mo"
done
nautilus -q
```

## Troubleshooting

If the item does not appear, check that `python3-nautilus` is installed,
that the file was copied to the chosen directory, and that Nautilus has
been restarted. Also confirm that the folder is local.

If the item appears but the editor does not open, try this in a terminal:

```bash
code --new-window /path/to/folder
```

If the command only works through a shell alias or shell configuration,
make the `code` executable available in the graphical session's `PATH`.

## Languages and translation

`gettext` selects the translation from the Nautilus process environment,
checking `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, and `LANG` in that order.
English is the original language. The following translation catalogs are available:

| Language | Catalog |
| --- | --- |
| Arabic | `ar` |
| Bengali | `bn` |
| Brazilian Portuguese | `pt_BR` |
| French | `fr` |
| Hindi | `hi` |
| Indonesian | `id` |
| Simplified Chinese (Mandarin) | `zh_CN` |
| Spanish | `es` |
| Urdu | `ur` |

If no catalog is available for the selected language, the menu appears in English.
After changing the session language, restart Nautilus to reload the translation.

The `po/*.po` files contain the editable translations. The `.mo` files
are compiled catalogs and must be installed in the `locale` directory next
to the extension. They are generated locally and ignored by Git.

To add a language, extract the messages and create a catalog (German in
this example):

```bash
xgettext --language=Python --from-code=UTF-8 --keyword=_ --package-name=nautilus-vscode -o /tmp/nautilus-vscode.pot nautilus-vscode.py
msginit --no-translator --locale=de --input=/tmp/nautilus-vscode.pot --output-file=po/de.po
```

Translate the `msgstr` entries in `po/de.po`, compile with `msgfmt --check`,
and install into `locale/de/LC_MESSAGES/nautilus-vscode.mo`, following the
same installation steps as the existing catalogs.

## Development validation

To check the syntax without opening the editor:

```bash
python3 -m py_compile nautilus-vscode.py
git diff --check
```

This check does not replace manually testing the menu in Nautilus.

## Documentation

See the [official nautilus-python reference manual](https://gnome.pages.gitlab.gnome.org/nautilus-python/) for the
extension API, including `Nautilus.MenuProvider` and `Nautilus.MenuItem`.

## License

MIT; see [LICENSE](LICENSE). The full license text is also included in the
header of `nautilus-vscode.py` so that it accompanies installations that copy
only that file. There is no need to install `LICENSE` separately into the
extension directories.
