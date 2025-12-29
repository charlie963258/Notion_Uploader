# Automatically update evaluation result to Notion Database

## Set up the environment and install required package
`pip install -r requirements.txt`

### Set up the `.env` file
`TAIDE_API_KEY = TAIDE_NOTION_INTEGRATION_KEY`  
`TMMLU_DATABASE = TAIDE_NOTION_TMMLU_DATABASE`
 - You have to set the specific benchmark database if you want to ues it.
 - Read the `server.py` file and modify the API_KEY part if needed  
 - If you do not want to set up the `.env` file or upload to your specific database, you can input the key munually.
 - Remember to connect your integration to the specific database.
---
## HTTP-based API based on FastAPI Quick Start
run `uvicorn server:app --reload`

## Curl Command
Following is an example of the curl command you can try to upload your evaluation result to the notion database.  
 - The default of Datetime will be the current time when upload.
 - The default of Update_exist will be False
 - If you want to upload to your own database, both of database_id and integration key are needed, otherwise keep them blank.
```bash
curl -X 'POST' \
  '<Your_server_url>/api/update_to_notion?date=<datetime>&database_id=<Specific Database ID>&model_name=<Model Name>&Benchmark=<Benchmark>&Update_exist=<Whether update the page if exist>' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@<Your_File_path>;type=application/json'
```
### For example
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/update_to_notion?date=20240322-155253&database_id=<Testing Database ID>&<Your Integration Key>&model_name=test&Benchmark=MathQA&Update_exist=False' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@../sample_files/mathqa.json;type=application/json'
```
---
## Currently available Benchmarks
`TMMLU+` `MT-Bench` `IFEval` `TriviaQA` `HellaSwag` `GSM8K` `OpenbookQA` `MathQA` `PiQA` `TruthfulQA`
## Note
 - `MT-bench` need to use `gen_report.py` to generate the required result json file
```
python gen_report.py \
 --judge_file_path ./judgment.jsonl \
 --target_model_list model_name \
 --export_dir ./
```
 - There are some sample files in `sample` folder
