import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cisco-interface-parse-config",
    version="1.0.0",
    description="Parses interface names and output desired configurations",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vkoprivica/Cisco/Cisco_Int_Parse_Config",
    author="Vukasin Koprivica",
    author_email="vkoprivica.git@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    # packages=["hostname_press"],
    packages=find_packages(exclude=("tests",)),    
    include_package_data=True,
    # install_requires=["feedparser", "html2text"],
    data_files=[('/', ['output.txt'])],
    entry_points={
        "console_scripts": [
            "cisco-interface-parse-config=ciscoparseconfig.__main__:main",
        ]
    },
)

