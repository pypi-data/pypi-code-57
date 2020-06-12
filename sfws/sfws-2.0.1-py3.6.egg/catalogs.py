
class Catalogs:
    client = None
    response = {"state":"fail","message":"no initialized"}
    
    def set_client(self,client):
        self.client = client

    #CATALOGS
    def get_catalogs(self, access_token, params, order = None):
        if(self.client):
            request_end_point = str('catalogs')

            if('catalog_id' in params):
                if(len(params['catalog_id'])>0):
                    request_end_point += str('/')+str(params['catalog_id'])

            self.client.set_request_path(request_end_point,'GET')
            ocapi_response = self.client.do_request(access_token)
            
            self.response = {"state":"ok", "message":"products fetched","ocapi_response":ocapi_response}
        return self.response
    
    def get_catalog_categories(self, access_token, params, order = None):
        if(self.client):
            request_end_point = str('catalogs')

            if('catalog_id' in params):
                #start base endpoint
                if(len(params['catalog_id'])>0):
                    request_end_point += str('/')+str(params['catalog_id'])
                
                #endpoint with category or all catgegories
                if('category_id' in params and len(params['catalog_id']) > 0):
                    if(len(params['category_id'])>0):
                        request_end_point += str('/categories/')+str(params['category_id'])
                    else:
                        request_end_point += str('/')+str('categories')
                   
            print(request_end_point)
            self.client.set_request_path(request_end_point,'GET')
            ocapi_response = self.client.do_request(access_token)
            self.response = {"state":"ok", "message":"products fetched","ocapi_response":ocapi_response}
        return self.response