
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
		# TODO
		pass


	def should_not_be_equal(self, expected, actual):
		# TODO
		pass


	def print_report(self):
		# TODO
		pass

