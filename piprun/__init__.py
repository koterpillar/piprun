"""Piprun main module."""

import hashlib
import os
import subprocess


def devnull():
    """Polyfill subprocess.DEVNULL for Python < 3.3."""
    try:
        return subprocess.DEVNULL
    except AttributeError:
        return open(os.devnull, 'w')


VIRTUALENV_DIR = os.path.expanduser('~/.piprun')


class Environment(object):
    """A Python virtual environment reference."""

    def __init__(self, requirements, interpreter=None):
        """
        Create a virtual environment reference.

        :param interpreter: Python interpreter to use
        :param requirements: Requirements to install into the environment
        """

        self.requirements = requirements
        self.interpreter = interpreter or None

    def create(self):
        """Create this virtual environment."""

        virtualenv_args = ['virtualenv', '--quiet']
        if self.interpreter:
            virtualenv_args.append('--python={}'.format(self.interpreter))
        virtualenv_args.append(self.path)
        subprocess.check_call(virtualenv_args, stdout=devnull())

        pip = os.path.join(self.binary_path, 'pip')
        subprocess.check_call((pip, 'install') + tuple(self.requirements),
                              stdout=devnull())

    def activate(self):
        """Activate this virtual environment for use in subprocesses."""

        os.environ['VIRTUAL_ENV'] = self.path
        os.environ['PATH'] = \
            self.binary_path + ':' + os.environ.get('PATH', '')

    @property
    def exists(self):
        """Whether this environment exists."""

        return os.path.exists(self.path)

    @property
    def path(self):
        """
        Path to this virtual environment, based on the hash of the requirements
        and the interpreter.
        """

        return os.path.join(VIRTUALENV_DIR, self.hash)

    @property
    def binary_path(self):
        """Path to the binaries in the virtual environment."""

        return os.path.join(self.path, 'bin')

    @property
    def hash(self):
        """Hash of the environment requirements and interpreter."""

        return str(hash((self.interpreter, tuple(self.requirements))))


class Piprun(object):
    """Main Piprun object."""

    def split_args(self, args):
        """
        Split an argument list into arguments for piprun itself and the program
        being run. Everything before the first '--' is considered to be
        requirements, what follows '--' is passed to the program. It is an
        error not to have '--' in the list.
        """

        try:
            reqs_end = args.index('--')
        except ValueError:
            raise ValueError("Argument list must include '--'.")

        return args[:reqs_end], args[reqs_end + 1:]

    def __init__(self, *args):
        """Parse the command line arguments."""

        requirements, program_args = self.split_args(args)

        if os.path.exists(requirements[0]):
            self.interpreter = requirements[0]
            self.requirements = requirements[1:]
        else:
            self.interpreter = None
            self.requirements = requirements

        self.program_args = program_args

    def run(self):
        """Create or activate the environment and run the specified program."""
        self.environment = Environment(
            requirements=self.requirements,
            interpreter=self.interpreter,
        )

        if not self.environment.exists:
            self.environment.create()

        self.environment.activate()

        return self.execute()

    def execute(self):
        """Execute the specified script."""
        os.execvp('python', ('python',) + self.program_args)

    @classmethod
    def main(cls, *args):
        """Main entry point."""

        piprun = cls(*args)
        piprun.run()


def main(*args):
    """Console entry point."""

    return Piprun.main(*args)
