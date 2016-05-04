"""Test the testing functions."""

from __future__ import absolute_import
from __future__ import print_function

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

    def test_returning_function(self):
        """Test a function that returns."""

        self.assertEqual(
            self.fork_output(
                lambda: print("asdf"),
            ),
            "asdf\n"
        )

    def test_exception(self):
        """Test a function that raises an exception."""

        def raise_exception():
            """Raise a test exception."""
            raise Exception("asdf")

        self.assertIn(
            "Exception: asdf",
            self.fork_output(raise_exception),
        )
