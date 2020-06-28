from setuptools import setup, find_packages

with open("README.md", 'r') as fr:
	description = fr.read()

setup(
    name='pyCheckmol',
    version='1.0.0',
    url='https://github.com/jeffrichardchemistry/pyCheckmol',
    license='GNU GPL',
    author='Jefferson Richard',
    author_email='jrichardquimica@gmail.com',
    keywords='Cheminformatics, Chemistry, checkmol, smiles, quantum-chemistry, Molecules',
    description='A package for Cheminformatics.',
    long_description = description,
    long_description_content_type = "text/markdown",
    packages=['pyCheckmol'],
    install_requires=['pandas>=0.25.3'],
	scripts=['bin/checkmol-config', 'bin/openbabel-config', 'bin/pycheckmol-config'],
	classifiers = [
		'Intended Audience :: Developers',
		'Intended Audience :: End Users/Desktop',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Chemistry',
		'Topic :: Scientific/Engineering :: Physics',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Operating System :: Unix',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6']
)
