import string
from random import sample, choice
from hashlib import md5
from os.path import join

chars = string.letters + string.digits
length = 80
a = ''.join([choice(chars) for i in range(length)]) # way 2
b = md5(a).hexdigest()
c = md5(a).hexdigest()
d = join(b + c)
print d
