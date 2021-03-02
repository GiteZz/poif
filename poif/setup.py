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
    packages=setuptools.find_packages(),
    # https://docs.python.org/3/distutils/setupscript.html#installing-package-data
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["daif=poif.cli.cli:main"]},
    install_requires=[
        "opencv-python==4.5.1.48",
        "dataclasses==0.8",
        "PyYAML==5.4.1",
        "jinja2==2.11.3",
        "dataclasses_json==0.5.2",
        "pandas==1.1.5",
        "numpy==1.19.5",
        "tqdm==4.58.0",
        "requests==2.25.1",
        "fusepy==3.0.1",
        "boto3==1.17.17",
        "gitpython==3.1.13",
    ],
    extras_require={
        "test": [
            "black==20.8b1",
            "isort==5.7.0",
            "mypy==0.800",
            "pytest==6.2.2",
            "autoflake==1.4",
            "docker==4.4.4",
            "pdoc3==0.9.2",
        ]
    },
)
