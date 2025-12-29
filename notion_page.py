import requests
import logging
from notion_client import Client

logger = logging.getLogger(__name__)

class notion_page():
    def __init__(self, integration_api, database_id):
        # self._try_request(integration_api, database_id)
        self.integration_api = integration_api
        self.client = Client(auth=self.integration_api)    
            
    def _try_request(self, integration_api, database_id): #Try to connect notion DB
        result = requests.get(
            url=f"https://api.notion.com/v1/databases/{database_id}",
            headers={
                "Authorization": integration_api,
                "Notion-Version": "2022-06-28"
            }
        )
        if result.json()['object'] == 'error':
            logger.info("Fail to connect !!!")
            logger.info(result.json())
            exit() 
        
        return result
    
    def _create(self, prop, database_id):
        try:
            page = self.client.pages.create(
                parent={"database_id": database_id},
                properties=prop
            )
            logger.info("Create Page")
        except Exception as e:
            logger.error(e)
            return {"message": "There was an error uploading the file"}
        return page
    
    def _update(self, id, prop):
        page = self.client.pages.update(
            page_id=id,
            **{ "properties": prop }
        )
        logger.info("Update Page")
        return page
    
    def _get_exist_page(self, database_id):
        database_pages = self.client.databases.query(
            **{
                "database_id": database_id,
            }
        ).get("results")
            
        return database_pages
    
    def _write_text(self, id, content, update=False, type="text"):
        logger.info(f"--------Writing Text details--------")
        texts = [f'{key}: {value}' for key, value in content.items()]
        texts = '\n'.join(texts)
        
        if not update:
            try:
                self.client.blocks.children.append(
                    block_id=id,
                    children=[
                        {
                            'object': 'block',
                            'type': 'paragraph',
                            'paragraph':{
                                'rich_text':[
                                    {
                                        'type': type,
                                        'text': {
                                            'content': texts
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                )
            except:
                logger.error("Write Text Error")
                raise
        else:
            try:
                self.client.blocks.update(
                    block_id=self.client.blocks.children.list(block_id=id)["results"][0]["id"],
                    **{
                        'object': 'block',
                        'type': 'paragraph',
                        'paragraph':{
                            'rich_text':[
                                {
                                    'type': type,
                                    'text': {
                                        'content': texts
                                    }
                                }
                            ]
                        }
                    }
                )
            except:
                logger.error("Write Config Error")
                raise