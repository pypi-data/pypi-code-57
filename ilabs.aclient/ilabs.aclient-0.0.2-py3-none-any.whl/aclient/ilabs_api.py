import asks
import json
from ilabs.aclient.get_secret import get_secret
from ilabs.aclient import __version__
import logging

ILABS_USER_AGENT = 'ILabs API client ' + __version__


def noop(*av, **kav): pass


class ILabsApi:

    URL_API_BASE = 'https://ilabs-api.innodata.com'

    def __init__(self, user_key=None, user_agent=ILABS_USER_AGENT, endpoint='https://ilabs-api.innodata.com'):
        self._endpoint = endpoint

        self._user_key = user_key or get_secret().get('ilabs_user_key')
        if self._user_key is None:
            raise RuntimeError('Could not find credentials')

        self._user_agent = user_agent

    async def _request(self, method, url, data=None, content_type=None, query=None):
        headers = {
            'User-Key'     : self._user_key,
            'User-Agent'   : self._user_agent,
            'Cache-Control': 'no-cache'
        }
        if content_type is not None:
            headers['Content-Type'] = content_type

        res = await asks.request(method, url,
            params=query,
            headers=headers,
            data=data,
        )

        if res.status_code not in (200, 202):
            raise RuntimeError('REST endpoint returned error: %s' % res.status_code)

        return res

    async def _post(self, url, data, content_type=None, query=None):
        return await self._request('POST', url, data, content_type=content_type, query=query)

    async def get(self, url, query=None):
        '''
        Issues GET request with credentials.
        Useful for status/ and cancel/ REST operations using
        urls returned from predict() call.
        '''
        return await self._request('GET', url, query=query)

    async def ping(self):
        '''
        Checks that API is accessible.

        Always returns this: { "ping": "pong" }.
        '''
        res = await self.get(f'{self._endpoint}/v1/ping')
        return res.json()

    async def upload_input(self, binary_data, filename=None):
        '''
        Upload file to the input cloud folder as "filename".
        If "filename" is None, system will generate name for you.

        The best practice is to let system auto-generate name for you.

        Returns dictionary with the following keys:

        - bytes_accepted  - number of bytes in the uploaded file
        - input_filename  - the name of the file
        '''
        logging.info('Uploading as filename=%s', filename)
        url = f'{self._endpoint}/v1/documents/input/'
        if filename:
            validate_filename(filename)
            url += filename
        out = await self._post(url,
            data=binary_data,
            content_type='application/octet-stream')
        out = out.json()
        bytes_accepted = int(out['bytes_accepted'])
        if bytes_accepted != len(binary_data):
            raise RuntimeError('internal upload error: %r' % out)
        return out

    async def download_input(self, filename):
        '''
        Downloads file from the input cloud folder.

        Returns binary contents of the file.
        '''
        logging.info('Downloading input: %s', filename)
        validate_filename(filename)
        return (await self.get(f'{self._endpoint}/v1/documents/input/{filename}')).content

    async def predict(self, domain, filename):
        '''
        Schedules a task to run prediction on file "filename" using
        domain "domain".

        Returns dictionary with the following keys:

        - task_id   - task id
        - task_cancel_url  - use this url to cancel the task
        - document_output_url - use this url to download prediction result
        - tast_status_url - query status
        - output_filename - name of the output file (created only after task
            successfully completes)
        - version - ???
        '''
        logging.info('Trigger prediction job: domain=%s, filename=%s', domain, filename)
        validate_filename(filename)
        out = await self.get(f'{self._endpoint}/v1/reference/{domain}/{filename}')
        return out.json()

    async def status(self, domain, task_id):
        '''Query status of a task sceduled with predict() method

        It is recommended that clients use pre-built URL string
        returned by predict() call in 'task_status_url' to query
        the task status, instead of using this method.

        Returns dictionary with the following keys:

        - error - [optional] if present, indicates task execution error
        - completed - true or false. Typically client polls API until it
            sees compleded==True. This field is always present.
        - progress - number indicating current step
        - steps - estimated total number of steps in this task
        - message - [optional] contains progress message
        '''

        logging.info('Status query for job %s', task_id)
        out = await self.get(f'{self._endpoint}/v1/reference/{domain}/{task_id}/status')
        return out.json()

    async def cancel(self, domain, task_id):
        '''
        Cancel task scheduled with predict() method.

        It is recommended that clients use pre-built URL string
        returned by predict() call in 'task_cancel_url' to cancel
        the running task, instead of using this method.
        '''
        logging.info('Canceling job %s', task_id)
        out = await self.get(f'{self._endpoint}/v1/reference/{domain}/{task_id}/cancel')
        return out.json()

    async def download_output(self, filename):
        '''
        Retrieves file from output cloud folder

        It is recommended that clients use pre-built URL string
        returned by predict() call in 'document_output_url' to retrieve
        the prediction result, instead of using this method.
        '''
        logging.info('Downloading output: %s', filename)
        validate_filename(filename)
        out = await self.get(f'{self._endpoint}/v1/documents/output/{filename}')
        return out.content

    async def upload_feedback(self, domain, filename, binary_data):
        '''
        Uploads file to training folder for the given "domain".
        Use it to provide prediction feedback like this:

        - send file for prediction
        - receive the prediction result
        - review predicted file and edit if necessary (to correct prediction mistakes)
        - upload to training folder using this method
        '''
        logging.info('Uploading feedback: domain=%s, filename=%s', domain, filename)

        validate_domain(domain)
        validate_filename(filename)

        out = await self._post(
            f'{self._endpoint}/v1/documents/training/{domain}/{filename}',
            data=binary_data,
            content_type='application/octet-stream'
        )
        out = out.json()

        if out['bytes_accepted'] != len(binary_data):
            raise RuntimeError('internal upload error: %r' % out)

        return out

def validate_domain(domain):
    if '/' in domain or '..' in domain:
        raise ValueError('domain can not contain slashes nor double dots: %r' % domain)

def validate_filename(filename):
    if '/' in filename or '..' in filename:
        raise ValueError('file name can not contain slashes nor double dots: %r' % domain)


if __name__ == '__main__':
    import trio

    logging.basicConfig(level=logging.DEBUG)

    api = ILabsApi(user_key='12345', endpoint='http://10.111.150.154')

    async def doit():
        result = await api.ping()
        print(result)

        result = await api.upload_input(b'data')
        print(result)

        input_filename = result['input_filename']
        result = await api.predict('testpod', input_filename)
        print(result)

        task_id = result['task_id']
        output_filename = result['output_filename']

        delay = 0.5
        while True:
            await trio.sleep(delay)
            result = await api.status('testpod', task_id)
            print(result)
            if result['completed']:
                break
            delay *= 2
            if delay > 30:
                delay = 30

        if 'error' in result:
            raise RuntimeError(result['error'])

        data = await api.download_output(output_filename)
        print(data)
        return data


    trio.run(doit)