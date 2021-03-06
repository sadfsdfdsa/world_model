import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Shuvaev Artem",  # Replace with your own username
    version="0.0.1",
    author="Shuvaev Artem",
    author_email="shuvaevlol@gmail.com",
    description="Package with world model for simulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sadfsdfdsa/world_model",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
