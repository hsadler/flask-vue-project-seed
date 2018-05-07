
# Testies test framework

import sys
sys.path.append('..')

from utils.print import ppp


class Testies():
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
			ppp('actual value: {0} should equal expected value: {1}'.format(
				expected,
				actual
			))
		self.tests_total = self.tests_total + 1


	def should_not_be_equal(self, expected, actual):
		are_equal = expected == actual
		if not are_equal:
			self.tests_passed = self.tests_passed + 1
		else:
			ppp('actual value: {0} shouldn\'t equal expected value: {1}'.format(
				expected,
				actual
			))
		self.tests_total = self.tests_total + 1


	def print_report(self):
		ppp('test results: {0}/{1}'.format(
			self.tests_passed,
			self.tests_total
		))

