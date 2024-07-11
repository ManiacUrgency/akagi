import os

file_path = os.path.dirname(os.path.realpath(__file__))
input_file = os.path.join(file_path, "papers_reference_check.txt") 

with open(input_file, "r") as file:
    content = file.read()
    count = 0
    for number in range(64):
        pattern = f"[{number}]"
        if pattern in content:
            print(f"{number}: yes")
        else:
            print(f"{number}: no")
            count += 1

print("number of no references: ", count)
print("number of references:", 63 - count)