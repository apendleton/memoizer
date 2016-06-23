from setuptools import setup, find_packages
import os


setup(
    name='memoizer',
    version='0.0.1',
    description='Python library managing function memoization, especially persistent caching.',
    long_description='Python library managing function memoization, especially persistent caching.',
    author='Thomas Low',
    author_email='code@thomaslow.com',
    url='http://code.thomaslow.com/doc/memoizer/',
    packages=find_packages(),
    license='BSD License',
    platforms=["any"],
    py_modules=["memoizer"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
