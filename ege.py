# # with open("24.txt") as file:
# #     file = file.readline()


# # indexes = []
# # letters = ["ABC", "ACB", "BAC", "BCA","CAB", "CBA"]


# # for i in range(len(file)-2):
# #     s = file[i] + file[i+1] + file[i+2] 
# #     if s in letters:
# #         indexes.append(i+2)


# # max_space = 0
# # for j in range(len(indexes)-1):
# #     if (indexes[j+1] - indexes[j])-3 > max_space:
# #         max_space = (indexes[j+1] - indexes[j])-3 


# # print(max_space)


# # with open("24.txt") as file:
# #     file = file.readline()




# # counter = 0
# # max_counter = 0
# # for i in range(len(file)):
# #     if file[i] != "D":
# #         max_counter = max(max_counter, counter)
# #         counter = 0 
# #     else:
# #         counter += 1

# # print(max_counter)
# # print(counter)
        



# with open("24.txt") as file:
#     file = file.readline()

# counter = 1
# max_counter = 0
# for i in range(len(file)-1):
#     if file[i] != file[i+1]:
#         counter += 1
#     else:
#         max_counter = max(max_counter, counter)
#         counter = 1

# print(max_counter)


# def f(start, stop):
#     if start == stop:
#         return 1
#     if start > stop:
#         return 0
#     return f(start+1, stop) + f(start+3, stop) + f(start*3, stop)

# print(f(4,10) * f(10,17) * f(17,23))



# result = []
# pod_result = []
# counter = 0

# for i in range(201455, 201470):
#     for j in range(1, i+1):
#         if i % j == 0:
#             counter += 1
#             pod_result.append(j)
#     print(counter)
#     if counter == 4:
#         result.append(pod_result)
#     pod_result = []
#     counter = 0



# print(result)


"""
i - ?
j - *
"""

# stepen = 0
# result = []
# for i in range(1,10):
#     for j in range(10):
#         for y in range(10):
#             s = (str(j) * y)+"31"+(str(j) * y)+"65"+str(i)
#             if int(s) % 31 == 0 and int(s) % 2031 == 0:
#                 stepen += 1
#         for g in range(1,10):
#             if 2**g == stepen:
#                 result.append([s,int(s)%2031])
#                 break
#         stepen = 0

# print(result)




stepen = 1
result = []

first = [''] + list(range(1,10000))


for i in range(1,10):
    for j in first:
        for y in first:
            s = str(j)+"31"+str(y)+"65"+str(i)
            if int(s) >= 10**9:
                break
            if int(s) % 31 == 0 and int(s) % 2031 == 0:
                for r in range(1,int(s)// 2 + 1):
                    if int(s) % r:
                        stepen += 1
            for g in range(1,10):
                if 2**g == stepen:
                    result.append([s,int(s)//2031])
                    break
            stepen = 1


print(result)
