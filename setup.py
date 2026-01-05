from setuptools import setup
from setuptools.command.build import build
import os
import shutil
import subprocess
import sys

# Remove build directory
THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(THIS_SCRIPT_DIR, "build")):
    shutil.rmtree(os.path.join(THIS_SCRIPT_DIR, "build"))


class CustomBuildCommand(build):
    """Custom build command that runs make build before the normal build process."""

    def run(self):
        try:
            print("Running 'make build'...")
            subprocess.check_call(["make", "build"], cwd=THIS_SCRIPT_DIR)
            print("'make build' completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error running 'make build': {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("Warning: 'make' command not found. Skipping build step.")
        except Exception as e:
            print(f"Unexpected error running 'make build': {e}")
            sys.exit(1)

        # Call the parent build command
        super().run()


setup(
    cmdclass={
        'build': CustomBuildCommand,
    },
)
