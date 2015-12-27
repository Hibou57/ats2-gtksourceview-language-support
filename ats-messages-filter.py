#!/usr/bin/env python3
# -*- coding:utf-8; mode:python3; indent-tabs-mode:nil; c-basic-offset:4; -*-

"""Filter and reformat ATS messages, to suite typical editors messages pan.

Note: as of 2015 December, this filter is considered obsolete, and it is 
suggested to use the one provide in this repository, instead: 
[PostiATS-Utilities](https://github.com/Hibou57/PostiATS-Utilities).

To use this, ensure you have a Python 3 interpreter available, move this
file somewhere accessible according to your `${PATH}` and give this file the
executable attribute. Optionally, remove the `*.py` extensions to make it more
look like a typical command.

It's an `stdin` filter, reformating ATS messages received on input as follow:

  * `filename: N(line=N, offs=N) -- N(line=N, offs=N)` gets changed into
    `relative-filename:#line:#column:`.
  * Messages are indented under the heading giving the location (see above).
  * Message are split into lines using the `: ` separator (using same indent).
  * `name$N$N(N);` are changed into `name;`.
  * `Var(N)` are changed into `Var(?)` (a question mark, literally).
  * Showtype messages are formated as regular message with location.
  * The repository path prefix which appears in some name, like ATS
    exceptions, is collapsed as `[…]`.


Relative-filename: it is made relative to the current working directory, to be
shorter. If the filter output is to be used in a text editor's location pan
and that location pan has issue with relative filenames, set the
`USE_RELATIVE_FILENAMES` configuration variable below, to `False`.

Variable numeric IDs: note some numeric IDs may remains, as not all can be
removed, because ATS may return integer literals in message too. So and
occasionnaly, some numbers which are not integer literals will remain.

Multiline split: a message like “error(3): something wrong: more.” is turned
into this:

        relative-filename:N:N:
           error(3):
           something wrong:
           more.

It's also useful with messages from `showtype`, which will display the type on
its line and the sort on the line below (as type and sort are `: ` separated).

Every `_2home_2hwxi_2research_2Postiats_2git_2src_2pats` is replaced with
`[…]`, to make messages shorter. If you need to avoid this to keep exact
references in case of errors, either re-run the compiler not using this filter
or set the `COLLAPSE_REP_PREFIX` configuration variable below to `False`.

The default indent is 3 white spaces. You may change it by editing the
`INDENT` configuration variable below. Its expected value is a string, not
a number of white-spaces.

Keep in mind some message from ATS goes to `stdout` while some others goes
to `stderr`. You may redirecto `stderr` to `stdout` and filter all like this,
but some editor message pans display message using a distinct style for
errors, so that may be better to separate both. Doing so, check the output
of the filter is redirected to the intended stream (either `stdout` or
`stderr`).

Also keep in mind using a pipe does not provide access to the exit status
of anything but the last command in the pipe. ATS makes uses of exit status.
If you want to check ATS status, don't pipe directly to the filter, and
use an intermediate file instead. Please, find an example below.

Example SH script making use of this filter:

        #!/bin/sh

        NAME=$(basename "$1" ".dats")
        STDOUT_FILE="output/output.txt"
        STDERR_FILE="output/errors.txt"

        echo "PATSOPT $NAME";
        patsopt \
           --output "output/$NAME.c" \
           --dynamic "$NAME.dats" \
           1>"$STDOUT_FILE" \
           2>"$STDERR_FILE";
        STATUS=$?;
        ats-messages-filter <"$STDERR_FILE" >&2;
        ats-messages-filter <"$STDOUT_FILE" >&1;
        if [ $STATUS -ne 0 ]; then
           exit $STATUS;
        fi;

        echo "ATSCC2JS $NAME";
        atscc2js \
           --output "output/$NAME.js" \
           --input "output/$NAME.c" \
           1>"$STDOUT_FILE" \
           2>"$STDERR_FILE";
        STATUS=$?;
        ats-messages-filter <"$STDERR_FILE" >&2;
        ats-messages-filter <"$STDOUT_FILE" >&1;
        if [ $STATUS -ne 0 ]; then
           exit $STATUS;
        fi;

"""

USE_RELATIVE_FILENAMES = True
COLLAPSE_REP_PREFIX = True
INDENT = "   "


# Imports
# ============================================================================
import os.path
import sys


