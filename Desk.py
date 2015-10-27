import requests
from requests_oauthlib import OAuth1Session

import Config
from Logging import Logging
from Marshal import Marshal


class Desk(object):
    def __init__(self, sitename):
        self.url = 'https://%s.desk.com/api/v2/' % sitename

    def get_cases(self, case_filter=''):
        """
        Get all cases that match the supplied filter. If no filter is supplied, all cases will be fetched.

        :param case_filter: Either Customer ID, Company ID, or Filter ID
        :type case_filter: str
        :return: All Cases that match the filter, If the request was completed successfully.
        :rtype: str, bool
        """
        results, ok = self.get(self.url, 'cases' + case_filter)

        all_cases = results['_embedded']['entries']
        Logging.get_logger(__name__).debug('Get Cases returned %s' % str(results))

        while results['_links']['next'] is not None:
            results, ok = self.get(self.url, results['_links']['next']['href'].split('/')[-1])
            Logging.get_logger(__name__).debug('Get Cases returned %s' % str(results))

            all_cases.append(results['_embedded']['entries'])

        Logging.get_logger(__name__).info('Fetched a total of %d cases.' % len(all_cases))

        marshaled_results = Marshal.desk_case(all_cases)

        for case in marshaled_results:
            case.customer = self.get_customer(case.customer_id)[0]

        return marshaled_results, ok

    def get_customer(self, customer_id):
        """
        Get the Customer Information for a specified id

        :param customer_id:
         :type customer_id: int
        :return: Customer Information, If the request was completed successfully.
        :rtype: str, bool
        """
        results, ok = self.get(self.url, 'customers/' + str(customer_id))

        return Marshal.desk_customer(results), ok

    def get_filters(self):
        """
        Get all the filters in Desk.com

        :return: All Filters in Desk, If the request was completed successfully.
        :rtype: str, bool
        """
        results, ok = self.get(self.url, 'filters')
        Logging.get_logger(__name__).debug('Get Filters returned %s' % str(results))

        return results, ok

    def get_groups(self):
        """
        Get all the Groups in Desk.com

        :return: All Groups in Desk.com, If the request was successful
        :rtype: str, bool

        """
        results, ok = self.get(self.url, 'groups')
        if ok:
            results = results['_embedded']['entries']
        Logging.get_logger(__name__).debug('Get Groups returned %s' % str(results))

        return results, ok

    def get_cases_by_group(self, group_name):
        """
        Get all cases assigned to a certain group.
        Requires that a filter be setup that has all the cases for the desired group.

        :param group_name:
         :type group_name: str
        :return: All Cases belonging to the Group specified in the Parameters
        :rtype: str, bool
        """
        groups, ok = self.get_groups()
        assert ok

        group_id = 0
        for group in groups:
            if group['name'] == group_name:
                group_id = group['id']
                break

        filters, ok = self.get_filters()
        assert ok

        filter_id = 0
        for f in filters['_embedded']['entries']:
            # noinspection PyBroadException
            try:
                filter_group = int(f['_links']['group']['href'].split('/')[-1])
                if filter_group == group_id:
                    filter_id = f['id']
                    break
            except:
                pass

        results, ok = self.get_cases(case_filter='?filter_id=%i' % filter_id)

        return results, ok

    def add_note_to_case(self, case_id, note):
        """
        Add a note to the Supplied Case

        :param case_id: Case to add note to
         :type case_id: int
        :param note: Note to be added to Case
         :type note: str
        :return: The Updated Case, If the request was made successfully.
        :rtype: str, bool
        """

        Logging.get_logger(__name__).info("Adding Note to Case with ID: %d" % case_id)
        result, ok = self.post(self.url, 'cases/' + str(case_id) + '/notes',
                               {"body": note})

        return result, ok

    def resolve_case(self, case_id):
        """
        Mark a Case as Resolved

        :param case_id: Case to Resolve
         :type case_id: int
        :return: The Updated Case, If the request was made successfully.
        :rtype: str, bool
        """

        Logging.get_logger(__name__).info("Resolving Case with ID: %d" % case_id)
        result, ok = self.patch(self.url, 'cases/' + str(case_id), {"status": "resolved"})

        return result, ok

    @staticmethod
    def get(url, endpoint):
        """
        Make a GET request to the desk.com API using the pre-configured authentication method

        :param url: URL to make the GET Request to
         :type url: str
        :param endpoint: Path of the URL to make the request to
         :type endpoint: str
        :return: Returned JSON
         :rtype: str
        """
        url_endpoint = url + endpoint

        Logging.get_logger(__name__).info('Making GET Request to ' + url_endpoint)
        desk_config = Config.load_params()['Desk.com']

        if desk_config['auth_method'] == 'oauth':
            oauth_session = OAuth1Session(desk_config['client_key'],
                                          client_secret=desk_config['client_secret'],
                                          resource_owner_key=desk_config['resource_owner_key'],
                                          resource_owner_secret=desk_config['resource_owner_secret'])

            request = oauth_session.get(url_endpoint)

        else:
            request = requests.get(url_endpoint, auth=(desk_config['username'], desk_config['password']))

        try:
            return request.json(), request.status_code == 200
        except Exception, e:
            Logging.get_logger(__name__).error('Problem Getting JSON from GET Request - %s' % e.message)
            return []

    @staticmethod
    def post(url, endpoint, payload):
        """
        Make a POST request to the desired URL with the supplied Payload

        :param url: URL to make the POST Request to
         :type url: str
        :param endpoint: Path of the URL to make the request to
         :type endpoint: str
        :param payload: POST Payload
         :type payload: dict
        :return: Result JSON, If the request was made successfully
         :rtype: str, bool
        """

        url_endpoint = url + endpoint

        Logging.get_logger(__name__).info('Making POST Request to ' + url_endpoint)
        desk_config = Config.load_params()['Desk.com']

        if desk_config['auth_method'] == 'oauth':
            oauth_session = OAuth1Session(desk_config['client_key'],
                                          client_secret=desk_config['client_secret'],
                                          resource_owner_key=desk_config['resource_owner_key'],
                                          resource_owner_secret=desk_config['resource_owner_secret'])

            request = oauth_session.post(url_endpoint, payload)

        else:
            request = requests.post(url_endpoint, json=payload, auth=(desk_config['username'], desk_config['password']))

        try:
            return request.json(), request.status_code == 200
        except Exception, e:
            Logging.get_logger(__name__).error('Problem Getting JSON from POST Request - %s' % e.message)
            return []

    @staticmethod
    def patch(url, endpoint, payload):
        """
        Make a PATCH request to the desired URL with the supplied Payload


        :param url: URL to make the PATCH Request to
         :type url: str
        :param endpoint: Path of the URL to make the request to
         :type endpoint: str
        :param payload: PATCH Payload
         :type payload: dict
        :return: Result JSON, If the request was made successfully
         :rtype: str, bool
        """

        url_endpoint = url + endpoint

        Logging.get_logger(__name__).info('Making PATCH Request to ' + url_endpoint)
        desk_config = Config.load_params()['Desk.com']

        if desk_config['auth_method'] == 'oauth':
            oauth_session = OAuth1Session(desk_config['client_key'],
                                          client_secret=desk_config['client_secret'],
                                          resource_owner_key=desk_config['resource_owner_key'],
                                          resource_owner_secret=desk_config['resource_owner_secret'])

            request = oauth_session.patch(url_endpoint, payload)

        else:
            request = requests.patch(url_endpoint, json=payload,
                                     auth=(desk_config['username'], desk_config['password']))

        try:
            return request.json(), request.status_code == 200
        except Exception, e:
            Logging.get_logger(__name__).error('Problem Getting JSON from PATCH Request - %s' % e.message)
            return []
