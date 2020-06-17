import logging

import dateutil.parser

from udata.models import Dataset
from .utils import check_url, UnreachableLinkChecker

log = logging.getLogger(__name__)


class CroquemortLinkChecker(object):
    """Croquemort link checker implementation.

    The main interface is the `check` method.
    """

    def _format_response(self, response):
        status = response.get('final-status-code')
        try:
            status = int(status)
        except ValueError:
            return {'check:error': 'Malformed check response'}
        else:
            check_date = response.get('updated')
            if check_date:
                check_date = dateutil.parser.parse(response.get('updated'))

            result = {
                'check:url': response.get('checked-url'),
                'check:status': status,
                'check:available': status and status >= 200 and status < 400,
                'check:date': check_date,
            }

            for header in [
                'content-type', 'content-length', 'content-md5', 'charset',
                'content-disposition'
            ]:
                value = str(response.get(header, '') or '')
                if len(value) > 0:
                    try:
                        result[f"check:headers:{header}"] = int(value)
                    except ValueError:
                        result[f"check:headers:{header}"] = value

            return result

    def check(self, resource):
        """
        Parameters
        ----------
        resource : a uData resource instance to be checked

        Returns
        -------
        dict or None
            The formatted response from the linkchecker, like so:
            {
              'check:url': 'https://example.com',
              'check:status': 200,
              'check:available': True,
              'check:date': datetime.datetime(2017, 9, 4, 11, 13, 8, 888288),
              'check:headers:content-type': 'text/csv',
              'check:headers:content-length': 245436,
              'check:headers:content-md5': 'acbd18db4cc2f85cedef654fccc4a4d8',
              'check:headers:charset': 'utf-8',
              'check:headers:content-disposition': 'inline'
            }
            Or in case of failure (in udata-croquemort, not croquemort):
            {
              'check:error': 'Something went terribly wrong.'
            }
            Or in case of failure in croquemort:
            None
        """
        log.debug('Checking resource w/ URL %s', resource.url)
        dataset = Dataset.objects(resources__id=resource.id).first()
        if not dataset:
            message = 'No dataset found for resource %s', resource.id
            log.error(message)
            return {'check:error': message}
        try:
            # do not check ftp(s) urls
            if resource.url and resource.url.lower().startswith('ftp'):
                return
            check_response = check_url(resource.url, group=dataset.slug)
            return self._format_response(check_response)
        except UnreachableLinkChecker as e:
            log.error('Unreachable croquemort for url %s: %s', resource.url, e)
            return
