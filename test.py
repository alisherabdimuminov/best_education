# import random

# # Your array of dictionaries
# answers = [
#     {"value_1": "a", "value_2": "b"},
#     {"value_1": "c", "value_2": "d"},
#     {"value_1": "f", "value_2": "g"},
#     {"value_1": "h", "value_2": "i"},
#     {"value_1": "j", "value_2": "k"}
# ]

# keys = [i.get("value_1") for i in answers]
# values = [i.get("value_2") for i in answers]
# random.shuffle(keys)
# random.shuffle(values)

# d = []
# for i, j in zip(keys, values):
#     d.append({
#         "value_1": i,
#         "value_2": j
#     })
# # Print the shuffled array
# print(d)
import requests

url = ""