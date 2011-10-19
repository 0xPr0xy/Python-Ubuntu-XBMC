
import string
from random import sample, choice
chars = string.letters + string.digits
length = 20
''.join([choice(chars) for i in range(length)]) # way 2

