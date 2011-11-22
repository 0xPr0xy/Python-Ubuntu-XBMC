
#ask for user input
print
max_number = int(raw_input('Check primes untill number:  '))

#declare variables
part = int(max_number / 10)
steps = int(1)
last_steps = int()
percent = 0
i = 0
parts_bar = 0
primes_list = []
steps_list = []
primes_and_turns_list = []

#ask for user input
combined_output = raw_input('Output combined data? (yes/no)   ')

#start
print
print '0 %'

#check against user input
for number in range(2, max_number):
	
	#check against prime definition
	for x in range(2, number):
		
		#not a prime
		if number % x == 0:
			steps += 1
			break
	#a prime
	#store primes, steps
	else:
		steps += 1
		primes_list.append(number)
		prime_totals = len(primes_list)
		result = steps - last_steps
		last_steps = steps
		steps_list.append(result)
	
	#init parts_bar
	if steps == part:
		parts_bar += part
	
	#progression feedback 
	if steps == parts_bar:
		percent += 10
		print percent, '%'		
		parts_bar += part

#combine data		
while i != prime_totals:
	primes_steps = primes_list[i],steps_list[i]
	primes_and_turns_list.append(primes_steps)
	i += 1

#done combining, show results
if i == prime_totals:
	print '100 %'
	print
	print 'List of identified primes and the number of steps it took to find them, relative to the last identified prime.'
	print 
	if combined_output == 'no':
		for prime in primes_and_turns_list:
			print prime
	else:
		print primes_and_turns_list


	


	
	
			

			

		
			
				
			
