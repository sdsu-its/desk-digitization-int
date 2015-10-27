class DeskCase(object):
    """
    Models a Desk Case
    """

    def __init__(self):
        self.id = None
        self.labels = None
        self.status = None

        self.customer_id = None
        self.customer = None

        self.updated_at = None

        self.custom_fields = None


class DeskCustomer(object):
    """
    Models a Desk Customer
    """

    def __init__(self):
        self.id = None

        self.first_name = None
        self.last_name = None

        self.emails = list()


