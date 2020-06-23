from ilabs.aclient import ilabs_api
import trio
import json
import logging

def noop(*av, **kav): pass


class ILabsPredictor:

    @classmethod
    def init(cls, domain, *av, **kav):
        return cls(ilabs_api.ILabsApi(*av, **kav), domain)

    def __init__(self, api, domain):
        self.api = api
        self._domain = domain

    async def __call__(self, binary_data, progress=None):
        if progress is None:
            progress = noop

        progress('uploading %s bytes' % len(binary_data))

        response = await self.api.upload_input(binary_data)
        bytes_accepted = int(response['bytes_accepted'])
        input_filename = response['input_filename']
        progress('uploaded, accepted size=%s' % bytes_accepted)

        response = await self.api.predict(self._domain, input_filename)
        task_id = response['task_id']
        output_filename = response['output_filename']
        progress('job submitted, taks id: %s' % task_id)

        maybe_cancel = True
        try:
            count = 1
            while True:
                for count_idx in reversed(range(count)):
                    await trio.sleep(1.0)
                    progress('retrying in: %s' % (count_idx+1))

                logging.info('Requesting status for job %s', task_id)
                out = await self.api.status(self._domain, task_id)
                progress('progress: %s/%s' % (out['progress'], out['steps']))
                if out['completed']:
                    break
                count = min(count*2, 60)

            maybe_cancel = False
        finally:
            if maybe_cancel:
                logging.info('Cancelling job %s', task_id)
                await self.api.cancel(self._domain, task_id)

        err = out.get('error')
        if err is not None:
            raise RuntimeError('Prediction server returned error: ' + err)

        progress('fetching result')
        logging.info('Downloading: %s', output_filename)
        prediction = await self.api.download_output(output_filename)
        progress('downloaded %s bytes' % len(prediction))

        return prediction

    async def upload_feedback(self, filename, binary_data):
        return await self.api.upload_feedback(self._domain, filename, binary_data)


if __name__ == '__main__':

    predictor = ILabsPredictor.init('testpod', user_key='12345', endpoint='http://10.111.150.154')

    result = trio.run(predictor, b'Hello')
    print(result)