def main():
	str1 = 'hello'
	# print(str1[0])
	print(str1,' Faiz',' length=>',len(str1))

	int1 = 6 
	int2 = 7
	print(int2/int1)

	str2 = r'sjdf s\n\t'
	print(str2)

	str3 = """This is a test for 
	multiline statement"""

	print(str3)

	str4 = "hello"
	print(str4[:-1])
	print(str4[-3:])

	print(str4[1:])

	str5 = "%d is called %s in german language" % (1,'\'eine\'')
	print(str5)



if __name__ == "__main__":
	main()