import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

requires = [
    "docopt",
    "bpl-lib>=0.1.0",
    "bpl-api>=0.1.0",
    "ascii-table>=0.1.0",
    "mnemonic"
]

packages = [
    "bpl_client",
    "bpl_client.network",
    "bpl_client.helpers",
    "bpl_client.commands",
    "bpl_client.commands.account",
    "bpl_client.commands.message",
    "bpl_client.commands.network",
    "bpl_client.commands.network.config"
]

setuptools.setup(
    name="bpl-client",
    version="0.1.0",
    author="Alistair O'Brien",
    author_email="alistair.o'brien@ellesmere.com",
    description="A CLI Client for the Blockpool Blockchain.",
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    url="https://github.com/DuneRoot/bpl-cli",
    packages=packages,
    install_requires=requires,
    entry_points={
        "console_scripts": [
            "bpl-cli=bpl_client.__main__:main"
        ]
    }
)
