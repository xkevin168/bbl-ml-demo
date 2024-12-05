from pygbif import occurrences as occ

def get_image_list(**kwargs):
    ''' For arguments see: https://techdocs.gbif.org/en/openapi/v1/occurrence#/Searching%20occurrences/
    '''
    
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

    return list_of_files