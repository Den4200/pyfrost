import setuptools

with open('README.md', 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name="pyfrost",
    version="0.1.0",
    author="Dennis Pham",
    author_email="dpham.42@hotmail.com",
    description="An online chat library for creating the client and server.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/Den4200/pyfrost",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",

        "Topic :: Communications ",
        "Topic :: Communications :: Chat"
    ],
    python_requires='>=3.6',
)
