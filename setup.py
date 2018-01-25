#!/usr/bin/env python
from setuptools import setup, find_packages


with open('README.md', 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="TypoViewer",
    version="0.1.0.dev0",
    description="TypoViewer, a font viewer for Typeface an Type designers.",
    long_description=long_description,
    author="Abbas Al-Kaisi",
    author_email="fadox@gmx.net",
    url="http://fadox.github.io",
    license="GNU LGPL v3/GNU GPL v3",
    package_dir={"": "Lib"},
    packages=find_packages("Lib"),
    entry_points={
        "gui_scripts": [
            "TypoViewer =  TypoViewer.__main__:main"
        ]
    },
    install_requires=[
        "pyqt5>=5.5.0"
    ],
    platforms=["Linux", "Win32", "Mac OS X"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Fonts",
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
    test_suite="tests",
)