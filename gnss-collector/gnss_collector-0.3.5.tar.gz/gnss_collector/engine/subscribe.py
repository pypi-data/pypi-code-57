class SubscribeData:

    def __init__(self, task_name, queue_send, *args, **kwargs):
        self.task_name = task_name
        self.queue_send = queue_send
        self.clients = {}

    def add_client(self, idc):
        self.clients.update({idc: {}})

    def subscribe_table(self, idc, table_name, frequency=-1):
        """
        idc: client if for socket
        table_name: name of the table subscribed
        frequency: {-1:ALL iterations, 0: None iterations, n>0: every n iterations}

        """
        self.clients.get(idc).update(
            {table_name: {'f': frequency, 'counter': 0}})

    def send_data(self, data_input):
        # for client
        # extract list of clients
        # send data
        # {'command': 'SUBSCRIPTION',
        # 'table_name':table_name,
        # 'data':data,
        # 'DT_GEN': datetime.isoformat,
        # 'idc': idc}
        #
        for idc, table_set in self.clients.items():
            for table_name, frequency_dict in table_set.items():
                data = data_input.get(table_name, None)
                f = frequency_dict.get('f')
                counter = frequency_dict.get('counter')
                if counter == 0:
                    self.queue_send.put(data)
                elif counter > 0 and counter < f:
                    counter += 1
                    frequency_dict.update({'counter': counter})
                elif counter == f:
                    counter = 0
                    frequency_dict.update({'counter': counter})
