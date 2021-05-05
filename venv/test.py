card_number = '4000002817309428'
temp = list(card_number[:-1])
temp = [int(i) for i in temp]
print(temp)
for i in range(0, 15, 2):
    temp[i] *= 2
for i in range(len(temp)):
    if temp[i] > 9:
        temp[i] -= 9

added = sum(temp)
check_sum = added % 10
if check_sum != 0:
    check_sum = 10 - check_sum

print(check_sum)