import os
import json
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, Query
from typing import List
from benchmarks import tmmluplus, mt_bench, ifeval, hellaswag, triviaqa, GSM8K, OpenbookQA, MathQA, PiQA, TruthfulQA, main_5
from dotenv import load_dotenv
load_dotenv()

TAIDE_API_KEY = os.environ['TAIDE_API_KEY'] # 'secret_random_string' #INTEGRATION KEY

benchmark_to_database = {
    "TMMLUplus": os.environ['TMMLU_DATABASE'],
    "MT-Bench": os.environ['MT_BENCH_DATABASE'],
    "IFEval": os.environ['IFEVAL_DATABASE'],
    "TriviaQA": os.environ['TRIVIAQA_DATABASE'],
    "HellaSwag": os.environ['HELLASWAG_DATABASE'],
    "GSM8K": os.environ['GSM8K_DATABASE'],
    "OpenbookQA": os.environ['OPENBOOKQA_DATABASE'],
    "MathQA": os.environ['MATHQA_DATABASE'],
    "PiQA": os.environ['PIQA_DATABASE'],
    "TruthfulQA": os.environ['TRUTHFULQA_DATABASE'],
    "Main_5": os.environ['MAIN_5_DATABASE']
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

benchmark = ["TMMLUplus", "MT-Bench", "IFEval", "TriviaQA", "HellaSwag", "GSM8K", "OpenbookQA", "MathQA", "PiQA", "TruthfulQA", "Main_5"]
judge_model = ["No", "gpt-4-0613", "ev.1.0.0", "ev.1.1.0", "ev.2.0.0"]

app = FastAPI()

@app.get("/")
def read_root():
    return "Notion Database Upload"

@app.post("/api/update_to_notion")
async def update_to_notion(
    files: List[UploadFile] = File(...),
    date: str = "",
    database_id: str='',
    integration_api: str='',
    model_name: str = '',
    Benchmark: str = Query(..., enum=benchmark),
    Judge_Model: str = Query("No", enum=judge_model),
    Update_exist: bool = Query(True)
):
    # Save the uploaded file
    try:
        if date == "":
            date = str(datetime.now().strftime("%Y%m%d-%H%M%S"))
        if database_id == "" and integration_api == "":
            database_id = benchmark_to_database[Benchmark]
            integration_api = TAIDE_API_KEY
            logger.info("You are going to upload the organization's database")
        else:
            if database_id == "" or integration_api == "":
                return {"message": "You need to provide both of database id and integration key or keep them blank"}
            logger.info("You are going to upload the specific database")
        logger.info(f"Upload {Benchmark}")
            
        try:
            date = transform_date(date)
        except Exception as e:
            logger.error(e)
            return {"message": "(Date) Upload Failed!!!"}
        
        if Benchmark == "Main_5":   
            data = dict()
            for file in files:
                if "eval" in file.filename:
                    filename = file.filename
                    bench_name = os.path.splitext(os.basename(filename))[0].split("_")[-1]
                    
                    try:
                        contents = await file.read()
                        data[bench_name] = json.loads( contents )["overall"]["avg_score"]
                    except Exception as e:
                        logger.error(e)
                        return {"message": "There was an error on reading file."}
                    finally:
                        await file.close()
            logger.info("Build Page Info")
            page = main_5.main_5(integration_api, database_id, model_name, date, Judge_Model, data)
        else:
            try:
                contents = await files[0].read()
                data = json.loads( contents )
            except Exception as e:
                logger.error(e)
                return {"message": "There was an error on reading file."}
            finally:
                await files[0].close()
            
            logger.info("Build Page Info")
            if Benchmark =="TMMLUplus":
                page = tmmluplus.tmmluplus(integration_api, database_id, model_name, date, data)
            elif Benchmark == "MT-Bench":
                page = mt_bench.mt_bench(integration_api, database_id, date, data)
            elif Benchmark == "IFEval":
                page = ifeval.ifeval(integration_api, database_id, model_name, date, data)
            elif Benchmark == "TriviaQA":
                page = triviaqa.triviaqa(integration_api, database_id, model_name, date, data)
            elif Benchmark == "HellaSwag":
                page = hellaswag.hellaswag(integration_api, database_id, model_name, date, data)
            elif Benchmark == "GSM8K":
                page = GSM8K.GSM8K(integration_api, database_id, model_name, date, data)
            elif Benchmark == "OpenbookQA":
                page = OpenbookQA.openbookqa(integration_api, database_id, model_name, date, data)
            elif Benchmark == "MathQA":
                page = MathQA.mathqa(integration_api, database_id, model_name, date, data)
            elif Benchmark == "PiQA":
                page = PiQA.piqa(integration_api, database_id, model_name, date, data)
            elif Benchmark == "TruthfulQA":
                page = TruthfulQA.truthfulqa(integration_api, database_id, model_name, date, data)
        
        try:
            logger.info("Upload Page Info")
            resp = page.upload(Update_exist)
            return {"message": resp}
        except Exception as e:
            logger.error(e)
            return {"message": f"({Benchmark}) Upload Failed !!!"}
        
    except Exception as error:
        logger.error(error)
        return {"message": "There was an error uploading the file"}

def transform_date(date):
    if len(date) == 0:
        date = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    d = date.split('/')[-1].split('-')[0]
    t = date.split('/')[-1].split('-')[1]
    date = f"{d[:4]}-{d[4:6]}-{d[6:]}T{t[:2]}:{t[2:4]}:{t[4:]}"
    date = datetime.fromisoformat(date)
    date = date - timedelta(hours=8)
    date = date.strftime("%Y-%m-%dT%H:%M:%S")
    
    return date