"""Setup.py to ensure hwcomponents._version_scheme is importable during build."""

import sys
import os
from pathlib import Path

# Add paths to ensure hwcomponents can be imported
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Try to find hwcomponents in parent directories (for submodule case)
parent_dir = current_dir.parent.parent
hwcomponents_dir = parent_dir / "hwcomponents"
if hwcomponents_dir.exists() and str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from setuptools import setup
from setuptools.command.build import build
import shutil
import subprocess

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        """Mark wheel as platform-specific since it bundles a compiled C++ binary."""

        def finalize_options(self):
            super().finalize_options()
            self.root_is_pure = False

        def run(self):
            # Temporarily pretend we have ext_modules so that install_lib places
            # files in platlib (the wheel root with Root-Is-Purelib: false) rather
            # than in {dist_info}.data/purelib/ which auditwheel rejects.
            orig = self.distribution.has_ext_modules
            self.distribution.has_ext_modules = lambda: True
            try:
                super().run()
            finally:
                self.distribution.has_ext_modules = orig

        def get_tag(self):
            _, _, plat = super().get_tag()
            return "py3", "none", plat

except ImportError:
    bdist_wheel = None

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
        "build": CustomBuildCommand,
        **({"bdist_wheel": bdist_wheel} if bdist_wheel is not None else {}),
    },
)
