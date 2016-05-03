"""Test the testing functions."""

from __future__ import absolute_import

import os

from .base import ForkOutputTest


class TestForkOutputTest(ForkOutputTest):
    """Test the output test."""

    def test_fork_output(self):
        """Test fork_output."""

        self.assertEqual(
            self.fork_output(
                lambda: os.execl('/bin/echo', '/bin/echo', "asdf"),
            ),
            "asdf\n"
        )
