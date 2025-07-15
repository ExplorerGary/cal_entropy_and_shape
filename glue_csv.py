# glue_csv.py

import os
import csv
import pandas as pd
import matplotlib.pyplot as plt


def glue_csv():
    a = "005_ENTROPY_RESULTS_PROCESSPOOL.csv"
    b = "./DATA/006_failed_to_compress.csv"

    df1 = pd.read_csv(a)
    df2 = pd.read_csv(b)

    merged = pd.merge(df1, df2, on="name", how="outer")
    merged.to_csv("merged_output.csv", index=False)


if __name__ == "__main__":
    glue_csv()
    print("CSV files merged successfully into 'merged_output.csv'.")
    
    
    