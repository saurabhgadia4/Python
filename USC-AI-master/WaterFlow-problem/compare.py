file1 = 'output.txt'
file2 = 'output_test.txt'

if __name__=="__main__":
	pass_count = 0
	total_count = 0
	fail_count=0
	pass_tests = []
	fail_tests = []
	f1_obj = open(file1,'r')
	f2_obj = open(file2,'r')
	loop=1
	while loop:
		l1 = f1_obj.readline()
		l2 = f2_obj.readline()
		if l1 == '':
			loop = 0
			break
		total_count+=1
		# print 'l1',l1
		# print 'l2',l2
		if l1==l2:
			pass_count+=1
			pass_tests.append(total_count)
		else:
			fail_count+=1
			fail_tests.append(total_count)

	print 'total_Count',total_count,'pass Count:',pass_count,'fail_count',fail_count
	print 'pass testcases',pass_tests
	print 'fail testcases',fail_tests


