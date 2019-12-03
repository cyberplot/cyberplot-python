import json, os, requests, ast
import numpy as np
import pandas as pd

DEFAULT_URL = "http://127.0.0.1"
PORT = "5000"
UPLOAD_PATH = "/api/dataset_upload/"

class cyberplot:
    def new(self, dataFrame, id, name, serverUrl = None, matrix = False):
        if not name:
            print("Please specify dataset name.")

        self.__upload(dataFrame, id, name, serverUrl, False, matrix)

    def update(self, dataFrame, id, serverUrl = None, matrix = False):
        self.__upload(dataFrame, id, None, serverUrl, True, matrix)

    def __upload(self, dataFrame, id, name, serverUrl, updating, matrix):
        if not id:
            print("Please specify identifier.")
            return

        datasetType = "multivariate"
        containsHeader = 1
        if matrix:
            datasetType = "matrix"
            dataFrame.to_csv("_cp_dataset.csv", index = False, header = False)
            containsHeader = 0
        else:
            dataFrame.to_csv("_cp_dataset.csv", index = False)

        usedUrl = serverUrl
        if not serverUrl:
            usedUrl = DEFAULT_URL
        usedUrl += ":" + PORT + UPLOAD_PATH

        metadata = {"json": [{"json": {"name": name, "type": datasetType, "identifier": id, "containsHeader": containsHeader, "updating": updating}}]}
        files = {"file": open("_cp_dataset.csv", "rb")}
        response = requests.post(usedUrl, files = files, data = metadata, verify = False)

        os.unlink("_cp_dataset.csv")

        if response.status_code == 201:
            print("Dataset uploaded.")
        else:
            print(ast.literal_eval(response.text)["result"])

from pydataset import data
cp = cyberplot()
cp.new(data("iris"), id = "123b7d7f8de0873d713e1e6c036c20cd", name = "Iris Dataset")