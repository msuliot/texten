# python setup.py sdist bdist_wheel

from setuptools import setup, find_packages

setup(
    name="texten",
    version="1.24.513",
    author="Michael Suliot",
    author_email="michael@suliot.com",
    description="Texten is a TEXT Extraction Node for converting text for a RAG system.",
    long_description=open('README.md').read(),
    url="https://github.com/msuliot/texten.git",
    packages=find_packages(),
    install_requires=[
        'git+https://github.com/msuliot/package.utils.git',
        'git+https://github.com/msuliot/package.data.loaders.git'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
