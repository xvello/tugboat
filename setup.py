import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tugboat-backups",
    version="0.2.0",
    author="Xavier Vello",
    author_email="xavier.vello@gmail.com",
    description="Integrate containers in your backup workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xvello/tugboat-backups",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click==7.0',
        'docker==3.7.2',
    ],
    entry_points='''
        [console_scripts]
        tugboat=tugboat.main:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Archiving :: Backup"
    ],
)