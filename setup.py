from setuptools import setup, find_packages

setup(
    name="omnidimension",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["requests"],
    author="https://www.omnidim.io/",
    author_email="kevin@omnidim.io",
    description="Minimal SDK for Omni Assistant services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kevin-omnidim/omnidim-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)