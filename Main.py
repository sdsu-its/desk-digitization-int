import datetime

import requests

import Config
from Desk import Desk
from Logging import Logging


def send_ticket(url, email):
    """
    Generate and Send the Streaming ticket for the file hosted at URL to the supplied email

    :param url: URL of the file on File Server
     :type url: str
    :param email: Email of the Faculty who requested the Ticket
     :type email: str
    :return: If the email was sent successfully
    :rtype: bool
    """
    file_name = url.split('/')[-1]
    file_path = '/nas/streaming/faculty/ondemand/user' + url[url.find('nas/user/') + 8:]

    r = requests.get(Config.load_params()['Rohan_Search']['url'] + 'rest/email',
                     {'email': email, 'path': file_path, 'name': file_name})

    return r.status_code == 200


if __name__ == "__main__":
    desk = Desk(Config.load_params()['Desk.com']['site_name'])
    cases = desk.get_cases_by_group('Digitizing')[0]

    for case in cases:
        if case.status != 'resolved' and case.status != 'closed':
            if case.custom_fields['streaming_url'] is not None and case.custom_fields['streaming_url'] != "":
                Logging.get_logger(__name__).info("Found Case that is Ready for Processing")
                Logging.get_logger(__name__).debug("Case %d is ready for Processing" % case.id)

                client_email = case.customer.emails[0]['value']
                send_ticket(case.custom_fields['streaming_url'], client_email)
                desk.add_note_to_case(case.id, 'Streaming Ticket sent to Faculty on %s by Automation System' %
                                      datetime.datetime.now().strftime('%c'))
                desk.resolve_case(case.id)