# Functions
# ============================================================================
DECIMALS = "0123456789"


# Locations
# ----------------------------------------------------------------------------
def get_number(string):
    """Get decimal number in `string` prefix.

    Result: (value, tail)

    Value is None if no number could be read, in which case tail is just
    `string`, otherwise value is a number and tail is the tail of `string`
    after the number which was parsed.

    Helper for `get_location`.

    """
    index = 0
    number_image = ""
    len_string = len(string)
    while index < len_string and string[index] in DECIMALS:
        number_image += string[index]
        index += 1
    if number_image == "":
        result = (None, string)
    else:
        result = (int(number_image), string[index:])
    return result


def checked_prefix(string, prefix):
    """Check if `string` has the prefix.

    Result: (status, tail)

    Status is `False` if `string` does not start with `prefix`, in which case
    tail is just `string`, otherwise status is `True` and tail is the tail of
    `string` after `prefix`.

    Helper for `get_location` and `reformated_located_message`.

    """
    if string.startswith(prefix):
        result = (True, string[len(prefix):])
    else:
        result = (False, string)
    return result


def get_location(string):
    """Get location at string prefix.

    Result: (value, tail)

    Value is `None` if no location could be parsed, in which case tail is just
    `string`, otherwise value is a tuple of line‑no and column‑no where
    line‑no and column‑no are numbers, and tail is the tail of `string` after
    the location which was parsed.

    The location parsed includes a raw byte offset (not character offset), but
    it is ignored and not returned in the tuple.

    The location parsed is of the form `N(line=N, offs=N)`, where N are
    decimal numbers (the raw byte offset is the first N). `offs=N` gives the
    column number (its an offset in the line).

    Note patsopt/patscc/patscc2js are not Unicode aware. It does not matter
    with line numbers, but it may matters with column numbers, which may be
    innacurate if a column number is after a multi‑byte character. Exactly,
    the column‑number will be too big. As multi‑byte characters may only occur
    in comments, it will matter only whenever there are comments inside of ATS
    expressions, and these comments contains multi‑byte characters. This is
    expected to be rare, but not impossible.

    """
    tail = string
    ok = True
    if ok:
        (ignored, tail) = get_number(tail)
        ok = ignored is not None
    if ok:
        (ok, tail) = checked_prefix(tail, "(line=")
    if ok:
        (line_number, tail) = get_number(tail)
        ok = line_number is not None
    if ok:
        (ok, tail) = checked_prefix(tail, ", offs=")
    if ok:
        (column_number, tail) = get_number(tail)
        ok = column_number is not None
    if ok:
        (ok, tail) = checked_prefix(tail, ")")
    if ok:
        result = ((line_number, column_number), tail)
    else:
        result = (None, string)
    return result


# Reformated message
# ----------------------------------------------------------------------------
CWD = os.path.join(os.getcwd(), "")


def get_filename(string):
    """Get filename at `string prefix`, colon terminated.

    Result: (value, tail)

    Value is `None` if no filename could be parsed, in which case tail is just
    `string`, otherwise value is the filename and tail is the tail of `string`
    after the filename which was parsed.

    The filename may be empty (it happens with patscc2js), so it will return
    an empty filename if `string` readily starts with a colon.

    Helper for `reformated_located_message`.

    """
    index = string.find(":")
    if index == -1:
        result = (None, string)
    else:
        result = (string[:index], string[index+1:])
    return result


def filename_made_relative(filename):
    """Filename made shorter, relative to the startup wording directory."""
    if filename == "":
        result = ""
    else:
        result = os.path.relpath(filename, start=CWD)
    return result


def reformated_located_message(string):
    """`filename: N(line=N, offs=N) -- N(line=N, offs=N): message` reformated.

    Result: new‑string or `None`

    If `string` is not of the expected form, `None` is returned, otherwise
    returns `path:line‑no:column‑no: message`, where line‑no and column‑no are
    decimal numbers and where message will contain new-line characters and
    added indents.

    """
    tail = string
    ok = True
    if ok:
        (filename, tail) = get_filename(tail)
        ok = filename is not None
    if ok:
        (ok, tail) = checked_prefix(tail, " ")
    if ok:
        (lc, tail) = get_location(tail)
        ok = lc is not None
    if ok:
        (ok, tail) = checked_prefix(tail, " -- ")
    if ok:
        (ignored, tail) = get_location(tail)
        ok = ignored is not None
    if ok:
        (ok, tail) = checked_prefix(tail, ": ")
    if ok:
        message = tail.strip()
        messages = message.split(": ")
        # pylint: disable=unpacking-non-sequence
        # PyLint does not see lc is not None.
        (line_number, column_number) = lc
        separator = ":\n" + INDENT
        if USE_RELATIVE_FILENAMES:
            filename = filename_made_relative(filename)
        result = (
            filename
            + ":"
            + str(line_number)
            + ":"
            + str(column_number)
            + separator
            + separator.join(messages))
    else:
        result = None
    return result


