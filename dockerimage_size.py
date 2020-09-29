import requests
import json
import math

ITEMS_PER_PAGE = 10
response_content = requests.get('https://hub.docker.com/v2/repositories/library/adoptopenjdk/tags?page=1')
result_json = json.loads(response_content.text)
TOTAL_NUM_TAGS = result_json["count"]
number_iterations = math.ceil(TOTAL_NUM_TAGS / ITEMS_PER_PAGE)
TOTAL_SIZE = 0
DIGEST_ARR = []
for i in range(1,number_iterations):
    print("Iteration - " + str(i) + " / " + str(number_iterations) +" : Scanning sizes ...", end=" ")
    result_set = result_json["results"]
    if len(result_set) == 0:
        break
    for result in result_set:
        images = result["images"]
        if len(images) == 0:
            break
        for image in images:
            if image["os"] == "windows" and image["architecture"] == "amd64" and image["digest"] not in DIGEST_ARR:
                DIGEST_ARR.append(image["digest"])
                TOTAL_SIZE = TOTAL_SIZE + image["size"]
    print("Done. Total Size : " + str(TOTAL_SIZE * 0.000001) + " MB")
    response_content = requests.get(result_json["next"])
    result_json = json.loads(response_content.text)

print("Total Size: " + str(TOTAL_SIZE * 0.000000001) + " GB")