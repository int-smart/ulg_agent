#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="ulg agent",
    version="0.1.0",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "pyulog",
        "matplotlib",
        "numpy",
        "together",
        "python-dotenv",
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "ulg-extract=cli:main",
        ],
    },
    author="Abhishek",
    description="A ULG extractor for time series data.",
)
