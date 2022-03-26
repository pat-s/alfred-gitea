#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2015 deanishe@deanishe.net
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2015-10-11
# Source: https://git.deanishe.net/deanishe/alfred-unwatched-videos/src/branch/master
#

"""Generate thumbnails in the background."""

from __future__ import print_function, unicode_literals, absolute_import

import urllib
import logging
import hashlib
import os
import subprocess
import sys

from workflow import Workflow
from workflow.util import LockFile, atomic_writer

log = logging.getLogger(__name__)


class Thumbs(object):
    """Thumbnail generator."""

    def __init__(self, cachedir):
        """Create new ``Thumbs`` object.

        Args:
            cachedir (str): Path to directory to save thumbnails in.
        """
        self._cachedir = os.path.abspath(cachedir)
        self._queue_path = os.path.join(self._cachedir, 'thumbnails.txt')
        self._queue = []

        try:
            os.makedirs(self._cachedir)
        except (IOError, OSError):
            pass

    @property
    def cachedir(self):
        """Where thumbnails are saved.

        Returns:
            str: Directory path.
        """
        return self._cachedir

    def thumbnail_path(self, img_path):
        """Return appropriate path for thumbnail.

        Args:
            img_path (str): Path to image file.

        Returns:
            str: Path to thumbnail.
        """
        if isinstance(img_path, unicode):
            img_path = img_path.encode('utf-8')
        elif not isinstance(img_path, str):
            img_path = str(img_path)

        h = hashlib.md5(img_path).hexdigest()
        dirpath = os.path.join(self.cachedir, h[:2], h[2:4])
        thumb_path = os.path.join(dirpath, u'{}.png'.format(h))
        return thumb_path

    def thumbnail(self, img_path):
        """Return resized thumbnail for ``img_path``.

        Args:
            img_path (str): Path to original images.

        Returns:
            str: Path to thumbnail image.
        """
        thumb_path = self.thumbnail_path(img_path)

        if os.path.exists(thumb_path):
            return thumb_path
        else:
            self.queue_thumbnail(img_path)
            return None

    def queue_thumbnail(self, img_path):
        """Add ``img_path`` to queue for later thumbnail generation.

        Args:
            img_path (str): Path to image file.
        """
        self._queue.append(img_path)

    def save_queue(self):
        """Save queued files."""
        if not self._queue:
            return

        text = []
        for p in self._queue:
            if isinstance(p, unicode):
                p = p.encode('utf-8')
            text.append(p)
            log.debug('Queued for thumbnail generation : %r', p)

        text = b'\n'.join(text)
        with LockFile(self._queue_path):
            with atomic_writer(self._queue_path, 'ab') as fp:
                fp.write(b'{}\n'.format(text))

        self._queue = []

    @property
    def has_queue(self):
        """Whether any files are queued for thumbnail generation.

        Returns:
            bool: ``True`` if there's a queue.
        """
        return (os.path.exists(self._queue_path) and
                os.path.getsize(self._queue_path) > 0)

    def process_queue(self):
        """Generate thumbnails for queued files."""
        if not self.has_queue:
            log.debug('Thumbnail queue empty.')
            return

        queue = []
        with LockFile(self._queue_path):
            with open(self._queue_path) as fp:
                for line in fp:
                    line = line.strip()
                    if not line:
                        continue
                    queue.append(line)
            with atomic_writer(self._queue_path, 'wb') as fp:
                fp.write('')

        succeeded = True
        for i, img_path in enumerate(queue):
            log.debug('Generating thumbnail %d/%d ...', i + 1, len(queue))
            if not self.generate_thumbnail(img_path):
                succeeded = False

        return succeeded

    def generate_thumbnail(self, img_path):
        """Generate and save thumbnail for ``img_path``.

        Args:
            img_path (str): Path to image file.

        Returns:
            bool: ``True`` if generation succeeded, else ``False``.
        """
        thumb_path = self.thumbnail_path(img_path)
        dirpath = os.path.dirname(thumb_path)
        try:
            os.makedirs(dirpath)
        except OSError:
            pass

        urllib.urlretrieve(img_path, thumb_path)

        log.debug('Wrote thumbnail for `%s` to `%s`.', img_path, thumb_path)

        return True


def main(wf):
    """Generate any thumbnails pending in the queue.

    Args:
        wf (Workflow): Current workflow instance.
    """
    t = Thumbs(wf.datafile('thumbs'))
    t.process_queue()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
