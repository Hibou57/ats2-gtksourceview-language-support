# ats2-language-support

ATS2 language support and integration
=====================================

Installation on Linux environments
----------------------------------

Not all parts are mandatory, so you may proceed with the only one you want,
as much as with all of the ones. Available parts are:

  * ATS Language definition
  * ATS source file MIME type
  * ATS source file MIME type icon
  * A variant of the Solarized Dark theme as a bonus

The Linux environment is supposed to honnour the *Freedesktop* standard and
to come with the *GtkSourceView* functionnalities (not standard).

The installation is a per‑user installation, as one should avoid trickering in
the system directories (to avoid interference with packages management).

### Installing the language definition

This will provide syntax colourization in `GtkSourceView` based editors.

  * Close any opened *GtkSourceView* based editor (ex. Gedit or Medit or
    Anjuta, are exemples of such)
  * Check the directory `$HOME/.local/share/gtksourceview-3.0/language-specs/`
    exists. If it don't, create it. Copy the file `ats.lang` into your
    `$HOME/.local/share/gtksourceview-3.0/language-specs/`.
  * Open an ATS source file your favorite *GtkSourceView* based editor and
    check the language colourization is applied.

Hint: *Medit* (also known as *MooEdit*) use its own language definitions
directory: `$HOME/.local/share/medit-1/language-specs/`. You will probably
have to copy the file there too if you use this editor.

Hint: the language ID is `ats`, although the language defined is ATS2.

### Installing the MIME type

This will make your file browser aware of ATS(2) source files type.


  * Check the directory `$HOME/.local/share/mime/packages` exists. If it
    don't, create it. Copy the file `ats.xml` into your
    `$HOME/.local/share/mime/packages`.
  * Do either one of these:
     + From a command shell,
       execute `update-mime-database ~/.local/share/mime`
     + Logout from and login back to GUI session.
  * Open your favourite *Freedesktop* aware file browser (ex. Nautilus, as
    an exemple), right‑click (or whatever else) on an ATS source file, and
    in the relevant property tab, check the MIME type is `text/x-ats` and/or
    the file type's description is “ATS program source” (or its available
    translation).

Hint: to have ATS source files associated to a MIME type, allows you to
associated your editor of favour for this kind of file, or any other custom
application.

### Installing the MIME type icon

This will make your file browser and various other application, display
ATS source files with the proper icon, ex. in file browser pane of editor tab.

  * Check the directory `$HOME/.icon` exists. If it don't, create it.
  * Check if there is a or are theme folder(s) in the directory.
  * If there are theme folders, then copy `ats.svg` in each of the `scalable`
    subdirectory of these them folders. If there are no them folders, then
    copy `ats.svg` right in `$HOME/.icon`. CHECKME: could this be an option
    to always copy `ats.svg` right in `$HOME/.icon` even if there are specific
    theme folders?
  * Do either one of these:
     + From a command shell,
       execute `update-icon-caches ~/.icons`, the close and re‑open any
       application displaying files as icons in one way or another.
     + Logout from and login back to GUI session.
  * Open your favourite *Freedesktop* aware file browser (ex. Nautilus, as
    an exemple), get into any directory containing ATS source files, and
    check these source files are displays with the nice ATS icon.

### Installing the bonus Solarized Dark theme variant

This will provide you a slightly modified Solarized Dark color scheme for
*GtkSourceView* editors, named Solarized Dark Alternate.

This will provide syntax colourization in `GtkSourceView` based editors.

  * Close any opened *GtkSourceView* based editor (ex. Gedit or Medit or
    Anjuta, are exemples of such)
  * Check the directory `$HOME/.local/share/gtksourceview-3.0/styles/`
    exists. If it don't, create it. Copy the file `solarized-dark-alt.xml`
    into your `$HOME/.local/share/gtksourceview-3.0/styles/`.
  * Open any source file your favorite *GtkSourceView* based editor, and check
    the alternative theme is available.

Hint: *Medit* (also known as *MooEdit*) use its own style directory:
`$HOME/.local/share/medit-1/language-specs/` (yes, the same as that of
language files). You will probably have to copy the file there too if you use
this editor.

Hint: the reasons why the modification to the Solarized Dark theme were made
and why it may be good (or not) to you, are explained in the file
`solarized-dark-alt.xml` it‑self.
