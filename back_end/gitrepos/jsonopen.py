import json
import glob

for filename in glob.iglob('./Allgather/json/*.json'):
	with open(filename) as f:
		data = json.load(f)
		print(filename, 'CUDA', data['CUDA'])

	

	
