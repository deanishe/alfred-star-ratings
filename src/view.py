#!/usr/bin/python
# encoding: utf-8
#
# Copyright © 2015 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2015-10-08
#

"""
Alfred 2 Script Filter. Shows the ratings of files selected in Finder.
"""

from __future__ import print_function, unicode_literals, absolute_import

import os
import subprocess
import sys

from rate import get_rating
from workflow import Workflow, ICON_WARNING

log = None

AS_FINDER_SELECTION = b"""
tell application "Finder"
    set pathList to {}
    set theSelection to the selection
    -- log ((count of theSelection) as text) & " items selected"
    repeat with theItem in theSelection
        set the end of pathList to POSIX path of (theItem as alias)
    end repeat
    log pathList
    return my joinArray(pathList, linefeed)
end tell

-- Return a string of theArray joined with theDelimiter
on joinArray(theArray, theDelimiter)
    set theString to ""
    -- Save default delimiters
    set oldDelim to AppleScript's text item delimiters
    repeat with theItem in theArray
        if theString = "" then
            set theString to theString & theItem
        else
            set theString to theString & theDelimiter & theItem
        end if
    end repeat
    -- Restore delimiters
    set AppleScript's text item delimiters to oldDelim
    return theString
end joinArray
"""

ICONS_RATING = {
    0: 'icons/0_stars.png',
    1: 'icons/1_star.png',
    2: 'icons/2_stars.png',
    3: 'icons/3_stars.png',
    4: 'icons/4_stars.png',
    5: 'icons/5_stars.png',
}
ICON_ERROR = 'icons/error.png'
ICON_UNRATED = 'icons/unrated.png'


def finder_selection():
    """Return list of files selected in Finder."""
    cmd = [b'osascript', b'-e', AS_FINDER_SELECTION]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if err:
        log.debug('osascript STDERR: {0!r}'.format(err))

    if proc.returncode != 0:
        raise IOError('osascript exited with status {0}'.format(
                      proc.returncode))

    out = wf.decode(out.strip())
    if not out:
        return []

    return out.split('\n')


def main(wf):
    """Run Script Filter."""

    query = wf.args[0]
    # Cache Finder selection for a few seconds. This should stop
    # it being re-fetched for the duration of the workflow's use
    selection = wf.cached_data('selection', finder_selection, max_age=5)

    for path in selection:
        log.debug('Selected : {0}'.format(path))

    if not selection:
        wf.add_item('Nothing selected.',
                    'Select some files in Finder and run again.',
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0

    # ---------------------------------------------------------
    # Filter results
    if query:
        selection = wf.filter(query, selection,
                              key=os.path.basename, min_score=30)

    if not selection:
        wf.add_item('No matches',
                    'Try a different query.',
                    icon=ICON_WARNING)

    # ---------------------------------------------------------
    # Display results
    home = os.path.expanduser('~/')
    for path in selection:
        try:
            rating = get_rating(path)
        except IOError as err:
            log.error(err)
            icon = ICON_ERROR
        else:
            if rating is not None:
                rating = int(rating)
            icon = ICONS_RATING.get(rating, ICON_UNRATED)

        # Strip trailing slash from directories, otherwise
        # Python returns an empty basename
        basename = os.path.basename(path.rstrip('/'))
        wf.add_item(basename,
                    path.replace(home, '~'),
                    arg=path,
                    uid=path,
                    type='file',
                    icon=icon)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