# `_2home_2hwxi_2research_2Postiats_2git_2src_2pats` prefix
# ----------------------------------------------------------------------------
REP_DIR = "_2home_2hwxi_2research_2Postiats_2git_2src_2pats"


def repository_prefix_collapsed(line):
    """`_2home_…_2git_2src_2pats` replaced with `[…]`."""
    if COLLAPSE_REP_PREFIX:
        result = line.replace(REP_DIR, "[…]")
    else:
        result = line
    return result


# Showtype location
# ----------------------------------------------------------------------------
SHOWTYPE_PREFIX = "**SHOWTYPE[UP]**("
SHOWTYPE_SUFFIX = "): "


def showtype_location_promoted(line):
    """Promote the location wrapped in `**SHOWTYPE[UP]**(…)`.

    The wrapping text is also removed.

    This make the message suitable for reformating with
    `reformated_located_message`.

    """
    if line.startswith(SHOWTYPE_PREFIX):
        index = line.find(SHOWTYPE_SUFFIX)
        if index != 1:
            location = line[len(SHOWTYPE_PREFIX):index]
            message = line[index+len(SHOWTYPE_SUFFIX):]
            result = location + ": " + message
        else:
            result = line
    else:
        result = line
    return result


# IDS of variables
# ----------------------------------------------------------------------------
def variable_id_end(line, index):
    """Return the end of a variable ID starting at index.

    If there is no variable ID at index, `None` is returned.

    Helper for `variable_ids_erased`.

    """
    # $N…$N(N)
    end = None
    j = index
    if line[j] == "$" and line[j+1] in DECIMALS:
        while line[j] == "$" and line[j+1] in DECIMALS:
            j += 1
            while line[j] in DECIMALS:
                j += 1
        if line[j] == "(" and line[j+1] in DECIMALS:
            j += 1
            while line[j] in DECIMALS:
                j += 1
            if line[j] == ")":
                j += 1
                end = j
    return end


def variable_ids_erased(line):
    """Erase all variables numeric IDs, to left the names alone."""
    start = 0
    result = line
    while start < len(result):
        end = variable_id_end(result, start)
        if end is not None:
            result = result[:start] + result[end:]
        else:
            start += 1
    return result


# Variables as number
# ----------------------------------------------------------------------------
VAR_PREFIX = "Var("
LEN_VAR_PREFIX = len(VAR_PREFIX)


def variable_number_end(line, index):
    """Return the end of a variable number in `line` starting at `index`.

    If there is no variable number at `index`, `None` is returned.

    Helper for `variable_numbers_substituted`.

    """
    # Var(N)
    end = None
    j = index
    if (line[j:j+LEN_VAR_PREFIX] == VAR_PREFIX
            and line[j+LEN_VAR_PREFIX] in DECIMALS):
        j += LEN_VAR_PREFIX
        while line[j] in DECIMALS:
            j += 1
        if line[j] == ")":
            j += 1
            end = j
    return end


def variable_numbers_substituted(line):
    """All `Var(N)` substituted with `Var(?)`."""
    start = 0
    result = line
    while start < len(result):
        end = variable_number_end(result, start)
        if end is not None:
            result = result[:start] + "Var(?)" + result[end:]
        else:
            start += 1
    return result


# Main
# ============================================================================
def main():
    """Read from `stdin`, reformat and write to `stdout`."""
    for line in sys.stdin:
        line = repository_prefix_collapsed(line)
        line = showtype_location_promoted(line)
        line = variable_ids_erased(line)
        line = variable_numbers_substituted(line)
        new_message = reformated_located_message(line)
        if new_message is not None:
            print(new_message, flush=True)
        else:
            print(line, flush=True)


# Entry point
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()


# ============================================================================
# EOT
