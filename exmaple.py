# values = [10, 15, 8, 20, 12, 9, 18]  # 7 positions
# window = 3  # 1 before + itself + 1 after, since center=True


# values = [4, 9, 2, 15, 6, 8, 3]


# for i in range(len(values)):
#     start = max(0, i - 1)
#     end = min(len(values), i + 2)
#     neighborhood = values[start:end]
#     local_max = max(neighborhood)
#     print(f"i={i}, value={values[i]}, neighborhood={neighborhood}, local_max={local_max}, is_peak={values[i] == local_max}")



symbols = input("Give me the thicker symbol(s) you want to analyze.\n"
                "If more than one, make sure to enter them comma separated: ")

symbol = symbols.split(",")

print(f"len: {len(symbol)}")
if not symbol:
    print("List is empty")
else:
    for i in symbol:
        print(i.strip(" ").upper())

# for i in a:
#     print(i)