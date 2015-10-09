#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2015 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2015-10-08
#

"""rate.py [options] <file>...

Show and set OS X star ratings on files and folders.

Rating must be a number between 0.0 and 5.0.

Usage:
    rate.py [-r <rating>] <file>...
    rate.py -c <file>...
    rate.py (-h|-v)

Options:
    -c, --clear            Remove rating metadata.
    -r, --rating=<rating>  The rating to apply to files.
    -v, --version          Print the version number and exit.

"""

from __future__ import print_function, unicode_literals, absolute_import

from ctypes import (
    cdll,
    create_string_buffer,
    c_char_p,
    c_float,
    c_uint64,
    sizeof,
    util,
)
import os
import sys

from biplist import readPlistFromString, writePlistToString
from docopt import docopt


__version__ = open(os.path.join(os.path.dirname(__file__), 'version')).read()
__author__ = 'Dean Jackson <deanishe@deanishe.net>'

RATING_KEY = 'com.apple.metadata:kMDItemStarRating'
RATING_KEY_C = c_char_p(RATING_KEY.encode('utf-8'))

xattr = cdll.LoadLibrary(util.find_library('xattr'))


def log(*args):
    """Log message to STDERR.

    Args:
        *args: Values to print.

    """

    print(' '.join(args), file=sys.stderr)


def c_path(path):
    """Convert `path` to `c_char_p`.

    Args:
        path (unicode): Filepath

    Returns:
        c_char_p: Encoded filepath

    """

    if isinstance(path, unicode):
        path = path.encode('utf-8')

    return c_char_p(path)


def clear_rating(path):
    """Remove rating metadata from `path`.

    Args:
        path (unicode): File whose rating to remove.

    Raises:
        IOError: Raised if `removexattr` call fails.

    """

    p = c_path(path)
    size = xattr.getxattr(p, RATING_KEY_C, None, 0, 0, 0)
    if size == -1:  # No rating set
        return None

    success = xattr.removexattr(p, RATING_KEY_C, 0)

    if success == -1:
        raise IOError('removexattr failed for path `{}`'.format(path))


def get_rating(path):
    """Get star rating for `path`.

    Args:
        path (unicode): File whose rating to retrieve.

    Raises:
        IOError: Raised if call to `getxattr` fails.

    Returns:
        float or None: Star rating of `path`.

    """

    p = c_path(path)
    size = xattr.getxattr(p, RATING_KEY_C, None, 0, 0, 0)
    if size == -1:  # No rating set
        return None

    buf = create_string_buffer(size)
    success = xattr.getxattr(p, RATING_KEY_C, buf, c_uint64(size), 0, 0)

    if success == -1:
        raise IOError('getxattr failed for path `{}`'.format(path))

    # print('got raw rating : {!r}'.format(buf.raw))
    return readPlistFromString(buf.raw)


def set_rating(path, rating):
    """Set star rating of `path` to `rating`.

    Args:
        path (unicode): File whose rating to set.
        rating (float): Star rating between 0.0 and 5.0.

    Raises:
        IOError: Raised if `setxattr` call fails.

    """

    p = c_path(path)
    bplist = writePlistToString(rating)
    size = c_uint64(len(bplist))
    success = xattr.setxattr(p, RATING_KEY_C, bplist, size, 0, 0)
    if success == -1:
        raise IOError('setxattr failed for path `{}`'.format(path))


def do_list_ratings(filepaths):
    """Print ratings of `filepaths` to STDOUT.

    Args:
        filepaths (list): Files whose ratings to print.

    Returns:
        int: 0 or 1 on failure.

    """

    retcode = 0

    for path in filepaths:
        if not os.path.exists(path):
            log('ERROR: Path does not exist : {}'.format(path))
            retcode = 1
            continue

        try:
            rating = get_rating(path)
        except IOError as err:
            log('ERROR: {}'.format(err))
            retcode = 1
            continue

        print('{}\t{}'.format(rating, path))

    return retcode


def do_clear_ratings(filepaths):
    """Remove ratings of `filepaths`.

    Args:
        filepaths (list): Files whose ratings to print.

    Returns:
        int: 0 or 1 on failure.

    """

    retcode = 0

    for path in filepaths:
        if not os.path.exists(path):
            log('ERROR: Path does not exist : {}'.format(path))
            retcode = 1
            continue

        try:
            clear_rating(path)
        except IOError as err:
            log('ERROR: {}'.format(err))
            retcode = 1
            continue

    return retcode


def main():
    """Run script.

    Raises:
        ValueError: Raised if rating is invalid.

    Returns:
        int: 0 on success, 1 on failure

    """

    args = docopt(__doc__, version=__version__)

    rating = args.get('--rating')
    filepaths = [s.decode('utf-8') for s in args.get('<file>')]

    if args.get('--clear'):
        return do_clear_ratings(filepaths)

    if rating is None:
        return do_list_ratings(filepaths)

    rating = float(rating)

    if rating < 0.0 or rating > 5.0:
        raise ValueError(
            'Invalid rating : {}. Must be between 0.0 and 5.0.'.format(rating))

    retcode = 0

    for path in filepaths:
        try:
            set_rating(path, rating)
        except IOError as err:
            log('ERROR: {}'.format(err))
            retcode = 1

    return retcode

if __name__ == '__main__':
    sys.exit(main())
