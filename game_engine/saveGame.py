import json
from os import path
from os import remove

def create_save_file():
    with open("save_file.json", "w") as save_file:
        a_nodes = {'21' : "-", '09' : "-", '00' : "-"}
        b_nodes = {'18' : "-", '10' : "-", '03' : "-"}
        c_nodes = {'15' : "-", '11' : "-", '06' : "-"}
        d_nodes = {'22' : "-", '19' : "-", '16' : "-", '07' : "-", '04' : "-", '01' : "-"}
        e_nodes = {'17' : "-", '12' : "-", '08' : "-"}
        f_nodes = {'20' : "-", '13' : "-", '05' : "-"}
        g_nodes = {'23' : "-", '14' : "-", '02' : "-"}
        lines = [['21', '09', '00'], ['18', '10', '03'], ['15', '11', '06'],
                 ['22', '19', '16'], ['07', '04', '01'], ['17', '12', '08'],
                 ['20', '13', '05'], ['23', '14', '02'], ['00', '01', '02'],
                 ['03', '04', '05'], ['06', '07', '08'], ['09', '10', '11'],
                 ['12', '13', '14'], ['15', '16', '17'], ['18', '19', '20'],
                 ['21', '22', '23'], ['00', '03', '06'], ['02', '05', '08'],
                 ['21', '18', '15'], ['23', '20', '17']]
        map = {'a_nodes' : a_nodes, 'b_nodes' : b_nodes, 'c_nodes' : c_nodes, 'd_nodes' : d_nodes,
                'e_nodes' : e_nodes, 'f_nodes' : f_nodes,'g_nodes' : g_nodes}
        data = {
            'data': {'ai_marker' : 'O',
            'ai_markers_left' : 12,
            'ai_markers_on_board' : 0,
            'ai_previous_move' : [None, None, False],
            'player_marker' : 'X',
            'player_markers_left' : 12,
            'player_markers_on_board' : 0,
            'player_previous_move': [None, None, None],}, #[Node moves from, node moved to, if moved from a three in a row (true or false)]
            

            'map' : map,
            'lines' : lines
        }
        json.dump(data, save_file, indent=1, sort_keys=True)
        return data

def save_save_file(data):
    with open("save_file.json", "w") as save_file:
        json.dump(data, save_file, indent=1, sort_keys=True)


def load_save_file():
    exists = path.exists("save_file.json")
    if (exists):
        with open("save_file.json", "r") as save_file:
            data = json.load(save_file)
            return data
    else:
        return create_save_file()

def delete_save_file():
    exists = path.exists("save_file.json")
    if (exists):
        remove('save_file.json')

# Tests

#create_save_file()
'''
#save_file = load_save_file()

#save_file["map"]["a_nodes"] = {'21' : "X", '9' : "X", '0' : "-"}
#save_file["map"]["d_nodes"]["22"] = "X"
#save_file["map"]["d_nodes"]["19"] = "O"
#save_file["map"]["d_nodes"]["16"] = "O"

#save_save_file(save_file)

#save_file = load_save_file()

#save_file = load_save_file()

'''


