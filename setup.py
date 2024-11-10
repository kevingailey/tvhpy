import datetime                                                                                                                              
import pprint                                                                                          
import pytvh
print('enter TVH Host')
host = input()
print('enter TVH port')
port = input()
print('enter username')
username = input()
print('enter password')
password = input()

cache_py = open('tvh_data.py','w')                                                                     
cache_py.write('host =' + pprint.pformat(host) + '\n')                                                                                      
cache_py.write('username =' + pprint.pformat(username) + '\n')                                                                                    
cache_py.write('password =' + pprint.pformat(password) + '\n')                                                                                    
cache_py.write('port =' + pprint.pformat(port) + '\n')                                                                                    
cache_py.close()
print('channels list:')
pytvh.tvh(host,port,username,password)
