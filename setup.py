from setuptools import setup, find_packages

__version__ = "dev"
__doc__ = """
Helper module to extract info from C files."""

setup(
	name = "clang_helper",
	version = __version__,
	description = __doc__,
	packages = find_packages(),
	author = "Austin Hicks <camlorn38@gmail.com>",
	zip_safe = False,
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
	],
)
