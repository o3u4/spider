import os
s = 'D:/movie/a/a.txt'
os.makedirs('/'.join(s.split('/')[:-1]))

