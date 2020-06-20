import time, datetime

class Products:

    client = None
    response = {"state":"fail","message":"no initialized"}
    
    def set_client(self,client):
        self.client = client

    #PRODUCTS
    def shop_product_search(self, access_token, fields, phrase, url_params, order = None, api='/s/MasAbrazos_AR/dw/shop/'):
        if(self.client):
            params = { 
                       
                        'query': {
                                    "text_query":  {
                                                        "fields": fields,
                                                        "search_phrase": phrase
                                                    },                                    
                                },
                        "expand": ['prices'],
                        "select": "(**)"
                     }

            request_end_point = str('product_search'+url_params)
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'GET')
            ocapi_response = self.client.do_request(access_token, params)
            print(ocapi_response)
            self.response = {"state":"ok", "message":"products fetched","ocapi_response":ocapi_response.json(),"params":params}
        return self.response
    
    def shop_product_search_prices(self, access_token, fields, phrase, url_params, order = None, api='/s/MasAbrazos_AR/dw/shop/'):
        if(self.client):
            params = {                        
                        'query': {
                                    "text_query":  {
                                                        "fields": fields,
                                                        "search_phrase": phrase
                                                    },                                    
                                },
                        "expand": ['prices'],
                        "select": "(**)"
                     }

            request_end_point = str('product_search/prices'+url_params)
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'GET')
            ocapi_response = self.client.do_request(access_token, params)
            print(ocapi_response)
            self.response = {"state":"ok", "message":"products fetched","ocapi_response":ocapi_response.json(),"params":params}
        return self.response

    # DATA API
    #***************************************#

    #PRODUCTS
    def product_search(self, access_token, fields, phrase, order = None, api='/s/-/dw/data/'):
        if(self.client):

            params = { 
                        'query': {
                                    "text_query":  {
                                                        "_type": "text_query",
                                                        "fields": fields,
                                                        "search_phrase": phrase
                                                    },                                    
                                },
                        "expand": ['prices'],
                        "select": "(**)"
                     }

            request_end_point = str('product_search')
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'POST')
            ocapi_response = self.client.do_request(access_token, params)
            print(ocapi_response)
            self.response = {"state":"ok", "message":"products fetched","ocapi_response":ocapi_response.json(),"params":params}
        return self.response

    
    def get_product(self, access_token, _id, api='/s/-/dw/data/'):
        if(self.client):
            params = {
                        "expand": ['availability, images, prices, variations']
             }
            request_end_point = str('products') + str('/') + str(_id)
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'GET')
            ocapi_response = self.client.do_request(access_token, params)
            self.response = {"state":"ok", "message":"products fetched","ocapi_response":ocapi_response.json()}
            return self.response
    

    def update_product_inventory_record(self, access_token,parameters, api='/s/-/dw/data/'):
        if(self.client):
            params = {
                        "allocation":   {
                                            "amount": parameters['amount']
                                        }
                      }

            #inventory_lists/MasAbrazos_AR-inventory/product_inventory_records/smart-diaper-v1-MasAbrazos-master  
            # option: set for single inventory and product id           
            if(('single_inventory' in parameters) and ('single_product_id' in parameters)):
                params = {
                            "allocation":   {
                                                "amount": parameters['amount']
                                            }
                         }
                print("updating single product")
                request_end_point = str('inventory_lists/') + str(parameters['single_inventory']) + str('/product_inventory_records/') + str(parameters['single_product_id'])
                self.client.set_api(api)
                self.client.set_request_path(request_end_point,'PATCH')
                ocapi_response = self.client.do_request(access_token, params)
                self.response = {"state":"ok", "message":"products inventory updated","ocapi_response":ocapi_response.json(),'multiple_products':False}
            else:
                products = parameters['products']
                products_inventory = []
                for product in products:
                    current_product_id = product['id']
                    current_product_amount = product['amount']
                    print("updating product " + str(current_product_id))
                    request_end_point = str('inventory_lists/') + str(parameters['single_inventory']) + str('/product_inventory_records/') + str(current_product_id)
                    self.client.set_api(api)
                    self.client.set_request_path(request_end_point,'PATCH')

                    params = {
                                "allocation":   {
                                                    "amount": current_product_amount
                                                }
                             }

                    ocapi_response = self.client.do_request(access_token, params)
                    products_inventory.append(ocapi_response.json())
                
                self.response = {"state":"ok", "message":"products inventory updated","ocapi_response":products_inventory,'multiple_products':True}                
            return self.response
    
    def get_product_inventory_record(self, access_token,parameters, api='/s/-/dw/data/'):
        if(self.client):
                request_end_point = str('inventory_lists/') +  str(parameters['single_inventory']) +  str('/product_inventory_records')
                self.client.set_api(api)
                self.client.set_request_path(request_end_point,'GET')
                ocapi_response = self.client.do_request(access_token, {})
                self.response = {"state":"ok", "message":"products inventory records fetched","ocapi_response":ocapi_response.json()}
                return self.response
    
    def update_products_price(self, access_token, customs_objects, api='/s/-/dw/data/'):
        ocapi_responses = []
        if(self.client):            

            for custom_object in customs_objects:
                now_milliseconds = int(time.time() * 1000) 
                request_end_point = str('custom_objects/PriceImportRequest') + str('/') + str(now_milliseconds)
                self.client.set_api(api)
                self.client.set_request_path(request_end_point,'PUT')
                ocapi_response = self.client.do_request(access_token, custom_object)
                ocapi_responses.append({"state":"ok", "message":"products price updated","ocapi_response":ocapi_response.json()})
            self.response = ocapi_responses 
            return self.response
    
    def cron_run_osf_cron(self, access_token, execution, api='/s/-/dw/data/'):
        if(self.client):   

            request_end_point = str('jobs') + str('/') + str(execution) + str('/') + str('executions')
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'POST')
            ocapi_response = self.client.do_request(access_token, {})
            self.response = {"state":"ok", "message":"run custom cron","ocapi_response":ocapi_response.json()}
            return self.response
    
    def cron_get_osf_job_status(self, access_token, execution, job_id, api='/s/-/dw/data/'):
        if(self.client):   

            request_end_point = str('jobs') + str('/') + str(execution) + str('/') + str('executions') + str('/') + str(job_id) 
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'GET')
            ocapi_response = self.client.do_request(access_token, {})
            self.response = {"state":"ok", "message":"cron status by job id","ocapi_response":ocapi_response.json()}
            return self.response
    
    def cron_replicate_stage_to_production(self, access_token, replication, api='/s/-/dw/data/'):
        if(self.client):   

            request_end_point = str('jobs') + str('/') + str(replication) + str('/') + str('executions')
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'POST')
            ocapi_response = self.client.do_request(access_token, {})
            self.response = {"state":"ok", "message":"cron replication","ocapi_response":ocapi_response.json()}
            return self.response
            