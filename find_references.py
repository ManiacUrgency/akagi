with open("/Users/stephenjin/Documents/Leonard/paper.txt", "r") as file:
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