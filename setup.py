from setuptools import setup, find_packages
import os
import shutil

# Remove build directory
THIS_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if os.path.exists(os.path.join(THIS_SCRIPT_DIR, "build")):
    shutil.rmtree(os.path.join(THIS_SCRIPT_DIR, "build"))


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
)
