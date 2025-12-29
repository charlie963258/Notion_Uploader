import logging
from notion_page import notion_page
from datetime import datetime

logger = logging.getLogger(__name__)

class hellaswag(notion_page):
    def __init__(self, integration_api, database_id, model_name, date, data):
        super().__init__(integration_api, database_id)
        
        self.database_id = database_id
        self.model_name = model_name
        self.date = date
        self.prop, self.config = self._build_model_data(data)

    def _build_model_data(self, data): #fetch the json data
        prop = dict()
        results = data['results']["hellaswag"]

        for item, score in results.items():
            if item != "alias" and score != "N/A":
                prop[item.split(",")[0]] = round(score, 4)
                
        config = data["config"]
        
        return prop, config

    def _build_prop(self):
        prop = dict()
        prop = {
            "Model":{
                "title":[
                    {
                        "text":{
                            "content": f"{self.model_name}"
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": self.date
                }
            }
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
                "model_name": item["properties"]["Model"]["title"][0]["plain_text"] if item["properties"]["Date"]["date"] is not None else "",
                "date": item["properties"]["Date"]["date"]["start"].split(".")[0] if item["properties"]["Date"]["date"] is not None else 0,
                "id": item["id"]
            })
        
        return exist_list
                
    def upload(self, update_exist):
        exist_list = self._get_exist_models()
        
        for item in exist_list:
            if item["model_name"] == self.model_name:
                logger.info(f"### Model: {self.model_name} has been uploaded !!! ###")
                current_time = datetime.fromisoformat(f"{self.date[:-2]}00").timestamp()
                exist_time = datetime.fromisoformat(item["date"]).timestamp()
                
                if update_exist:
                    if current_time > exist_time:
                        prop = self._build_prop()
                        self._update(item["id"], prop)
                        self._write_text(item["id"], self.config, update=True)
                        
                        return None
                    else:
                        logger.info("### Already be the newest ###")
                        
                        return None
                else:
                    logger.info("### Do not update exist, check the args parser ###")
                    return None
                 
        prop = self._build_prop()
        page = self._create(prop, self.database_id)
        self._write_text(page["id"], self.config)
        
        return None