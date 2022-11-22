import json

with open('matchs_dict.json', "r") as file:
    matchs_dict = json.load(file)
try:
    print((matchs_dict['57125']['Part5']) is KeyError)
except KeyError:
    print(0)
# if KeyError(matchs_dict['57125']['Part5']):
#     print('Четверть еще не вышла')
# else:
#     print('Ваша четверть вышла')
