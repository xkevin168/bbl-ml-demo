# UBC Beaty Biodiversity Museum - ML Project Demo

A proof of concept project to utilize machine learning techniques for handling, organizing, and presenting large quantities of herbarium data.

## Data Download
To download images from the beaty collection:
1. Clone the repo
2. Run `git checkout ethan-dev`
3. `cd` into the repo
4. Make sure you are in the venv or conda env you want to work with
5. Run `pip install -e .`
    - this will install the repo as a package, the -e flag tells it that you are editing the package so that when you make changes, you don't have to reinstall the package each time
6. Run `cd data`
7. Run `python download.py`
    - If you want to change the number of images you want to download, you have to modify the 'num_samples' parameter in the main function
