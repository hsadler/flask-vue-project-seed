
# Testie test framework

from utils.print import ppp


class Testie():
	"""
	Tiny little test framework for keeping track of test cases.

	"""


	def __init__(self):
		self.tests_passed = 0
		self.tests_total = 0


	def should_be_equal(self, expected, actual):
		are_equal = expected == actual
		if are_equal:
			self.tests_passed = self.tests_passed + 1
		else:
			ppp(
				'actual value:',
				actual,
				'should equal expected value:',
				expected
			)
		self.tests_total = self.tests_total + 1


	def should_not_be_equal(self, expected, actual):
		are_equal = expected == actual
		if not are_equal:
			self.tests_passed = self.tests_passed + 1
		else:
			ppp(
				'actual value:',
				actual,
				'shouldn\'t equal expected value:',
				expected
			)
		self.tests_total = self.tests_total + 1


	def print_report(self):
		ppp('test results: {0}/{1}'.format(
			self.tests_passed,
			self.tests_total
		))

