import torch



for offset in range(0, 100, 10):
    print(offset, torch.exp(torch.tensor(-25. + offset))
          / torch.exp(torch.tensor(25. + offset)))

print()
for offset in range(0, 100, 10):
    print(offset, torch.exp(torch.tensor(-25. - offset))
          / torch.exp(torch.tensor(25. - offset)))


# x = 1.
# y = 10897393428759273457970009.


# print(torch.tensor(x) / torch.tensor(y))
# for ii in range(20):
#     x /= 10000
#     y /= 10000
#     print(torch.tensor(x) / torch.tensor(y))


# x = 1.
# y = 10897393428759273457970009.



# print()
# print()
# print()

# print(torch.tensor(x) / torch.tensor(y))
# for ii in range(20):
#     x *= 10000
#     y *= 10000
#     print(torch.tensor(x) / torch.tensor(y))
