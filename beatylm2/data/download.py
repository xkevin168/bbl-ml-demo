from beatylm2.utils.data_utils import get_image_list
from pathlib import Path
import requests
from typing import List, Union
import os
import time
import random
from tqdm import tqdm

''' Definition of get_image_list from bbl-ml-demo/beatylm2/utils/data_utils.py:
from pygbif import occurrences as occ

def get_image_list(**kwargs):
    # For arguments see: https://techdocs.gbif.org/en/openapi/v1/occurrence#/Searching%20occurrences/
    
    # default search arguments
    search_args = {
        "datasetKey": "07fd0d79-4883-435f-bba1-58fef110cd13",
        "mediaType": "StillImage",
        "limit": 1000,
    }

    # override default search arguments with user-provided arguments
    search_args.update(kwargs)

    # search for occurrences
    query = occ.search(**search_args)

    # extract the list of image files
    list_of_files = []
    for record in query["results"]:
        list_of_files.append(record["catalogNumber"] + ".jpg")

    return list_of_files'''

def download_images(dst_path: Union[Path, str], num_samples: int, **kwargs):

    # ensure the destination directory exists
    dst_path = Path(dst_path)
    os.makedirs(dst_path, exist_ok=True)

    # download images
    print(f"Downloading {num_samples} images to '{os.path.abspath(dst_path)}'...")
    print(f"\tNote* there are only ~35,000 images in the database")
    print(f"\tNote* that many images are not available which may slow down the download process")

    files_downloaded = []
    num_downloaded = 0
    num_tries = 0 # number of images tried to download, can be used to set begining offset for future downloads
    offset = kwargs.get("offset", 0)

    while num_downloaded < num_samples:
        # get list of images to download
        image_files = get_image_list(**kwargs)
        if not image_files:
            print("No more image files to download.")
            break

        # download images in the list
        with tqdm(total=num_samples, desc="Downloading images", initial=num_downloaded, unit="image") as pbar:
            for image_file in image_files:
                
                url = f"https://beaty.b-cdn.net/{image_file}"
                try:
                    response = requests.get(url, stream=True)
                except Exception as e:
                    print(f"An error occurred while downloading {url}: {e}")
                    return len(files_downloaded), files_downloaded, num_tries

                num_tries += 1

                if response.status_code == 200:
                    with open(dst_path / image_file, "wb") as f:
                        f.write(response.content)

                    files_downloaded.append(image_file)
                    num_downloaded += 1
                    pbar.update(1)

                    if num_downloaded >= num_samples:
                        break

                # add a random delay to avoid overloading the server
                time.sleep(random.uniform(0.1, 1))

            offset += len(image_files)
            kwargs["offset"] = offset
        
    return len(files_downloaded), files_downloaded, num_tries

if __name__ == "__main__":
    num, files, num_tries = download_images("data/images", num_samples=1000, limit=200)
    print(f"Downloaded: {num} images")
    print(f"Files: {files}")
    print(f"final offset: {num_tries}")
    