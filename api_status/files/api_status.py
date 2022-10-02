import os
import requests

import test_conn as t

LOG_DIR='/datascientest/result/'
LOG_FILE='api_status.log'

api_address = os.environ.get('API_SERVER')
api_port = os.environ.get('API_PORT')

if not t.is_connexion_open(api_address=api_address,api_port=api_port, duration=20):
  test_status = 'FAILURE'
  status_code = 500
else:  
  r = requests.get(
     url = 'http://{address}:{port}/status'.format(address=api_address, port=api_port),
  )
  status_code = r.status_code
  if status_code == 200:
      test_status = 'SUCCESS'
  else:
      test_status = 'FAILURE'


output = '''
========================================
 PROJET02 API availability test
 M. Mazouari 
 C. Laurence
========================================

request done at "/status"

expected result = 200
actual result = {status_code}

==> {test_status}

'''
  
  
print(output.format(status_code=status_code, test_status=test_status))

if os.environ.get('LOG') == 'yes':
   print('Writing output to file:' + LOG_DIR + LOG_FILE)
   with open(LOG_DIR + LOG_FILE, 'a') as file:
      file.write(output.format(status_code=status_code, test_status=test_status))
   file.close()

