import re

# Read the input file
with open("input.txt", "r") as file:
    data = file.read()

# Extract numbers using regular expression
pattern = r'\[\s*(\d+\s*(?:,\s*\d+\s*)*)\]'
# Find all matches
matches = re.findall(pattern, data)
numbers = [re.findall(r'\d+', match) for match in matches]
#print(numbers)
flattened_numbers = [int(num) for sublist in numbers for num in sublist]

dedup_numbers = list(set(flattened_numbers))
sorted_numbers = sorted(dedup_numbers)

#print(sorted_numbers)
sorted_numbers_str = [str(num) for num in sorted_numbers]

# Print the numbers separated by commas
print(','.join(sorted_numbers_str))
