import warnings
from dli.client.components import SirenComponent
from dli.client.utils import ensure_count_is_valid
from dli.client.components.urls import search_urls


class Search(SirenComponent):
    """
    Catalogue search functions.
    """

    def search(self, term, count=100):
        """
        Search across all catalogue entities given a particular set of keywords.

        :param str term: The search term.
        :param int count: Optional. The amount of results to be returned.

        :returns: A list of Catalogue entities
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                automotive_catalogue_entities = client.search(
                    term="Automotive",
                    count=100
                )

        """
        warnings.warn(
            f'Calls to search will be deprecated in future. '
            f'New endpoints will be provided in the Packages '
            f'and Datasets that will allow you to list ALL '
            f'that are visible to your user.',
            PendingDeprecationWarning
        )
        ensure_count_is_valid(count)
        return self.session.get(
            search_urls.search_root, params={'query': term, 'page_size': count}
        ).to_many_siren('')

    def search_packages(self, term, count=100):
        """
        Search across packages in the catalogue given a particular set of keywords.

        :param str term: The search term.
        :param int count: Optional. The amount of results to be returned. Defaults to 100.

        :returns: A list of packages
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                automotive_packages = client.search_packages(
                    term="Automotive",
                    count=100
                )

        """
        warnings.warn(
            f'Calls to search packages will be deprecated in future. '
            f'New endpoints will be provided in the Packages '
            f'and Datasets that will allow you to list ALL '
            f'that are visible to your user.',
            PendingDeprecationWarning
        )
        ensure_count_is_valid(count)
        return self.session.get(
            search_urls.search_packages, params={'query': term, 'page_size': count}
        ).to_many_siren('package')

    def search_datasets(self, term, count=100):
        """
        Search across datasets in the catalogue given a particular set of keywords.

        :param str term: The search term.
        :param int count: Optional. The amount of results to be returned. Defaults to 100.

        :returns: A list of datasets
        :rtype: list[collections.namedtuple]

        - **Sample**

        .. code-block:: python

                results = client.search_datasets(
                    term="CDS",
                    count=100
                )

        """
        warnings.warn(
            f'Calls to search datasets will be deprecated in future. '
            f'New endpoints will be provided in the Packages '
            f'and Datasets that will allow you to list ALL '
            f'that are visible to your user.',
            PendingDeprecationWarning
        )
        ensure_count_is_valid(count)
        return self.session.get(
            search_urls.search_datasets, params={'query': term, 'page_size': count}
        ).to_many_siren('dataset')
