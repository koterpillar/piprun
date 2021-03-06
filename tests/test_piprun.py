"""Test piprun."""

from __future__ import absolute_import

import shutil
import tempfile

from .base import ForkOutputTest

import piprun


class TestPiprun(ForkOutputTest):
    """Test piprun."""

    maxDiff = None

    def setUp(self):
        """
        Use a temporary directory for virtual environments generated by piprun.
        """

        virtualenv_dir = tempfile.mkdtemp()
        piprun.VIRTUALENV_DIR = virtualenv_dir
        self.addCleanup(shutil.rmtree, virtualenv_dir, ignore_errors=True)

    def execute_file(self, contents, *arguments):
        """
        Execute a file with specified contents using piprun.

        :param arguments: Arguments to pass to the process.
        :returns: Process output, as a string.
        """

        with tempfile.NamedTemporaryFile() as file_:
            file_.write(contents.encode())
            file_.flush()

            shebang = contents[:contents.find('\n')]
            self.assertEqual(shebang[:2], '#!',
                             "File must have a shebang.")
            shebang = shebang[2:].split()

            if shebang[0] == '/usr/bin/env':
                shebang = shebang[1:]

            self.assertEqual(shebang[0], 'piprun',
                             "File must be set up to run with piprun.")
            shebang = shebang[1:]

            arguments = shebang + [file_.name] + list(arguments)

            return self.fork_output(lambda: piprun.main(*arguments))

    def flask_script(self, version):
        """A script that requires Flask and prints its version."""

        return """
#!/usr/bin/env piprun Flask=={version} --
from __future__ import print_function

import flask

print(flask.__version__)
""".strip().format(version=version)

    def test_execution(self):
        """Test executing a file that specifies dependencies."""

        self.assertEqual(
            self.execute_file(self.flask_script('0.10.1')),
            '''0.10.1\n'''
        )
