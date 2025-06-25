from setuptools import setup, find_packages, Command
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


def readme():
    with open("README.md") as f:
        return f.read()


# Get all files in cacti/tech_params
tech_params_files = [
    "cacti/tech_params/16nm.dat",
    "cacti/tech_params/180nm-old.dat",
    "cacti/tech_params/180nm.dat",
    "cacti/tech_params/22nm.dat",
    "cacti/tech_params/32nm.dat",
    "cacti/tech_params/45nm.dat",
    "cacti/tech_params/65nm-old.dat",
    "cacti/tech_params/65nm.dat",
    "cacti/tech_params/90nm-old.dat",
    "cacti/tech_params/90nm.dat",
]

setup(
    name="hwcomponents_cacti",
    version="0.1",
    description="A package for estimating the energy and area of memories with CACTI",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
    ],
    keywords="accelerator hardware energy estimation CACTI",
    author="Tanner Andrulis",
    author_email="andrulis@mit.edu",
    license="MIT",
    python_requires=">=3.12",
    packages=find_packages(),
    py_modules=["hwcomponents_cacti"],
    package_data={
        "hwcomponents_cacti": [
            "default_cfg.cfg",
            "cacti/cacti",
            *tech_params_files,
        ],
    },
    include_package_data=True,
    entry_points={},
    cmdclass={
        'build': CustomBuildCommand,
    },
)
