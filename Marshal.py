from dateutil.parser import parse

from Models import DeskCase, DeskCustomer


class Marshal(object):
    @staticmethod
    def desk_case(json):
        results = list()

        for element in json:
            case = DeskCase()
            case.id = element['id']
            case.labels = element['label_ids']
            case.updated_at = parse(element['updated_at'])
            case.status = element['status']
            case.custom_fields = element['custom_fields']

            case.customer_id = element['_links']['customer']['href'].split('/')[-1]

            results.append(case)

        return results

    @staticmethod
    def desk_customer(json):
        customer = DeskCustomer()
        customer.id = json['id']
        customer.first_name = json['first_name']
        customer.last_name = json['last_name']
        customer.emails = json['emails']

        return customer
