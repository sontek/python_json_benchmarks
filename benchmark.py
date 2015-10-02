import random
import sys
import timeit

from functools import partial
from tabulate import tabulate

import yajl
import simplejson
import json
import rapidjson
import ujson


from collections import defaultdict


default_data = {
    'words': """
        Lorem ipsum dolor sit amet, consectetur adipiscing
        elit. Mauris adipiscing adipiscing placerat.
        Vestibulum augue augue,
        pellentesque quis sollicitudin id, adipiscing.
        """,
    'list': list(range(200)),
    'dict': dict((str(i),'a') for i in list(range(200))),
    'int': 100100100,
    'float': 100999.123456
}

user = {
    "userId": 3381293,
    "age": 213,
    "username": "johndoe",
    "fullname": u"John Doe the Second",
    "isAuthorized": True,
    "liked": 31231.31231202,
    "approval": 31.1471,
    "jobs": [ 1, 2 ],
    "currJob": None
}

friends = [ user, user, user, user, user, user, user, user ]

doubles = []
unicode_strings = []
strings = []
booleans = []
list_dicts = []
dict_lists = {}

medium_complex = [
    [user, friends],  [user, friends],  [user, friends],
    [user, friends],  [user, friends],  [user, friends]
]

for x in range(256):
    doubles.append(sys.maxsize * random.random())
    unicode_strings.append("نظام الحكم سلطاني وراثي في الذكور من ذرية السيد تركي بن سعيد بن سلطان ويشترط فيمن يختار لولاية الحكم من بينهم ان يكون مسلما رشيدا عاقلا ًوابنا شرعيا لابوين عمانيين ")
    strings.append("A pretty long string which is in a list")
    booleans.append(True)

for y in range(100):
    arrays = []
    list_dicts.append({str(random.random()*20): int(random.random()*1000000)})

    for x in range(100):
        arrays.append({str(random.random() * 20): int(random.random()*1000000)})
        dict_lists[str(random.random() * 20)] = arrays

doubles_dumped = rapidjson.dumps(doubles)
strings_dumped = rapidjson.dumps(strings)
dicts_dumped = rapidjson.dumps(dict_lists)
complex_dumped = rapidjson.dumps(medium_complex)

contenders = [
    ('yajl', yajl.Encoder().encode, yajl.Decoder().decode),
    ('simplejson', simplejson.dumps, simplejson.loads),
#    ('json', json.dumps, json.loads),
    ('rapidjson', rapidjson.dumps, partial(rapidjson.loads, precise_float=True)),
    ('ujson', ujson.dumps, partial(ujson.loads, precise_float=True))
]

doubles_test_name_dumps = 'Array 256 Doubles (dumps)'
doubles_test_name_loads = 'Array 256 Doubles (loads)'
strings_test_name_dumps = 'Array 256 unicode strings (dumps)'
strings_test_name_loads = 'Array 256 unicode strings (loads)'
dict_test_name_dumps = '100 dicts of 100 arrays (dumps)'
dict_test_name_loads = '100 dicts of 100 arrays (loads)'
complex_object_dumps = 'Complex Object (dumps)'
complex_object_loads = 'Complex Object (loads)'

results = {
    doubles_test_name_dumps: defaultdict(list),
    doubles_test_name_loads: defaultdict(list),
    strings_test_name_dumps: defaultdict(list),
    strings_test_name_loads: defaultdict(list),
    dict_test_name_dumps: defaultdict(list),
    dict_test_name_loads: defaultdict(list),
    complex_object_dumps: defaultdict(list),
    complex_object_loads: defaultdict(list),
}

for i in range(0, 5):
    random.shuffle(contenders)
    for name, dumps, loads in contenders:
        results[doubles_test_name_dumps][name].append(
            timeit.timeit(lambda: dumps(doubles), number=1000)
        )
        results[doubles_test_name_loads][name].append(
            timeit.timeit(lambda: loads(doubles_dumped), number=1000)
        )

        results[strings_test_name_dumps][name].append(
            timeit.timeit(lambda: dumps(strings), number=5000)
        )
        results[strings_test_name_loads][name].append(
            timeit.timeit(lambda: loads(strings_dumped), number=1000)
        )

        results[dict_test_name_dumps][name].append(
            timeit.timeit(lambda: dumps(dict_lists), number=2)
        )
        results[dict_test_name_loads][name].append(
            timeit.timeit(lambda: loads(dicts_dumped), number=2)
        )

        results[complex_object_dumps][name].append(
            timeit.timeit(lambda: dumps(medium_complex), number=1000)
        )
        results[complex_object_loads][name].append(
            timeit.timeit(lambda: loads(complex_dumped), number=1000)
        )


table = []
headers = ['test']
results = sorted(results.items())

for test_name, data in results:
    test_table = [test_name]
    data = sorted(data.items())
    for module, values in data:
        headers.append(module)
        avg = sum(values) / len(values)
        test_table.append(avg)
    table.append(test_table)

print(tabulate(table, headers, tablefmt='grid'))
