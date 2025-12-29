import os 
import json
import argparse
from datetime import datetime, timedelta
from benchmarks.graduation import graduation_exp
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ['API_KEY'] # 'secret_random_string' #INTEGRATION KEY
DATABASE = os.environ['DATABASE'] #'random_string' #DATABASE KEY

def parse_args():
    parser = argparse.ArgumentParser(description="Update eval result to notion database")
    parser.add_argument(
        "--result_path", type=str, required=True, help="result folder path"
    )
    parser.add_argument(
        "--update_exist", action="store_true", default=False,  help="if the result exist, still upload ?"
    )
    
    args = parser.parse_args()
    
    return args

if __name__ == '__main__':
    args = parse_args()

    # Load the result from the result_path
    with open(args.result_path, "r") as f:
        result = json.load(f)
    
    page = graduation_exp(API_KEY, DATABASE, result)

    page.upload(update_exist=args.update_exist)
        
