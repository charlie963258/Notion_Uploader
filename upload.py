import os 
import json
import argparse
from notion_client import Client
from notion_page import notion_page
from benchmarks.graduation import graduation_exp
from tqdm.auto import tqdm
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ['API_KEY'] # 'secret_random_string' #INTEGRATION KEY
DATABASE = os.environ['DATABASE'] #'random_string' #DATABASE KEY

main_path = "-"

for item in os.listdir(main_path):
    if item != "finance_coder_medical_layerwise":
        continue
    # if item == "Head_Wise_Pruned" or item == "ablation_study" or item == "old_result":
    #     continue
    if "copy" in item.lower():
        continue
    
    folder_path = os.path.join(main_path, item)
    model_list = []
    if "coder" in folder_path.split("/")[-1].lower():
        model_list.append("Coder")
    if "math" in folder_path.split("/")[-1].lower():
        model_list.append("Math")
    if "medical" in folder_path.split("/")[-1].lower():
        model_list.append("Medical")
    if "finance" in folder_path.split("/")[-1].lower():
        model_list.append("Finance")
    if "koni" in folder_path.split("/")[-1].lower():
        model_list.append("KONI")
    if "breeze" in folder_path.split("/")[-1].lower():
        model_list.append("Breeze2")
        
    if "expert" in folder_path.split("/")[-1].lower():
        model_list.append("Expert")
        for model_name in tqdm(os.listdir(folder_path)):
            merge_method = "None"
            upload_dict = {
                "config": {
                    "model_name": model_name,
                    "Merge_Method": merge_method,
                    "Model_Contain": model_list
                }
            }
            model_folder = os.path.join(folder_path, model_name)

            for benchmark in os.listdir(model_folder):
                if benchmark == "industryinstruction-finance":
                    benchmark = "industryinstruction_finance"
                if benchmark == "logickor" or benchmark == "hae-rae-bench":
                    lang = "ko"
                elif benchmark == "taide" or benchmark == "awesome-taiwan-knowledge":
                    lang = "zh-tw"
                elif benchmark in ["gsm8k", "math"]:
                    continue
                else:
                    lang = "en"
                benchmark_file_path = os.path.join(model_folder, benchmark, lang, "score.json")
                if not os.path.exists(benchmark_file_path):
                    print(f"File not found: {benchmark_file_path}")
                    continue

                if benchmark == "humaneval-xl":
                    with open(benchmark_file_path, "r") as f:
                        score = json.load(f)['pass@1'] * 1000
                else:
                    with open(benchmark_file_path, "r") as f:
                        score = json.load(f)['Average']
                
                upload_dict["result"] = upload_dict.get("result", {})
                upload_dict["result"][benchmark] = score

            upload_page = graduation_exp(API_KEY, DATABASE, upload_dict)
            # print(upload_page)
            upload_page.upload(update_exist=False)
    else:
        for model_name in tqdm(os.listdir(folder_path)):
            if "nick" not in model_name.lower():
                continue
            if "old" in model_name.lower():
                continue
            # if "task_arithmetic" not in model_name.lower() and "ties" not in model_name.lower():
            #     continue
            if "normal" in model_name.lower():
                if "task_arithmetic" == model_name.lower().split("_normal")[0]:
                    merge_method = "Task_Arithmetic"
                elif "ties" == model_name.lower().split("_normal")[0]:
                    merge_method = "TIES"
                elif "breadcrumbs" == model_name.lower().split("_normal")[0]:
                    merge_method = "Breadcrumbs"
                # elif "breadcrumbs_ties" == model_name.lower().split("_normal")[0]:
                #     merge_method = "Breadcrumb_TIES"
                elif "dare" == model_name.lower().split("_normal")[0]:
                    merge_method = "DARE"
                # elif "dare_ties" == model_name.lower().split("_normal")[0]:
                #     merge_method = "Dare_TIES"
                elif "multislerp" == model_name.lower().split("_normal")[0]:
                    merge_method = "Multislerp"
                elif "sce" == model_name.lower().split("_normal")[0]:
                    merge_method = "SCE"
                elif "della" == model_name.lower().split("_normal")[0]:
                    merge_method = "Della"
            else:
                merge_method = "HILA"

            upload_dict = {
                "config": {
                    "model_name": model_name,
                    "Merge_Method": merge_method,
                    "Model_Contain": model_list
                }
            }
            model_folder = os.path.join(folder_path, model_name)

            for benchmark in os.listdir(model_folder):
                if benchmark == "industryinstruction-finance":
                    benchmark = "industryinstruction_finance"
                if benchmark == "logickor" or benchmark == "hae-rae-bench":
                    lang = "ko"
                elif benchmark == "taide" or benchmark == "awesome-taiwan-knowledge":
                    lang = "zh-tw"
                elif benchmark in ["gsm8k", "math"]:
                    continue
                else:
                    lang = "en"

                benchmark_file_path = os.path.join(model_folder, benchmark, lang, "score.json")
                if not os.path.exists(benchmark_file_path):
                    print(f"File not found: {benchmark_file_path}")
                    continue
                
                if benchmark == "humaneval-xl":
                    with open(benchmark_file_path, "r") as f:
                        score = json.load(f)['pass@1'] * 1000
                else:
                    with open(benchmark_file_path, "r") as f:
                        score = json.load(f)['Average']
                
                upload_dict["result"] = upload_dict.get("result", {})
                upload_dict["result"][benchmark] = score

            upload_page = graduation_exp(API_KEY, DATABASE, upload_dict)
            # print(upload_page)
            upload_page.upload(update_exist=False)