#!/usr/bin/python3.8

import requests

#

logged = [{'status' : False}]

#

def Setlogged(value):

    global logged

    logged[0] = value

#

def Push(path, method='GET', json=None, cookies=None):

    url = ('https://microlancer.io/api' + path)

    if method == 'GET':
        return requests.get(url, json=json, cookies=cookies)

    if method == 'POST':
        return requests.post(url, json=json, cookies=cookies)

#

class Login:

    def __init__(self, email, password):

        self.email, self.password = email, password

    def __repr__(self):

        return 'https://github.com/Zenitsudeck/'

    def login(self, two2fa=None):

        cookies = dict(requests.get('https://microlancer.io/').cookies)

        Setlogged({'status' : True, 'cookies' : cookies, 'csrftoken' : None})

        json = Push('/auth/login', cookies=logged[0]['cookies']).json()
        json['formValues'].update({'email' : self.email, 'password' : self.password})

        request = Push('/auth/login', method='POST', json=json, cookies=logged[0]['cookies'])

        Setlogged({'status' : True, 'cookies' : dict(request.cookies), 'csrftoken' : request.json()['formValues']['csrfToken']})

        request = request.json()

        if str(two2fa).isnumeric() == True and 'message' in request['statusMessage'].keys():

            if 'google authentication' in request['statusMessage']['message']:

                return self.auth(two2fa)

            return request

        return request

    def auth(self, two2fa):

        json = Push('/auth/login-google-authentication', cookies=logged[0]['cookies']).json()
        json['formValues'].update({'verificationCode' : two2fa, 'csrfToken' : logged[0]['csrftoken']})

        request = Push('/auth/login-google-authentication', method='POST', json=json, cookies=logged[0]['cookies']).json()

        if request['statusMessage'] == None:

            Setlogged({'status' : True, 'cookies' : logged[0]['cookies'], 'csrftoken' : request['formValues']['csrfToken']})

            return request

        return request

    def logout(self):

        Setlogged({'status' : False})

        return Push('/auth/logout', cookies=self.cookies).json()

#

class Tasks:

    def __init__(self):

        if logged[0]['status'] == False:

            raise ValueError('You have not yet logged into the account.')

    def list(self, first=1, lenght=50, status='any', minsats=1, user=None):

        if (status in ['any', 'draft', 'my', 'alert']) and  (minsats > 0):

            query = '/task/list?start={0}&length={1}&status={2}&minimumAmount={3}'.format(first, lenght, status, minsats)

            if user != None:
                query += '&user={0}'.format(user)

            return Push(query, cookies=logged[0]['cookies']).json()

    def create(self, title, description, amount=1, repeatable=True, escrow=True):

        if (amount >= 1) and (repeatable in [True, False]) and (escrow in [True, False]):

            json = Push('/task/create', cookies=logged[0]['cookies']).json()
            json['formValues'].update({'title' : title, 'description' : description, 'amount' : amount})

            if repeatable == True:
                json['formValues']['repeat'] = repeatable

            if escrow == True:
                json['formValues']['escrow'] = escrow

            json['formValues']['csrfToken'] = logged[0]['csrftoken']

            return Push('/task/create', method='POST', json=json, cookies=logged[0]['cookies']).json()

    def edit(self, id, title, description, amount=1, repeatable=True, escrow=True):

        if (amount >= 1) and (repeatable in [True, False]) and (escrow in [True, False]):

            json = Push('/task/edit?id=' + id, cookies=self.login.cookies)

            if isinstance(json, list) == True:
                raise ValueError('Post with given ID is not found (it may have been deleted).')

            json['formValues'].update({'title' : title, 'description' : description, 'amount' : amount})

            if repeatable == True:
                json['formValues']['repeat'] = repeatable

            if escrow == True:
                json['formValues']['escrow'] = escrow

            json['formValues']['csrfToken'] = logged[0]['csrftoken']

            return Push('/task/edit', method='POST', json=json, cookies=logged[0]['cookies']).json()

    def view(self, id, first=1, lenght=50, status='any'):

        query = '?id={0}?start={1}&lenght={2}&status={3}'.format(id, first, lenght, status)

        return Push('/task/view' + query, cookies=logged[0]['cookies']).json()

    def comment(self, id, comment):

        if str(id).isnumeric() == True:

            json = Push('/task/comment', cookies=logged[0]['cookies']).json()
            json['formValues'].update({'csrfToken' : logged[0]['csrftoken'], 'comment' : comment, 'taskId' : id})

            return Push('/task/comment', method='POST', json=json, cookies=logged[0]['cookies']).json()

#

