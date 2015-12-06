ATS2 language support and integration
=====================================
Language support for GTKSourceView and integration in FreeDesktop environements.

Installation on Linux environments
----------------------------------

Not all parts are mandatory, so you may proceed with the only one you want,
as much as with all of the ones. Available parts are:

  * ATS2 Language definition
  * ATS(2) source file MIME type
  * ATS(2) source file MIME type icon
  * A variant of the Solarized Dark theme as a bonus

The Linux environment is supposed to honnour the *Freedesktop* standard and
to come with the *GtkSourceView* functionnalities (not standard).

The installation is a per‑user installation, as one should avoid trickering in
the system directories (to avoid interference with packages management).

### Installing the language definition

This will provide syntax colourization in *GtkSourceView* based editors 
(ex. Gedit or Medit or Anjuta, are exemples of such).

  * Close any opened *GtkSourceView* based editor.
  * Check the directory `$HOME/.local/share/gtksourceview-3.0/language-specs/`
    exists. If it don't, create it. Copy the file `ats.lang` into your
    `$HOME/.local/share/gtksourceview-3.0/language-specs/`.
  * Open an ATS source file in your favorite *GtkSourceView* based editor and
    check the language colourization is applied.

**Hint:** *Medit* (also known as *MooEdit*) uses its own language definitions
directory: `$HOME/.local/share/medit-1/language-specs/`. You will probably
have to copy the file there too if you use this editor.

**Hint:** the language ID is `ats`, although the language defined is ATS2.

### Installing the MIME type

This will make your file browser aware of ATS(2) source files type.

  * Check the directory `$HOME/.local/share/mime/packages` exists. If it
    don't, create it. Copy the file `ats.xml` into your
    `$HOME/.local/share/mime/packages`.
  * Do either one of these:
     + From a command shell,
       execute `update-mime-database ~/.local/share/mime`
     + Logout from and login back to your GUI session.
  * Open your favourite *Freedesktop* aware file browser (ex. Nautilus, as
    an exemple), right‑click (or whatever else) on an ATS source file, and
    in the relevant property tab, check the MIME type is `text/x-ats` and/or
    the file type's description is “ATS program source” (or its available
    translation).

**Hint:** to have ATS source files associated to a MIME type, allows you to
associate your editor of favour for this kind of file, or any other custom
application.

### Installing the MIME type icon

This will make your file browser and various other application, display
ATS source files with the proper icon, ex. in file browser pane of editor tab.

  * Check the directory `$HOME/.icons` exists. If it don't, create it.
  * Check if there is a or are theme folder(s) in the directory.
  * If there are theme folders, then copy `ats.svg` in each of the `scalable`
    subdirectory of these theme folders. If there are no theme folders, then
    copy `ats.svg` right in `$HOME/.icons`. CHECKME: could this be an option
    to always copy `ats.svg` right in `$HOME/.icons` even if there are
    specific theme folders?
  * Do either one of these:
     + From a command shell,
       execute `update-icon-caches ~/.icons`, the close and re‑open any
       application displaying files as icons in one way or another.
     + Logout from and login back to your GUI session.
  * Open your favourite *Freedesktop* aware file browser (ex. Nautilus, as
    an exemple), get into any directory containing ATS source files, and
    check these source files shows with the nice ATS icon.

### Installing the bonus *Solarized Dark* theme variant

This will provide you a slightly modified *Solarized Dark* color scheme for
*GtkSourceView* editors, named *Solarized Dark Alternate*.

  * Close any opened *GtkSourceView* based editor (ex. Gedit or Medit or
    Anjuta, are exemples of such)
  * Check the directory `$HOME/.local/share/gtksourceview-3.0/styles/`
    exists. If it don't, create it. Copy the file `solarized-dark-alt.xml`
    into your `$HOME/.local/share/gtksourceview-3.0/styles/`.
  * Open any source file in your favorite *GtkSourceView* based editor, and
    check the alternative theme is available.

**Hint:** *Medit* (also known as *MooEdit*) uses its own style directory:
`$HOME/.local/share/medit-1/language-specs/` (yes, the same as that of
language files). You will probably have to copy the file there too if you use
this editor.

The reasons why the modifications to the *Solarized Dark* theme, and which 
ones, were made and why it may be good (or not) to you, are explained in the 
file `solarized-dark-alt.xml` it‑self.

Usage notes
-----------

### Triggering colorization for extern blocks

An extern block (any the three forms) may get proper colorization, if it's preceded by a language tag, in the form of a comment.

Ex:

        (*JS*)
        %{
            alert(String(1.0));
        %}

The language tag comment is case-sensitive (see below for tags), must use the `(*…*)` form, and there many be multiple or no spaces/new-lines between it and the token opening the extern block.

Ex. this is as much fine as the above:

        (*JS*) %{ alert(String(1.0)); %}
        
Defined language tags:

  * For C: `ANSI-C` or `C99` or `C` or `ISO-C`.
  * For CIL: `CIL` or `CSharp` or `C-Sharp` or `C#`.
  * For JavaScript: `JS` or `JavaScript` or `EScript` or `ECMAScript` or `ES5`.
  * For PHP: `PHP`.
  * For Perl: `Perl`.
  * For Python: `Python` or `Py` (note the colorization used is that of Python 3).
  
No language tag or an unknow language tag, makes the extern block content be colorized uniformly with the preprocessor color.

### Filtering and reformating ATS messages

There is a format filter to be used with pipes and/or redirection. You will find it as `ats-messages-filter.py`. You may refer to the instruction given in the file it‑self, for usage.
