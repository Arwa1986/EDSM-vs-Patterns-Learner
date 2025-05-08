# import Utilities.PTA
def explor_whatis_whatisnot_next(pta):
    # transition_map = {'e1': [t1, t4], 'e2': [t3, t6, t7], 'e3': [t2, t5]}
    # transition_map : for alphabet character (transition label), list all traditions with that label
    transition_map_temp = {}

    # transition_map_final = {'e1':
    #                           {'follows_by': {'e3': 10, 'e6': 90},
    #                           'not_follows_by': ['e1', 'e2', 'e4', 'e5', 'e7']
    #                           }
    #                           'e2':
    #                           {'follows_by': {'e1': 20, 'e3': 80},
    #                           'not_follows_by': ['e2', 'e4', 'e5', 'e6', 'e7']
    #                           }
    #                     ....}
    # transition_map_final: for each alphabet character,
    # follows_by: list all characters that directly follows the key_character and their percentage of appearance
    # not_follows_by: list all characters that do not follow the key_character
    transition_map_final = {}
    for a in pta.G.get_alphabet():
        transition_map_temp[a] = []
        transition_map_final[a] = {'follows_by': {}, 'not_follows_by': []}
    for t in pta.G.get_all_transitons():
        if t.label not in transition_map_temp.keys():
            transition_map_temp[t.label] = []
        else:
            transition_map_temp[t.label].append(t)

    for a in transition_map_temp.keys():
        for t in transition_map_temp[a]:
            out_trans = pta.G.get_outgoing_transitions_for_state(t.to_state)
            for ot in out_trans:
                if ot.label not in transition_map_final[a]['follows_by']:
                    transition_map_final[a]['follows_by'][ot.label] = 1
                else:
                    transition_map_final[a]['follows_by'][ot.label] +=1
        appearance_number_of_a = len(transition_map_temp[a])
        for k in pta.G.get_alphabet():
            if k not in transition_map_final[a]['follows_by'].keys():
                transition_map_final[a]['not_follows_by'].append(k)

        for k in transition_map_final[a]['follows_by'].keys():
            transition_map_final[a]['follows_by'][k] = (transition_map_final[a]['follows_by'][k]/appearance_number_of_a)*100


    return transition_map_final
