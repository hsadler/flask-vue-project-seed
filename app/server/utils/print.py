
# Console print helper

import json
import pprint


INDENT = 2

pp = pprint.PrettyPrinter(indent=INDENT)


def ppp(*args, as_json=False):
	print('')
	for arg in args:
		if as_json:
			print(
				json.dumps(
					arg,
					sort_keys=True,
					indent=INDENT,
					separators=(',', ': ')
				)
			)
		else:
			pp.pprint(arg)
