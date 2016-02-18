import unittest

from app.models.transient.Plan import Plan


class PlanTest(unittest.TestCase):
    """docstring for BasicsTestCase"""

    def setUp(self):
        print "setUp"
        pass

    def testPlan(self):
        plan = Plan()
        plan.plan()
        print "abc"

    def tearDown(self):
        print "tearDown"


if __name__ == '__main__':
    unittest.main()
