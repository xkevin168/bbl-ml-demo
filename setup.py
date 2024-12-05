from setuptools import setup, find_packages

setup(
    name="beatylm2",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pygbif==0.6.4",
        "tqdm==4.66.4",
        # add other dependencies here
    ],
    python_requires="==3.10.*",
)
