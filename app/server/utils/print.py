
# Console print helper

import json
import pprint
pp = pprint.PrettyPrinter(indent=2)


def ppp(to_print, as_json=False):
	if as_json:
		print(
			json.dumps(
				to_print,
				sort_keys=True,
				indent=2,
				separators=(',', ': ')
			)
		)
	else:
		pp.pprint(to_print)