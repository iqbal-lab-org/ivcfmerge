import setuptools

setuptools.setup(
    name="multifile-ORG-PYPI-USERNAME",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'paste_vcf = multifile.paster.vcf.__main__:main',
        ]
    }
)