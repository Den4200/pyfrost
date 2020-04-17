import setuptools

with open('README.md', 'r') as f:
    long_desc = f.read()

setuptools.setup(
    name="pyfrost",
    version="0.2.1",
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
    install_requires=[
        'astroid==2.3.3',
        'colorama==0.4.3',
        'isort==4.3.21',
        'lazy-object-proxy==1.4.3',
        'mccabe==0.6.1',
        'six==1.14.0',
        'SQLAlchemy==1.3.15',
        'typed-ast==1.4.1',
        'Werkzeug==1.0.0',
        'wrapt==1.11.2'
    ],
    python_requires='>=3.6',
)
