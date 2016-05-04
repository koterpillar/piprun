"""Test piprun."""

from __future__ import absolute_import

import os
import tempfile
import unittest

from .base import ForkOutputTest

import piprun


class TestPiprun(ForkOutputTest):
    """Test piprun."""

    def execute_file(self, contents, *arguments):
        """
        Execute a file with specified contents using piprun.

        :param arguments: Arguments to pass to the process.
        :returns: Process output, as a string.
        """

        with tempfile.NamedTemporaryFile() as file_:
            file_.write(contents.encode())
            file_.flush()

            return self.fork_output(
                lambda: piprun.main(file_.name, *arguments))

    FLASK_SCRIPT = """
#!/usr/bin/env piprun Flask==0.10.1 --

from flask import Flask

print(Flask)
"""

    def test_execution(self):
        """Test executing a file that specifies dependencies."""

        self.assertEqual(
            self.execute_file(self.FLASK_SCRIPT),
            '''flask.app.Flask'''
        )
