from setuptools import find_packages, setup

setup(
    name="dependify",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    url="https://github.com/EliJaghab/dependify",
    author="Your Name",
    author_email="elijaghab@gmail.com",
    description="A Python library for identifying dependencies in test files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
