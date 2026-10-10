import os
import requests
import pandas as pd

def fetch_rpoB_network():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    tsv_path = os.path.join(data_dir, "rpoB_interactome.tsv")
    
    url = "https://string-db.org/api/tsv/network"
    params = {
        "identifiers": "rpoB",
        "species": 83332,  # Mycobacterium tuberculosis H37Rv
        "required_score": 700,  # High confidence
        "limit": 10
    }
    
    print("Querying STRING API for rpoB functional interactome...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with open(tsv_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Interactome data saved to: {tsv_path}\n")
        
        df = pd.read_csv(tsv_path, sep="\t")
        partners = df[["preferredName_A", "preferredName_B", "score"]].drop_duplicates()
        
        print("=== Top High-Confidence Functional Interactors ===")
        print(partners.to_string(index=False))
    else:
        print(f"STRING API request failed with status code: {response.status_code}")

if __name__ == "__main__":
    fetch_rpoB_network()
