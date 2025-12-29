import logging
from notion_page import notion_page
from datetime import datetime

logger = logging.getLogger(__name__)

class tmmluplus(notion_page):
    def __init__(self, integration_api, database_id, model_name, date, data):
        super().__init__(integration_api, database_id)
        
        self.database_id = database_id
        self.model_name = model_name
        self.date = date
        self.nshot, self.prop, self.config, self.version = self._build_model_data(data)
        self.base_model, self.model_size = self._base_model_identify(model_name)

    def _build_model_data(self, data): #fetch the json data
        prop = dict()
        results = data['results']

        for item, score in results.items():
            if item == 'tmmluplus':
                prop['Avg'] = round(score['acc,none'], 4)
                continue
            if '_' in item and 'tmmluplus' in item:
                item = item.split('_', 1)[1]
                prop[item] = round(score['acc,none'], 4)
                
        config = data["config"]
        ver = data["versions"]["tmmluplus_accounting"]
        nshot = f"{data['n-shot']['tmmluplus_accounting']}shot"
        
        return nshot, prop, config, ver

    def _base_model_identify(self, name): #Identify the model
        base = []
        size = None
        name = name.lower()
        
        if 'tinyllama' in name:
            base.append('TinyLLaMA')
        elif 'llama' in name:
            base.append('LLaMA-2')
            
        if 'gemma' in name:
            base.append('Gemma')
        if 'breeze' in name:
            base.append("Breeze")
        if 'mistral' in name:
            base.append("Mistral")
        if 'mixtral' in name:
            base.append("Mixtral")
        if 'mpt' in name:
            base.append("mpt")
        if 'ferret' in name:
            base.append('Ferret')
        if 'taiwan-llm' in name:
            base.append('Taiwan-LLM')
        if "tulu" in name:
            base.append("Tulu")
        if "xwin" in name:
            base.append("Xwin")
        
        if len(base) == 0:
            base = None
            
        if "7b" in name:
            size = "7B"
        elif "13b" in name:
            size = "13B"
        elif "8x7b" in name:
            size = "8*7B"
        elif "1b" in name:
            size = "1B"
        elif "2b" in name:
            size = "2B"
        elif "70b" in name:
            size = "70B"
        elif "gpt" in name:
            size = "OpenAI"
            
        return base, size

    def _build_prop(self):
        prop = dict()
        prop = {
            "model_name":{
                "title":[
                    {
                        "text":{
                            "content": f"{self.model_name}"
                        }
                    }
                ]
            },
            "Versions": {
                "select": {
                    "name": str(self.version)
                }
            },
            "n-shot": {
                "select": {
                    "name": str(self.nshot)
                }
            },
            "Date": {
                "date": {
                    "start": self.date
                }
            }
        }
        
        if self.model_size != None:
            prop["Model Size"] = {
                "select": {
                    "name": str(self.model_size)
                }
            }
        
        if self.base_model != None:
            models = []
            for item in self.base_model:
                models.append({
                    "name": item
                })
            prop["base_model"] = {
                "multi_select": models
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
                "n_shot": item["properties"]["n-shot"]["select"]["name"],
                "date": item["properties"]["Date"]["date"]["start"].split(".")[0],
                "id": item["id"]
            })
        
        return exist_list
                
    def upload(self, update_exist):
        exist_list = self._get_exist_models()
        
        for item in exist_list:
            if item["model_name"] == self.model_name and item["n_shot"] == str(self.nshot):
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