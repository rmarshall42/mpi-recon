from collections import defaultdict
import numpy as np
import pickle
import glob

import json
import os

TYPE = 'Alltoallv'

for filepath in glob.iglob("./%s/repos/*.txt" % TYPE):
	name = ''
	#json_store = {}
	with open(filepath) as f:
		last = ''
		store = defaultdict(list)
		#flag = False
		for idx, line in enumerate(f):
			if idx == 0:
				name = line.split()[1].replace("/", "")
			curr = line.rstrip().split()
			if len(curr) == 1:
				last = curr[0]
			elif curr[0] == 'Call:':
				store[last].append((curr[1], curr[-1]))
			'''
			elif curr[0] == '***':
				flag = True
			if flag:
				if len(curr) == 2:
					key = str(curr[0].split('"')[1])
					json_store[key] = (int(curr[1].replace(',', '')))
			'''

	'''
	base = Path(TYPE+ '/json')
	jsonpath = base / (name + ".json")
	base.mkdir(exist_ok=True)
	jsonpath.write_text(json.dumps(json_store))

	'''
	with open(os.path.join(TYPE+ '/pkl' , TYPE + "_" + name), 'wb') as ff:
		pickle.dump(store, ff)
	#np.save(os.path.join(TYPE + '/npy' , TYPE + "_" + name), np.array(dict(store)))