class Offer:

    def __init__(self):

        if logged[0]['status'] == False:

            raise ValueError('You have not yet logged into the account.')

    def pitch(self, id, amount=1, pitch='I can do this task.'):

        id = str(id)

        if (id.isnumeric() == True) and (amount >= 1):

            json = Push('/offer/pitch', cookies=logged[0]['cookies']).json()

            json['formValues'].update({'pitch' : pitch, 'comment' : '', 'amount' : amount, 'csrfToken' : logged[0]['csrftoken']})
            json['formValues'].update({'postId' : id, 'offerId' : id, 'replyType' : 'offer'})

            return Push('/offer/pitch', method='POST', json=json, cookies=logged[0]['cookies']).json()

    def reply(self, offerid, message):

        offerid = str(offerid)

        if offerid.isnumeric() == True:

            json = Push('/offer/reply', cookies=logged[0]['cookies']).json()

            json['formValues'].update({'offerId' : offerid, 'message' : message, 'replyType' : 'message', 'csrfToken' : logged[0]['csrftoken']})

            return Push('/offer/reply', method='POST', json=json, cookies=logged[0]['cookies']).json()

    def retract(self, offerid, message='I can not do.'):

        offerid = str(offerid)

        if offerid.isnumeric() == True:

            json = Push('/offer/reply', cookies=logged[0]['cookies']).json()
            json['formValues'].update({'offerId' : offerid, 'message' : message, 'replyType' : 'retract', 'csrfToken' : logged[0]['csrftoken']})

            return Push('/offer/reply?id={0}'.format(offerid), method='POST', json=json, cookies=logged[0]['cookies']).json()

    def proposed(self, offerid, amount, message=''):

        offerid = str(offerid)

        if offerid.isnumeric() == True:

            json = Push('/offer/reply?id={0}'.format(7017), cookies=logged[0]['cookies']).json()

            if int(amount) == int(json['formValues']['proposedAmount']):
                return json

            json['formValues'].update({
                'offerId' : offerid, 'message' : message, 'replyType' : 'adjust', 'proposedAmount' : amount,
                'csrfToken' : logged[0]['csrftoken']
            })

            return Push('/offer/reply?id={0}'.format(offerid), method='POST', json=json, cookies=logged[0]['cookies']).json()

    def view(self, id):

        id = str(id)

        if id.isnumeric() == True:

            return Push('/view?id={0}'.format(id), cookies=logged[0]['cookies'])

class Notifications:

    def __init__(self):

        if logged[0]['status'] == False:
            raise ValueError('You have not yet logged into the account.')

    def dismiss(self, ids):

        if isinstance(ids, list) == True:

            json = Push('/notifications/dismiss', cookies=logged[0]['cookies']).json()
            json['formValues'].update({
                'notificationIds' : ids, 'csrfToken' : logged[0]['csrftoken'],
                'inputDisabled' : True, 'submitButtonDisabled' : True,
                'submitButtonContent' : {
                    'nodeName' : 'span', 'children' : ['Dismiss'],
                    'attributes': {'class' : 'loading'},
                    'status' : 'posting'
            }})

            return Push('/notifications/dismiss', method='POST', json=json, cookies=logged[0]['cookies']).json()

    def list(self, first=5, lenght=50, dismissed=True):

        if isinstance(first, int) == True and isinstance(lenght, int) == True:

            query = '/notifications/list?start={0}&length={1}'.format(first, lenght)

            if dismissed == True:
                query += '&showReadMessages=1'

            if dismissed == False:
                query += '&showReadMessages=0'

            return Push(query, cookies=logged[0]['cookies']).json()

def Current():

    if logged[0]['status'] == False:
        raise ValueError('You have not yet logged into the account.')

    return Push('/user/current', cookies=logged[0]['cookies']).json()

class Withdraw:

    def __init__(self):

        if logged[0]['status'] == False:
            raise ValueError('You have not yet logged into the account.')

    def withdraw(self, invoice, two2fa=None):

        if invoice[:4] == 'lnbc':

            json = Push('/withdraw/process', cookies=logged[0].cookies).json()
            json['formValues']['csrfToken'] = logged[0]['csrftoken']
            json['formValues']['invoice'] = invoice

            if str(two2fa).isnumeric() == True:
                json['formValues']['verificationCode'] = two2fa

            return Push('/withdraw/process', method='POST', json=json, cookies=logged[0]['cookies']).json()

class Services:

    def __init__(self):

        if logged[0]['status'] == False:
            raise ValueError('You have not yet logged into the account.')

    def view(self, id):

        if isinstance(id, int) == True and id >= 1:

            query = '/service/view?id={0}'.format(id)

            return Push(query, cookies=logged[0]['cookies']).json()

    def list(self, first=1, lenght=50, status='any', minsats=1, user=None):

        if isinstance(first, int) == True and isinstance(lenght, int) == True:

            if status in ['any', 'draft', 'offered', 'alert'] and minsats >= 1:

                if first >= 1 and lenght >= 1:

                    query = '/service/list?start={0}&lenght={1}&status={2}&minimumAmount={3}'.format(first, lenght, status, minsats)

                    if (user != None):
                        query += '&user={0}'.format(user)

                    return Push(query, cookies=logged[0]['cookies']).json()

    def create(self, escrow=True, packages=[]):

        if isinstance(packages, list) == True and len(packages) >= 1:

            packages_services = []

            for package in packages:

                if isinstance(package, dict) == True:

                    if list(package.keys()) !=  ['title', 'description', 'amount']:
                        raise ValueError('Your package is not complete.')

                    package.update({'status' : 1, 'packageId' : None})
                    packages_services.append(package)

            json = Push('/service/create', cookies=logged[0]['cookies']).json()
            json['formValues'].update({'escrow' : escrow, 'packages' : packages_services, 'csrfToken' : logged[0]['csrftoken']})

            if escrow == True:
                json['formValues']['escrow'] = 1

            if escrow == False:
                json['formValues']['escrow'] = 2

            return Push('/service/create', method='POST', json=json, cookies=logged[0]['cookies']).json()

#
