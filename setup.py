import setuptools

setuptools.setup(
    name='ivcfmerge',
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "ivcfmerge = ivcfmerge.cli.core:main",
            "ivcfmerge_batch = ivcfmerge.cli.batch:main",
        ],
    }
)
