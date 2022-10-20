
# opening the file in read mode
my_file = open("init_matrix_data.txt", "r")
  
# reading the file
data = my_file.read()
  
# replacing end of line('/n') with ' ' and
# splitting the text it further when '.' is seen.
data_into_list = data.split("\n")
pos=[]
for i in data_into_list:
    pos.append(i)
    # print(i)
# printing the data
# print(data_into_list)
my_file.close()