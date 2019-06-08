import json, os, requests, ast
import numpy as np
import pandas as pd

DEFAULT_URL = "http://127.0.0.1"
PORT = "5000"
UPLOAD_PATH = "/api/dataset_upload/"

class cyberplot:
    def new(self, dataFrame, id, name, serverUrl = None):
        dataFrame.to_csv("_cp_dataset.csv", index = False)

        usedUrl = serverUrl
        if not serverUrl:
            usedUrl = DEFAULT_URL
        usedUrl += ":" + PORT + UPLOAD_PATH

        metadata = {"json": [{"json": {"name": name, "identifier": id, "containsHeader": 1}}]}
        files = {"file": open("_cp_dataset.csv", "rb")}
        response = requests.post(usedUrl, files = files, data = metadata, verify = False)

        os.unlink("_cp_dataset.csv")

        if response.status_code == 201:
            print("Dataset uploaded.")
        else:
            print(ast.literal_eval(response.text)["result"])

from pydataset import data
cp = cyberplot()
cp.new(data("iris"), id = "424bbe505a1af797062c01972a13baf1", name = "Iris Python")