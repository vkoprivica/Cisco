import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cisco-multi-interface-config-assistance",
    version="1.0.1",
    description="""Script parses interface names, combines with desired predefined 
    configuration and outputs to the text file""",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vkoprivica/Cisco/Cisco_Multi_Interface_Config_Assistance",
    author="Vukasin Koprivica",
    author_email="vkoprivica.git@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ciscointparser=ciscointparser.__main__:main",
        ]
    },
)
