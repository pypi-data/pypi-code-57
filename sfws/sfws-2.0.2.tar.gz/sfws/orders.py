
class Orders:

    client = None
    response = {"state":"fail","message":"no initialized"}
    
    def set_client(self,client):
        self.client = client

    #ORDERS
    def shop_orders_search(self, access_token, fields, phrase, url_params, order = None, api='/s/MasAbrazos_AR/dw/shop/'):
        if(self.client):
            params = { 
                       
                        'query': {
                                    "text_query":  {
                                                        "fields": fields,
                                                        "search_phrase": phrase
                                                    },                                    
                                },
                        "sorts" : [{"field":"customer_name", "sort_order":"asc"}],
                        "select": "(**)"
                     }

            request_end_point = str('order_search'+url_params)
            self.client.api_service = "shop_api"
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'POST')
            ocapi_response = self.client.do_request(access_token, params)
            self.response = {"state":"ok", "message":"orders fetched","ocapi_response":ocapi_response.json(),"params":params}
        return self.response
    
    def shop_update_order_status(self,access_token, order_id, params, api='/s/MasAbrazos_AR/dw/shop/'):
        if(self.client):
            client_id = self.client.api_credentials['client_id']
            request_end_point = str('orders') + str('/') + str(order_id)  + str("?client_id=") + str(client_id)
            self.client.api_service = "shop_api"
            self.client.set_api(api)
            self.client.set_request_path(request_end_point,'PATCH')
            ocapi_response = self.client.do_request(access_token, params)
            #str('?client_id='+str(api_credentials["client_id"]))
            self.response = {"state":"ok", "message":"order updated","ocapi_response":ocapi_response.json()}
        return self.response