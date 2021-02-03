import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylinerating",  # Replace with your own username
    version="1.0.0",
    author="Tomas Barton",
    author_email="tommz9@gmail.com",
    description="A package to calculate the rating of power transmission lines (IEEE-728, CIGRE-601).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tommz9/pylinerating",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy >= 1.15",
        "pytest",
    ],
    setup_requires=["pytest > 3", "black > 18"],
)
