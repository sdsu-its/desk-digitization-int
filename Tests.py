import unittest

import Config
from Desk import Desk

DESK = Desk(Config.load_params()['Desk.com']['site_name'])


class TestDesk(unittest.TestCase):
    def test_filters(self):
        filters, ok = DESK.get_filters()

        if not ok:
            self.fail('Problem Making Request')

        self.assertTrue(len(filters) > 1)

    def test_groups(self):
        groups, ok = DESK.get_groups()
        if not ok:
            self.fail('Problem Making Request')

        self.assertTrue(len(groups) > 1)

    def test_cases_from_group(self):
        cases, ok = DESK.get_cases_by_group('Digitizing')
        if not ok:
            self.fail('Problem Making Request')

        self.assertTrue(len(cases) > 1)


if __name__ == '__main__':
    unittest.main()
