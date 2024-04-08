print("Linear Array Search")

try:
    count = int(input("Enter the number of elements to add in an array"))
except ValueError as e:
    print(f"Error : {e}")

data_list = []
for i in range(count):
    user_input = int(input("Enter values to add"))
    data_list.append(user_input)

print("Now enter an element to search in the array")

try:
    search_data = int(input())
except ValueError as e:
    print(f"Error : {e}")

value_count = 0

for values in data_list:

    value_count = value_count + 1
    
    if values == search_data:
        print(f"Value {values} found at Index {value_count}")
    else:
        print("Cannot find the value, Sorry")

