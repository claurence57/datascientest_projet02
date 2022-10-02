import os
import json
import requests

import test_conn as t

LOG_DIR='/datascientest/result/'
LOG_FILE='api_status.log'

api_address = os.environ.get('API_SERVER')
api_port = os.environ.get('API_PORT')

if not t.is_connexion_open(api_address=api_address,api_port=api_port, duration=20):
  test_status = 'FAILURE'
  output = '''
      ========================================================
        PROJET02 API content test
        M. Mazouari
        C. Laurence
      ========================================================

      Cannot connect to 
      | address={address}
      | port={port}

      ==>  {test_status}

    '''
  print(output.format(address=api_address,port=api_port,test_status=test_status))
  if os.environ.get('LOG') == 'yes':
    print('Writing output to file:' + LOG_DIR + LOG_FILE)
    with open(LOG_DIR + LOG_FILE, 'a') as file:
       file.write(output.format(address=api_address,port=api_port,test_status=test_status))
    file.close()
else:
  user = { 'username' : 'mounir', 'password' : 'mazouari' }
  sentences = [
    "However I have had bad experience camera has been handled in an unprofessional manner, the staff seems not really care our personal belongings",
    "The Eiffel Tower is absolutely beautiful I love seeing the Eiffel Tower it has amazing views from the top it is truly a remarkable site"
  ]
  
  for s in sentences:
    r = requests.get(
       url = 'http://{address}:{port}/sentiment'.format(address=api_address, port=api_port),
       params = { 'username' : user['username'], 'password' : user['password'], 'sentence' : s }
    )
 
    score = json.loads(r.content)['score']
    expected_result = (score == 'negatif')
    if s == sentences[1]:
      expected_result = (score == 'positif')
  
    if expected_result:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    output = '''
      ========================================================
        PROJET02 API content test
        M. Mazouari
        C. Laurence
      ========================================================

      request done at "/sentiment"
      | username={username}
      | password={password}
      | sentence="{sentence}"

      score = {score}

      ==>  {test_status}

    '''
    if expected_result:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    print(output.format(username=user['username'],password=user['password'],sentence=s,score=score,test_status=test_status))

    if os.environ.get('LOG') == 'yes':
      print('Writing output to file:' + LOG_DIR + LOG_FILE)
      with open(LOG_DIR + LOG_FILE, 'a') as file:
         file.write(output.format(username=user['username'],password=user['password'],sentence=s,score=score,test_status=test_status))
      file.close()

