import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poif",  # Replace with your own username
    version="0.0.1",
    author="Gilles Ballegeer",
    author_email="gilles.ballegeer@ugent.be",
    description="Interact with DVC, gitlab and S3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=["poif"],
    # https://docs.python.org/3/distutils/setupscript.html#installing-package-data
    package_dir={"poif": "poif"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["daif=poif.cli.cli:main"]},
    install_requires=[
        "dataclasses",
        "PyYAML",
        "jinja2",
        "dataclasses_json",
        "opencv-python",
        "awscli",
        "flask",
        "pandas",
        "numpy",
        "tqdm",
        "requests",
        "fusepy",
        "boto3",
        "gitpython",
    ],
    extras_require={
        "test": ["black==20.8b1", "isort==5.7.0", "mypy==0.800", "pytest==6.2.2", "autoflake==1.4", "docker"]
    },
)
