
# Console print helper

import json
import pprint


INDENT = 2

pp = pprint.PrettyPrinter(indent=INDENT)


def ppp(to_print, as_json=False):
	print('')
	if as_json:
		print(
			json.dumps(
				to_print,
				sort_keys=True,
				indent=INDENT,
				separators=(',', ': ')
			)
		)
	else:
		pp.pprint(to_print)