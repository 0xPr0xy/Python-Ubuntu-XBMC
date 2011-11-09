for n in range(2, 200):
	for x in range(2, n):
		if n % x == 0:
			#print '|no prime|', n, '=', x, '*', n/x
			break
	else:
         	# loop fell through without finding a factor
		print '|   prime|', n
