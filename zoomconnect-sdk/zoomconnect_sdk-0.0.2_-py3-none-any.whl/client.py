from zoomconnect_sdk.base_client import BaseClient


class Client(BaseClient):
    """
    Python SDK for the ZoomConnect.com API.

    Example usage:

      from zoomconnect.client import Client

      c = Client(api_token='api_token', account_email='account_email')
      try:
        message = c.send_sms("0000000000", "Welcome to ZoomConnect")
      except Exception as e:
        print(e)
      else:
        print(res)
    """

    # account : Core information related to your account
    def get_account_balance(self):
        """Makes a call to GET api/rest/v1/account/balance.

        Returns your account's credit balance

        https://www.zoomconnect.com/interactive-api/#!/account/getBalance
        """

        return self.do('GET', '/api/rest/v1/account/balance', req=None)

    def get_account_statistics(self):
        """Makes a call to GET /api/rest/v1/account/statistics.

        Returns data from the statistics report. Note that by default the statistics shown
        are based on the number of messages, use the calculateCreditValue should you wish
        to calculate the statistics based on credit value.

        https://www.zoomconnect.com/interactive-api/#!/account/getStatistics
        """

        return self.do('GET', '/api/rest/v1/account/statistics', req=None)

    def account_transfer(self, transferToEmail, numberOfCredits, transferFromEmail):
        """Makes a call to POST /api/rest/v1/account/transfer.

        Transfers credits between two users in the same team. The account email address
        fields as well as the number of credits to transfer are required.

        https://www.zoomconnect.com/interactive-api/#!/account/getStatistics
        """
        isInt, numberOfCredits = self.isInt(numberOfCredits)
        if isInt is False: raise Exception(f"numberOfCredits is not a valid number")
        req = {
            'transferToEmailAddress': transferToEmail,
            'numberOfCreditsToTransfer': numberOfCredits,
            'transferFromEmailAddress': transferFromEmail
        }

        return self.do('POST', '/api/rest/v1/account/transfer', req=req)

    def get_account_user_by_email(self, email):
        """Makes a call to GET api/rest/v1/account/user.

        Find a user for a particular email address

        https://www.zoomconnect.com/interactive-api/#!/account/search
        """
        return self.do('GET', '/api/rest/v1/account/user', req=None, param={"searchEmail": email})

    def create_account_user(self, firstName, lastName, password, emailAddress, contactNumber, company=None, userId=None,
                            creditBalance=None):
        """Makes a call to PUT /api/rest/v1/account/user.

        Creates a new sub-account in your team. The following fields are required
        firstname, lastname, email address, contact number and password.

        https://www.zoomconnect.com/interactive-api/#!/account/create
        """
        if creditBalance:
            isInt, creditBalance = self.isInt(creditBalance)
            if isInt is False: raise Exception(f"creditBalance is not a valid number")

        req = {
            "firstName": firstName,
            "lastName": lastName,
            "password": password,
            "emailAddress": emailAddress,
            "contactNumber": contactNumber,
            "company": company,
            "userId": userId,
            "creditBalance": creditBalance
        }

        return self.do('PUT', '/api/rest/v1/account/user', req=req)

    def update_account_user(self, userId, firstName, lastName, password, contactNumber):
        """Makes a call to POST /api/rest/v1/account/user/{userId}.
        Updates a sub-account in your team. The following fields can be updated
        firstname, lastname, contact number and password.

        https://www.zoomconnect.com/interactive-api/#!/account/update
        """

        req = {
            "firstName": firstName,
            "lastName": lastName,
            "password": password,
            "contactNumber": contactNumber,
            "userId": int(userId)
        }

        return self.do('POST', f'/api/rest/v1/account/user/{userId}', req=req)

    def get_account_user_by_userId(self, userId):
        """Makes a call to GET api/rest/v1/account/user/{userId}.

        Gets a user from a given user id

        https://www.zoomconnect.com/interactive-api/#!/account/getUser
        """
        isInt, userId = self.isInt(userId)
        if isInt is False:
            raise Exception(f"userId is not a valid number")
        else:
            return self.do('GET', f'/api/rest/v1/account/user/{userId}')

    # sms : Send and schedule messages
    def get_sms(self):
        """Makes a call to GET /api/rest/v1/sms/send.
        Returns an example of the data to POST to send a single message.

        https://www.zoomconnect.com/interactive-api/#!/sms/send
        """
        return self.do('GET', '/api/rest/v1/sms/send')

    def send_sms(self, recipientNumber, message, campaign=None, dateToSend=None, dataField=None):
        """Makes a call to POST /api/rest/v1/sms/send.

        Sends a single message. The recipientNumber and message fields are required.
        All other fields are optional

        https://www.zoomconnect.com/interactive-api/#!/sms/send_0
        """
        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber is not a valid mobile number. recipientNumber must be numeric and length of 10 and more")
        req = {
            'campaign': campaign,
            'recipientNumber': recipientNumber,
            'dateToSend': dateToSend,
            'dataField': dataField,
            'message': message
        }
        # 5eea0cc1c0fa4d7d7d19501e
        return self.do('POST', '/api/rest/v1/sms/send', req=req)

    def get_sms_bulk(self):
        """Makes a call to GET /api/rest/v1/sms/send-bulk.
        Returns an example of the data to POST to send multiple messages in one transaction.

        https://www.zoomconnect.com/interactive-api/#!/sms/sendBulk
        """
        return self.do('GET', '/api/rest/v1/sms/send-bulk')

    def send_sms_bulk(self, recipientNumbers, messages, campaign=None, dateToSend=None, dataField=None,
                      defaultDateToSend=None, messagesPerMinute=0):
        """Makes a call to POST /api/rest/v1/sms/send-bulk.

        Send multiple messages in one transaction.

        https://www.zoomconnect.com/interactive-api/#!/sms/send_0
        """
        smsRequestList = []
        if isinstance(recipientNumbers, list) and isinstance(messages, list):
            if len(recipientNumbers) == len(messages):
                for number, message in zip(recipientNumbers, messages):
                    validNumber, recipientNumber = self.testRecipientNumber(number)
                    if validNumber is False: raise Exception(
                        f"recipientNumber({number}) is not a valid mobile number. recipientNumber must be numeric and length of 10 and more")
                    smsRequestList.append({"recipientNumber": number, "message": message,
                                           'campaign': campaign, 'dateToSend': dateToSend,
                                           'dataField': dataField})
            else:
                raise Exception(f"recipientNumbers list and messages list are not the same length")
        elif isinstance(recipientNumbers, list) and messages:
            for number in recipientNumbers:
                validNumber, recipientNumber = self.testRecipientNumber(number)
                if validNumber is False: raise Exception(
                    f"recipientNumber({number}) is not a valid mobile number. recipientNumber must be numeric and length of 10 and more")
                smsRequestList.append({"recipientNumber": number, "message": messages,
                                       'campaign': campaign, 'dateToSend': dateToSend,
                                       'dataField': dataField})
        elif isinstance(recipientNumbers, str) and isinstance(messages, str):
            validNumber, recipientNumbers = self.testRecipientNumber(recipientNumbers)
            if validNumber is False: raise Exception(
                f"recipientNumber({recipientNumbers}) is not a valid mobile number. recipientNumber must be numeric and length of 10 and more")
            smsRequestList.append({"recipientNumber": recipientNumbers, "message": messages,
                                   'campaign': campaign, 'dateToSend': dateToSend,
                                   'dataField': dataField})
        else:
            raise Exception(f"recipientNumbers and messages parameters doesn`t contain valid values")

        isInt, messagesPerMinute = self.isInt(messagesPerMinute)
        if isInt is False: raise Exception(f"messagesPerMinute is not a valid number")

        req = {
            "defaultDateToSend": defaultDateToSend,
            "sendSmsRequests": smsRequestList,
            "messagesPerMinute": messagesPerMinute
        }

        return self.do('POST', '/api/rest/v1/sms/send-bulk', req=req)

    # contacts : Manage contacts
    def get_contacts_all(self):
        """Makes a call to GET /api/rest/v1/contacts/all.
        Returns all contacts

        https://www.zoomconnect.com/interactive-api/#!/contacts/getAll
        """
        return self.do('GET', '/api/rest/v1/contacts/all')

    def get_contact(self, contactId):
        """Makes a call to GET /api/rest/v1/contacts/{contactId}.
        Returns details for a single contact

        https://www.zoomconnect.com/interactive-api/#!/contacts/getAll
        """
        return self.do('GET', f'/api/rest/v1/contacts/{contactId}')

    def create_contact(self, firstName, lastName, contactNumber, title, links=None):
        """Makes a call to POST /api/rest/v1/contacts/create.
        Creates a contact

        https://www.zoomconnect.com/interactive-api/#!/contacts/create
        """
        validNumber, contactNumber = self.testRecipientNumber(contactNumber)
        if validNumber is False: raise Exception(
            f"contactNumber({contactNumber}) is not a valid mobile number. contactNumber must be numeric and length of 10 and more")

        req = {
            "firstName": firstName,
            "lastName": lastName,
            "contactNumber": contactNumber,
            "links": links,
            "title": title
        }
        return self.do('POST', '/api/rest/v1/contacts/create', req=req)

    def delete_contact(self, contactId):
        """Makes a call to DELETE /api/rest/v1/contacts/{contactId}.
        Delete a contact

        https://www.zoomconnect.com/interactive-api/#!/contacts/delete
        """
        return self.do('DELETE', f'/api/rest/v1/contacts/{contactId}',text=True)

    def update_contact(self, contactId, firstName, lastName, contactNumber, title, links=None):
        """Makes a call to POST /api/rest/v1/contacts/{contactId}.
        Updates a contact

        https://www.zoomconnect.com/interactive-api/#!/contacts/update
        """
        validNumber, contactNumber = self.testRecipientNumber(contactNumber)
        if validNumber is False: raise Exception(
            f"contactNumber({contactNumber}) is not a valid mobile number. contactNumber must be numeric and length of 10 and more")

        req = {
            "firstName": firstName,
            "lastName": lastName,
            "contactNumber": contactNumber,
            "links": links,
            "title": title
        }
        return self.do('POST', f'/api/rest/v1/contacts/{contactId}', req=req)

    def get_remove_contact_from_group(self, contactId, groupId):
        """Makes a call to GET /api/rest/v1/contacts/{contactId}/addFromGroup/{groupId}.
        Remove a contact from a group

        https://www.zoomconnect.com/interactive-api/#!/contacts/removeFromGroup
        """
        return self.do('GET', f'/api/rest/v1/contacts/{contactId}/addFromGroup/{groupId}',text=True)

    def remove_contact_from_group(self, contactId, groupId):
        """Makes a call to POST /api/rest/v1/contacts/{contactId}/addFromGroup/{groupId}.
        Remove a contact from a group

        https://www.zoomconnect.com/interactive-api/#!/contacts/removeFromGroup_0
        """
        return self.do('POST', f'/api/rest/v1/contacts/{contactId}/addFromGroup/{groupId}',text=True)

    def add_contact_to_group(self, contactId, groupId):
        """Makes a call to GET /api/rest/v1/contacts/{contactId}/addToGroup/{groupId}.
        Add a contact to a group

        https://www.zoomconnect.com/interactive-api/#!/contacts/addToGroup
        """
        return self.do('GET', f'/api/rest/v1/contacts/{contactId}/addToGroup/{groupId}',text=True)

    # def add_contact_to_group(self, contactId, groupId):
    #     """Makes a call to POST /api/rest/v1/contacts/{contactId}/addToGroup/{groupId}.
    #     Add a contact to a group
    #
    #     https://www.zoomconnect.com/interactive-api/#!/contacts/addToGroup_0
    #     """
    #     return self.do('POST', f'/api/rest/v1/contacts/{contactId}/addToGroup/{groupId}')

    # groups: Manage groups
    def get_groups_all(self):
        """ Makes a call to GET /api/rest/v1/groups/all
        Returns all groups

        https://www.zoomconnect.com/interactive-api/#!/groups/getAll
        """

        return self.do('GET', f'/api/rest/v1/groups/all')

    def get_group(self, groupId):
        """ Makes a call to GET /api/rest/v1/groups/{groupId}
        Returns details for a single group

        https://www.zoomconnect.com/interactive-api/#!/groups/get
        """

        return self.do('GET', f'/api/rest/v1/groups/{groupId}')

    def create_group(self, name, links=None):
        """ Makes a call to POST /api/rest/v1/groups/create
        Create a group

        https://www.zoomconnect.com/interactive-api/#!/groups/create
        """

        req = {
            "name": name,
            "links": links
        }

        return self.do('POST', f'/api/rest/v1/groups/create', req=req)

    def update_group(self, name, groupId, links=None):
        """ Makes a call to POST /api/rest/v1/groups/{groupId}
        Update a group

        https://www.zoomconnect.com/interactive-api/#!/groups/update
        """
        req = {
            "name": name,
            "links": links,
            "groupId": groupId
        }
        return self.do('POST', f'/api/rest/v1/groups/{groupId}', req=req)

    def delete_group(self, groupId):
        """ Makes a call to DELETE /api/rest/v1/groups/{groupId}
        Delete a group

        https://www.zoomconnect.com/interactive-api/#!/groups/delete
        """

        return self.do('DELETE', f'/api/rest/v1/groups/{groupId}',text=True)

    def add_group_to_contact(self, groupId, contactId):
        """ Makes a call to GET /api/rest/v1/groups/{groupId}/addContact/{contactId}
        Add a contact to a group

        https://www.zoomconnect.com/interactive-api/#!/groups/addContact
        """

        return self.do('GET', f'/api/rest/v1/groups/{groupId}/addContact/{contactId}',text=True)

    # def add_group_to_contact(self, groupId, contactId):
    #     """ Makes a call to POST /api/rest/v1/groups/{groupId}/addContact/{contactId}
    #     Add a contact to a group
    #
    #     https://www.zoomconnect.com/interactive-api/#!/groups/addContact_0
    #     """
    #
    #     return self.do('POST', f'/api/rest/v1/groups/{groupId}/addContact/{contactId}')

    def remove_group_from_contact(self, groupId, contactId):
        """ Makes a call to GET /api/rest/v1/groups/{groupId}/removeContact/{contactId}
        Remove a contact from a group

        https://www.zoomconnect.com/interactive-api/#!/groups/removeContact
        """

        return self.do('GET', f'/api/rest/v1/groups/{groupId}/removeContact/{contactId}',text=True)

    # def remove_group_from_contact(self, groupId, contactId):
    #     """ Makes a call to POST /api/rest/v1/groups/{groupId}/removeContact/{contactId}
    #     Remove a contact from a group
    #
    #     https://www.zoomconnect.com/interactive-api/#!/groups/removeContact_0
    #     """
    #
    #     return self.do('POST ', f'/api/rest/v1/groups/{groupId}/removeContact/{contactId}')

    # messages: Manage your messages
    def get_all_messages(self):
        """ Makes a call to GET /api/rest/v1/messages/all

        Returns all messages

        https://www.zoomconnect.com/interactive-api/#!/messages/getAll
        """

        return self.do('GET', f'/api/rest/v1/messages/all')

    def get_message_analyses(self, message, recipientNumber):
        """ Makes a call to POST /api/rest/v1/messages/analyse/full

        Returns full analysis of message

        https://www.zoomconnect.com/interactive-api/#!/messages/analyse_full
        """
        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber({recipientNumber}) is not a valid mobile number. recipientNumber must be numeric and length of {str(self.valid_mobile_number_length)} and more")
        req = {
            "message": message,
            "recipientNumber": recipientNumber
        }

        return self.do('POST', f'/api/rest/v1/messages/analyse/full', req=req)

    def get_message_credit_cost(self, message, recipientNumber):
        """ Makes a call to POST /api/rest/v1/messages/analyse/message-credit-cost

        Returns the number of credit which would be required to send the request message
        to the requested recipient number

        https://www.zoomconnect.com/interactive-api/#!/messages/analyse_message_credit_cost
        """
        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber({recipientNumber}) is not a valid mobile number. recipientNumber must be numeric and length of {str(self.valid_mobile_number_length)} and more")
        req = {
            "message": message,
            "recipientNumber": recipientNumber
        }

        return self.do('POST', f'/api/rest/v1/messages/analyse/message-credit-cost', req=req,text=True)

    def get_message_encoding(self, message, recipientNumber):
        """ Makes a call to POST /api/rest/v1/messages/analyse/message-encoding

        Returns the message encoding that would be required to send the requested message

        https://www.zoomconnect.com/interactive-api/#!/messages/analyse_message_encoding
        """
        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber({recipientNumber}) is not a valid mobile number. recipientNumber must be numeric and length of {str(self.valid_mobile_number_length)} and more")
        req = {
            "message": message,
            "recipientNumber": recipientNumber
        }

        return self.do('POST', f'/api/rest/v1/messages/analyse/message-encoding', req=req,text=True)

    def get_message_length(self, message, recipientNumber):
        """ Makes a call to POST /api/rest/v1/messages/analyse/message-length

        Returns the number of characters the requested message consists of

        https://www.zoomconnect.com/interactive-api/#!/messages/analyse_message_length
        """
        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber({recipientNumber}) is not a valid mobile number. recipientNumber must be numeric and length of {str(self.valid_mobile_number_length)} and more")
        req = {
            "message": message,
            "recipientNumber": recipientNumber
        }

        return self.do('POST', f'/api/rest/v1/messages/analyse/message-length', req=req,text=True)

    def check_message_length_within_max(self, message, recipientNumber):
        """ Makes a call to POST /api/rest/v1/messages/analyse/message-length-within-max-allowed

        Returns details for a single message

        https://www.zoomconnect.com/interactive-api/#!/messages/analyse
        """
        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber({recipientNumber}) is not a valid mobile number. recipientNumber must be numeric and length of {str(self.valid_mobile_number_length)} and more")
        req = {
            "message": message,
            "recipientNumber": recipientNumber
        }

        return self.do('POST', f'/api/rest/v1/messages/analyse/message-length-within-max-allowed', req=req,text=True)

    def get_number_of_messages(self, message, recipientNumber):
        """ Makes a call to POST /api/rest/v1/messages/analyse/number-of-messages

        Returns the number of SMS parts which would be sent when sending the requested message

        https://www.zoomconnect.com/interactive-api/#!/messages/analyse_number_of_messages
        """

        validNumber, recipientNumber = self.testRecipientNumber(recipientNumber)
        if validNumber is False: raise Exception(
            f"recipientNumber({recipientNumber}) is not a valid mobile number. recipientNumber must be numeric and length of {str(self.valid_mobile_number_length)} and more")

        req = {
            "message": message,
            "recipientNumber": recipientNumber
        }

        return self.do('POST', f'/api/rest/v1/messages/analyse/number-of-messages', req=req,text=True)

    def get_message(self, messageId):
        """ Makes a call to GET /api/rest/v1/messages/{messageId}

        Returns details for a single message

        https://www.zoomconnect.com/interactive-api/#!/messages/get
        """

        return self.do('GET', f'/api/rest/v1/messages/{messageId}')

    def delete_message(self, messageId):
        """ Makes a call to DELETE /api/rest/v1/messages/{messageId}

        Deletes a message

        https://www.zoomconnect.com/interactive-api/#!/messages/delete
        """

        return self.do('DELETE', f'/api/rest/v1/messages/{messageId}',text=True)

    def mark_message_as_read(self, messageId):
        """ Makes a call to PUT /api/rest/v1/messages/{messageId}/markRead

        Marks a message as read

        https://www.zoomconnect.com/interactive-api/#!/messages/markRead
        """

        return self.do('PUT', f'/api/rest/v1/messages/{messageId}/markRead')

    # def post_mark_message_as_read(self, messageId):
    #     """ Makes a call to POST /api/rest/v1/messages/{messageId}/markRead
    #
    #     Marks a message as read
    #
    #     https://www.zoomconnect.com/interactive-api/#!/messages/markRead_0
    #     """
    #
    #     return self.do('POST', f'/api/rest/v1/messages/{messageId}/markRead')

    def mark_message_as_unread(self, messageId):
        """ Makes a call to PUT /api/rest/v1/messages/{messageId}/markUnread

        Marks a message as read

        https://www.zoomconnect.com/interactive-api/#!/messages/markUnread
        """

        return self.do('PUT', f'/api/rest/v1/messages/{messageId}/markUnread')

    # def post_mark_message_as_unread(self, messageId):
    #     """ Makes a call to POST /api/rest/v1/messages/{messageId}/markUnread
    #
    #     Marks a message as read
    #
    #     https://www.zoomconnect.com/interactive-api/#!/messages/markUnread_0
    #     """
    #
    #     return self.do('POST', f'/api/rest/v1/messages/{messageId}/markUnread')

    # templates : Manage your templates
    def get_all_templates(self):
        """ Makes a call to GET /api/rest/v1/templates/all

        Returns all templates

        https://www.zoomconnect.com/interactive-api/#!/templates/getAll
        """

        return self.do('GET', f'/api/rest/v1/templates/all')

    def get_template(self, templateId):
        """ Makes a call to GET /api/rest/v1/templates/{templateId}

        Returns details for a single template

        https://www.zoomconnect.com/interactive-api/#!/templates/get
        """

        return self.do('GET', f'/api/rest/v1/templates/{templateId}')

    def delete_template(self, templateId):
        """ Makes a call to DELETE /api/rest/v1/templates/{templateId}

        Returns details for a single template

        https://www.zoomconnect.com/interactive-api/#!/templates/delete
        """
        return self.do('DELETE', f'/api/rest/v1/templates/{templateId}',text=True)

    # Pre flight static methods
    @staticmethod
    def isInt(i):
        try:
            return True, int(i)
        except ValueError:
            return False, i

    def testRecipientNumber(self, number):
        try:
            number = str(number).replace("+", "")
            int(number)
            if len(str(number)) >= self.valid_mobile_number_length:
                return True, number
            else:
                return False, number
        except Exception:
            return False, number
