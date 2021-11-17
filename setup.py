import setuptools
import io

with io.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ["lxml", "tkcalendar"]

setuptools.setup(
    name="xsd2tkform",
    version="0.1.0",
    author="Alexandre Schulz",
    author_email="alexandre.schulz@irap.omp.eu",
    description="Generate Tkinter forms from XSD files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dolgalad/xsd2tkform",
    project_urls={
        "Bug Tracker": "https://github.com/Dolgalad/xsd2tkform/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    install_requires=requirements,
    package_data={"":["*.png"],
        "xsd2tkform":["img/*.png"],
        },
    include_package_data=True,
)

