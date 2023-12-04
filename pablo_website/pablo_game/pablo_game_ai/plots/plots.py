"""
Make plots of the results
"""


import matplotlib.pyplot as plt
import json

def represent_from_json(json_file: str, title:str, label_x:str, label_y:str):
    """
    Represent results from a json file
    """
    with open(json_file,'r') as f:
        metrics = json.load(f)

    plt.figure(figsize=(10, 6))
    plt.plot(metrics)
    plt.title(title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()


def represent_from_list(list_results: list, title:str, label_x:str, label_y:str):
    """
    Represent results from a list of results
    """
    plt.figure(figsize=(10, 6))
    plt.plot(list_results)
    plt.title(title)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()