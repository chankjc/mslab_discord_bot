import copy
import default_message as default

record = {}


def GetRecord(id):
    if id not in record.keys():
        record[id] = copy.deepcopy(default.default_setting)
    return record[id]


def SaveRecord(id, message):
    for item in message:
        record[id].append(item)
    record[id] = [record[id][0]] + record[id][-1 * min(len(record[id]) - 1, 10) :]
