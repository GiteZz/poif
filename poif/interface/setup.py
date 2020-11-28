import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poif", # Replace with your own username
    version="0.0.1",
    author="Gilles Ballegeer",
    author_email="gilles.ballegeer@ugent.be",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=[
        'poif'
    ],
    #https://docs.python.org/3/distutils/setupscript.html#installing-package-data
    package_dir={
        'poif': 'poif'

    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['daif=daif.cli:main']
    },
    install_requires=[]
)