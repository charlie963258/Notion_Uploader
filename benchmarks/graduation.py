import logging
from notion_page import notion_page
from datetime import datetime, timedelta
from datetime import datetime

logger = logging.getLogger(__name__)

class graduation_exp(notion_page):
    def __init__(self, integration_api, database_id, data):
        super().__init__(integration_api, database_id)
        
        self.database_id = database_id
        self.date = (datetime.now() - timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S")
        # self.model_name, self.base_model, self.nshot, self.dataset, self.params, self.prop = self._build_model_data(data)
        self.config, self.prop = self._build_model_data(data)

    def _build_model_data(self, data): #fetch the json data
        prop = dict()

        for item, score in data["result"].items():
            # if "BLEU" in score:
            #     for key, value in score.items():
            #         if "second" in key:
            #             continue
            #         prop[f"{item}_{key}"] = round(value, 4) / 100
            # else:
            #     if item == "nshot":
            #         prop[item] = score
            #     else:
            #         prop[item] = round(score['accuracy'], 4) / 100
            prop[item] = round(score, 4)
        
        # return data["config"]["model_name"], data['config']['base_model'], data["config"]["nshot"],  data["config"]["dataset"], data["config"]["params"] ,prop
        return data["config"], prop

    def _build_prop(self):
        prop = dict()
        prop = {
            "model_name":{
                "title":[
                    {
                        "text":{
                            # "content": f"{self.model_name}"
                            "content": f"{self.config['model_name']}"
                        }
                    }
                ]
            },
            "Merge_Method": {
                "select": {
                    "name": f"{self.config['Merge_Method']}"
                }
            },
            "Model_Contain": {
                "multi_select": [{"name": name} for name in self.config.get("Model_Contain", [])]
            },
            # "nshot": {
            #     "select": {
            #         "name": f"{self.config['nshot']}-shot"
            #     }
            # },
            # "base_model": {
            #     "select": {
            #         "name": f"{self.config['base_model']}"
            #     }
            # },
            # "dataset": {
            #     "select": {
            #         "name": f"{self.config['dataset']}"
            #     }
            # },
            # "params": {
            #     "select": {
            #         "name": self.config['params']
            #     }
            # },
            # "Date": {
            #     "date": {
            #         "start": self.date
            #     }
            # }
        }
        
        for key, value in self.prop.items():
            prop[key] = {
                "number": value
            }
        return prop

    def _get_exist_models(self):   
        database_pages = self._get_exist_page(self.database_id)
        exist_list = []     
        
        for item in database_pages:
            exist_list.append({
                "model_name": item["properties"]["model_name"]["title"][0]["plain_text"],
                "nshot": item["properties"]["nshot"]["select"]["name"],
                "date": item["properties"]["Date"]["date"]["start"].split(".")[0],
                "id": item["id"]
            })
        
        return exist_list
                
    def upload(self, update_exist):
        # exist_list = self._get_exist_models()
        
        # for item in exist_list:
        #     if item["model_name"] == self.config['model_name'] and item["nshot"] == f"{self.self.config['nshot']}-shot":
        #         logger.info(f"### Model: {self.config['model_name']} has been uploaded !!! ###")
        #         current_time = datetime.fromisoformat(f"{self.date[:-2]}00").timestamp()
        #         exist_time = datetime.fromisoformat(item["date"]).timestamp()
                
        #         if update_exist:
        #             if current_time > exist_time:
        #                 prop = self._build_prop()
        #                 self._update(item["id"], prop)
                        
        #                 return None
        #             else:
        #                 logger.info("### Already be the newest ###")
                        
        #                 return None
        #         else:
        #             logger.info("### Do not update exist, check the args parser ###")
        #             return None
                 
        prop = self._build_prop()
        # print(prop)
        page = self._create(prop, self.database_id)
        # print(page)
        # self._write_text(page["id"], self.config['config_yaml'])
        
        return None