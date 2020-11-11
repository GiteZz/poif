import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datasets", # Replace with your own username
    version="0.0.1",
    author="Gilles Ballegeer",
    author_email="gilles.ballegeer@ugent.be",
    description="Interact with DVC, gitlab and S3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['datasets=datasets.cli:main']
    },
    install_requires=[
        'PyYAML==3.12'
    ]
)