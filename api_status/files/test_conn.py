import os
import time
import socket

def is_connexion_open(api_address = os.environ.get('API_SERVER'), api_port = os.environ.get('API_PORT'), duration=10, nb_test=10):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  is_closed=True
  while nb_test > 0 and is_closed:
    try:
      s.connect((api_address, int(api_port)))
      s.close()
      is_closed=False
      status_code = 0
    except socket.error:
      time.sleep(int(duration / nb_test))
      nb_test= nb_test - 1
      is_closed = True
  return not is_closed

if __name__ == "__main__" :
  print(f"Connexion is open: {is_connexion_open()}")
