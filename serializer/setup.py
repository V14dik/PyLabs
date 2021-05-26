try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.txt", 'r') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="Serializer",
    version="0.02.10",
    description="Lab2",
    long_description=LONG_DESCRIPTION,
    author="Monerd",
    author_email="",
    url="https://github.com/Monerd/LabsPy/tree/master/SecondLab",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ]
)