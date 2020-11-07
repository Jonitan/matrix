import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jonitan-matrix",
    version="1.0.1",
    author="Yonatan Naisteter",
    author_email="skiba8150@gmail.com",
    description="Matrix of size NxN implementation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jonitan/matrix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)