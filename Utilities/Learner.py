import copy
import random
# import networkx as nx

from Patterns.extract_patterns_from_reference_DFA import get_all_input_sequences_with_one_output
from Patterns.pattern_checker import violate_any_pattern, violate_any_pattern2
from Utilities.DISJOINTSETS import DisjointSet
from Utilities.PTA import PTA
from Utilities.write_clear_file import write_to_file_in_new_line


class Learner:
    figure_num = 2
    def __init__(self, pta:PTA):
        self.pta = pta
        self.found_blue = False
        self.visited = []
        self.blue_states = []


    def setup(self, edsm_file_name, with_pattern_file_name):
        self.pta.G.initial_state.color = 'red'
        self.red_states = [self.pta.G.initial_state]
        self.make_children_blue(self.pta.G.initial_state)
        self.counter = 1
        self.edsm_file_name= edsm_file_name
        self.with_pattern_file_name = with_pattern_file_name
        self.number_of_states_in_PTA = len(self.pta.G.graph.keys())


    def is_all_states_red(self):
        state_list = list(self.pta.G.graph.keys())
        for s in state_list:
            if s.color != 'red':
                return False
        return True

    def run_EDSM_learner(self):
        current_number_of_states = len(self.pta.G.graph.keys())
        if self.is_all_states_red() or current_number_of_states <= (self.number_of_states_in_PTA/3):
            print("number of states in the PTA is less than half of the original number of states")
            print("states in the PTA: ", self.number_of_states_in_PTA)
            print("states in the partial automata: ", current_number_of_states)
            return

        self.found_blue = False
        self.blue_states = []
        self.visited = []
        # self.pick_next_blue(self.pta.G.initial_state)
        self.update_blue_states()
        write_to_file_in_new_line(self.edsm_file_name, f'BLUE_STATES: {self.blue_states}')
        # self.draw()
        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states=[]
        blue=None
        valid_for_at_least_one_red = False
        for blue in self.blue_states:
            write_to_file_in_new_line(self.edsm_file_name, f'RED_STATES: {self.red_states}')
            for red in self.red_states:
                write_to_file_in_new_line(self.edsm_file_name, f'RED: {red} >< BLUE: {blue} ')
                # Create a new disjoint set data structure
                ds = DisjointSet()
                ds.s1 = red
                ds.s2 = blue
                self.make_set_for_every_state_rooted_at(ds, red)
                self.make_set_for_every_state_rooted_at(ds, blue)

                # shared_labels = self.pta.G.have_shared_outgoing_transition(red, blue)
                work_to_do = {}

                add_new_state = ds.union(red, blue)
                work_to_do[ds.find(red)] = ds.get_set(red)
                if add_new_state:
                    self.compute_classes2(ds, work_to_do)
                # ds.print()
                write_to_file_in_new_line(self.edsm_file_name, ds.to_string())
                if self.is_valid_merge(ds):
                    merging_scour = self.compute_scour(ds)
                    ds.merging_scour = merging_scour
                    mergable_states.append(ds)
                    if merging_scour > 0:
                        valid_for_at_least_one_red = True
                else:
                    ds.merging_scour = -1
                write_to_file_in_new_line(self.edsm_file_name, f'merging score for {ds.s1} & {ds.s2}: {ds.merging_scour}')

            if not valid_for_at_least_one_red:
                 # the blue_state can't be merged with any red_state
                self.make_it_red(blue)
                self.make_children_blue(blue)
                break
        if valid_for_at_least_one_red:
            print(f'number of states before merge: {len(self.pta.G.graph.keys())} - threshold: {len(self.pta.G.graph.keys())/4}')
            ds_with_highest_score = self.pick_high_scour_pair(mergable_states)
            write_to_file_in_new_line(self.edsm_file_name, '***********************************************************')
            write_to_file_in_new_line(self.edsm_file_name, f'{ds_with_highest_score.s1} & {ds_with_highest_score.s2} has the highest score : {ds_with_highest_score.merging_scour}')
            write_to_file_in_new_line(self.edsm_file_name, '***********************************************************')
            print(
                f'{self.counter}- {ds_with_highest_score.s1} & {ds_with_highest_score.s2} has the highest score : {ds_with_highest_score.merging_scour}')
            self.merge_sets(ds_with_highest_score)

            # write_to_file('EDSM_Learner_tracker.txt' ,self.pta.G.to_string())
            # print(f'merge counter: {self.counter}')
            if ds_with_highest_score.s1.get_reference_state() != ds_with_highest_score.s2.get_reference_state():
                print(f'Incorrect merge: {ds_with_highest_score.s1} & {ds_with_highest_score.s2}')

            # self.pta.G.print_graph()
            self.counter +=1
            # self.draw()

        self.update_red_states()
        self.run_EDSM_learner()
    def extract_patterns_from_partial_DFA(self):
        patterns = get_all_input_sequences_with_one_output(self.pta.G, 2)
        return patterns

    def run_EDSM_with_pattern_learner(self, pattern_list):
        if self.is_all_states_red():
            return

        self.found_blue = False
        self.blue_states = []
        self.visited = []
        # self.pick_next_blue(self.pta.G.initial_state)
        self.update_blue_states()
        # print(f'BLUE_STATES: {self.blue_states}')
        write_to_file_in_new_line(self.with_pattern_file_name, f'BLUE_STATES: {self.blue_states}')
        # self.draw()
        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states=[]
        blue=None
        valid_for_at_least_one_red = False
        for blue in self.blue_states:
            # print(f'RED_STATES: {self.red_states}')
            write_to_file_in_new_line(self.with_pattern_file_name, f'RED_STATES: {self.red_states}')
            for red in self.red_states:
                # print(f'BLUE: {blue} - RED: {red}')
                # Create a new disjoint set data structure
                ds = DisjointSet()
                ds.s1 = red
                ds.s2 = blue
                self.make_set_for_every_state_rooted_at(ds, red)
                self.make_set_for_every_state_rooted_at(ds, blue)

                # shared_labels = self.pta.G.have_shared_outgoing_transition(red, blue)
                work_to_do = {}

                add_new_state = ds.union(red, blue)
                work_to_do[ds.find(red)] = ds.get_set(red)
                if add_new_state:
                    self.compute_classes2(ds, work_to_do)
                # ds.print()
                if self.is_valid_merge(ds):
                    merging_scour = self.compute_scour(ds)
                    # make a copy of the learner to check if the merge is valid with the patterns
                    # the actual merge will be done on the copy and the original will remain unchanged
                    # this way we don't have to unmerge. we just discard the copy
                    temp_learner = copy.deepcopy(self)
                    temp_learner.merge_sets(ds)
                    graph_violate_pattern, violated_patterns = violate_any_pattern2(pattern_list, temp_learner.pta.G)
                    if graph_violate_pattern:
                        print(f'Violate a Pattern: {ds.s1} & {ds.s2} => score: {merging_scour}')
                        write_to_file_in_new_line(self.with_pattern_file_name, f'Violate a Pattern: {ds.s1} & {ds.s2} => score: {merging_scour}')
                        # print(f'violated patterns:')
                        write_to_file_in_new_line(self.with_pattern_file_name, f'violated patterns:')
                        for vp in violated_patterns:
                            # print(vp)
                            write_to_file_in_new_line(self.with_pattern_file_name, f'{vp}')
                        # decrease the merging scour by 2 to avoid this merge
                        merging_scour -= 2

                    ds.merging_scour = merging_scour
                    mergable_states.append(ds)
                    if merging_scour >= 0:
                        # ds.print()
                        valid_for_at_least_one_red = True
                else:
                    ds.merging_scour = -1
                    # ds.print()

                # print(f'BLUE: {blue} - RED: {red}=> {ds.merging_scour}')
                write_to_file_in_new_line(self.with_pattern_file_name, f'BLUE: {blue} - RED: {red}=> {ds.merging_scour}')

            if not valid_for_at_least_one_red:
                 # the blue_state can't be merged with any red_state
                self.make_it_red(blue)
                self.make_children_blue(blue)
                break
                # self.draw()
        incorrect_merges = False
        if valid_for_at_least_one_red:
            ds_with_highest_scour = self.pick_high_scour_pair(mergable_states)
            print(f'{ds_with_highest_scour.s1} & {ds_with_highest_scour.s2} has the highest scour : {ds_with_highest_scour.merging_scour}')
            write_to_file_in_new_line(self.with_pattern_file_name, f'{ds_with_highest_scour.s1} & {ds_with_highest_scour.s2} has the highest scour : {ds_with_highest_scour.merging_scour}')
            if ds_with_highest_scour.s1.get_reference_state() != ds_with_highest_scour.s2.get_reference_state():
                print(f'Incorrect merge: {ds_with_highest_scour.s1} & {ds_with_highest_scour.s2}')
                write_to_file_in_new_line(self.with_pattern_file_name, f'Incorrect merge: {ds_with_highest_scour.s1} & {ds_with_highest_scour.s2}')
                incorrect_merges = True
            self.merge_sets(ds_with_highest_scour)
            # if incorrect_merges:
            # self.pta.G.print_graph()
            print(f'merge counter: {self.counter}')
            self.counter += 1
            # self.pta.G.print_graph()
            # self.draw()

        self.update_red_states()
        self.run_EDSM_with_pattern_learner(pattern_list)

    def make_it_red(self, blue_state):
        if blue_state in self.blue_states:
            self.blue_states.remove(blue_state)
            blue_state.color = 'red'
            self.red_states.append(blue_state)

    def make_children_blue(self, state):
        if isinstance(self.pta.G.graph[state], dict):
            children = self.pta.G.graph[state].keys()
            for child in children:
                if child.color != 'red':
                    child.color = 'blue'
    def update_blue_states(self):
        blue_states = []
        for red in self.red_states:
            children = self.pta.G.get_children(red)
            for child in children:
                if child.color != 'red':
                    child.color = 'blue'
                    blue_states.append(child)
        self.blue_states = blue_states

    def pick_next_blue(self, red):
            if self.found_blue:
                return
            if red in self.red_states:
                self.visited.append(red)
                # Get a list of all neighbors of the red state
                neighbors = self.pta.G.get_children(red)
                # Exclude red states
                blue_neighbors = [s for s in neighbors if s not in self.red_states]
                for s in blue_neighbors:
                    self.blue_states.append(s)

                # self.draw()
                if self.blue_states:
                    for state in self.blue_states:
                        state.color = 'blue'
                    self.found_blue = True
                else:
                    for vs in self.visited:
                        if vs in neighbors:
                            neighbors.remove(vs)
                    if red in neighbors:
                        neighbors.remove(red)
                    for neighbor in neighbors:
                        self.pick_next_blue(neighbor)  # Recursive call to explore neighbors


    def update_red_states(self):
        new_list = []
        for state in self.pta.G.get_all_states():
            if state.color == 'red':
                new_list.append(state)

        self.red_states = new_list

    def make_set_for_every_state_rooted_at(self, ds, s):
        ds.make_set(s)
        descendants = self.pta.G.get_descendants(s)
        for d in descendants:
            ds.make_set(d)

    def pick_random_state(self):
        # Get a list of all nodes (states) in the graph
        all_states = list(self.apta.G.nodes())
        # Exclude red states
        non_red_states = [s for s in all_states if self.apta.G.nodes[s].get('fillcolor') != 'red']
        # Pick a random state from the list
        random_state = random.choice(non_red_states)

        return random_state

    def is_valid_merge(self, ds):
        all_sets = ds.get_sets()
        for representative, _set in all_sets.items():
            type_compatible, list_type = self.is_compatible_type(_set)
            input_compatible = self.is_input_compatible(_set)
            if not type_compatible or not input_compatible:
                return False
        return True

    def compute_scour(self, ds):
        merging_scour = 0
        states_count_before_merge = 0
        states_count_after_merge = 0
        all_sets = ds.get_sets()
        for representative, elements in all_sets.items():
            states_count_before_merge += len(elements)
            states_count_after_merge +=1

        merging_scour = states_count_before_merge - states_count_after_merge -1
        return merging_scour

    def compute_score_with_patterns(self, ds, pattern_list):
        merging_score = 0
        states_count_before_merge = 0
        states_count_after_merge = 0
        all_sets = ds.get_sets()
        for representative, elements in all_sets.items():
            states_count_before_merge += len(elements)
            states_count_after_merge +=1

        merging_score = states_count_before_merge - states_count_after_merge -1
        if violate_any_pattern2(pattern_list, self.pta.G, self.red_states):
            print('VALID merge was BLOCKED')
            merging_score = -2
        return merging_score
    def merge_sets(self, ds):
        sets = ds.get_sets()
        for set in sets.items():
            represinitive, states = set
            if len(states)>1:
                self.merge_states(represinitive, states)

    def merge_states(self, target, merge_list):
        graph_before_merge = copy.deepcopy(self.pta.G)
        list_type = self. get_list_type(merge_list)
        if any (state.color == 'red' for state in merge_list):
            target.color = 'red'
        merge_list.remove(target)

        for i in range(0, len(merge_list)):
            source = merge_list[i]
            self.transfer_out_edge(source, target)
            self.transfer_in_coming_edges(source, target)

            if source == self.pta.G.initial_state:
                self.pta.G.initial_state = target
            if source != target:  # this if to solve butterfly problem
                self.pta.G.delete_state(source)
                target.type = list_type
        # check if the graph is disconnected after the merge
        if self.pta.G.is_disconnected():
            print(f'Graph is disconnected after merging {target} with {merge_list}')
        #     compare the graph before and after the merge



        return target

    def transfer_out_edge(self, source, target):
        if source == target:
            return
        # mylist is temp list to make a copy of the out_edges list
        source_out_edges = self.pta.G.get_outgoing_transitions_for_state(source)

        for e in source_out_edges:
            target_out_edges = self.pta.G.get_outgoing_transitions_for_state(target)
            if self.is_in_target_out_edges(e, target_out_edges):
                continue
            temp_lbl = e.label

            # if the edge is a self loop in the source state move it to the target state
            if e.is_self_loop():
                self.pta.G.add_transition(target, target, temp_lbl)

            else:
                self.pta.G.add_transition(target, e.to_state, temp_lbl)

            self.pta.G.delete_Transition(e)

    def is_in_target_out_edges(self, edge_tuple, edges_list):
        for e in edges_list:
            # if both edges have the same label
            if e.label == edge_tuple.label:
                return True
        return False


    def transfer_in_coming_edges(self, source, target):
        source_incoming_transitions = self.pta.G.get_incoming_transitions(source)

        for e in source_incoming_transitions:
            temp_lbl = e.label
            if not self.pta.G.has_incoming_transition_label(target, e):
                self.pta.G.add_transition(e.from_state, target, temp_lbl)
            self.pta.G.delete_Transition(e)

    def is_input_compatible(self, states_list):
        outgoing_transitions_list = self.pta.G.get_outgoing_transitions_for_list_of_states(None, states_list)
        input_dict = {}
        for transition in outgoing_transitions_list:
            if transition.input not in input_dict:
                input_dict[transition.input] = set()
            input_dict[transition.input].add(transition.output)

        for input, output in input_dict.items():
            if len(output) > 1:
                return False
        return True

    # is_compatible_type: boolean
    # return true is s1 and s2 of the same type or at least of them is unlabeled
    # return false if one is rejected the other is accepted
    def is_compatible_type(self, list):
        compatible = False
        list_type = 'unlabeled'
        if any (state.type == 'rejected' for state in list):
            if any(state.type == 'accepted' for state in list):
                # some rejected and some accepted
                compatible = False
            else: # at least one is rejected and all other are unlabeled
                compatible = True
                list_type = 'rejected'
        elif any(state.type == 'accepted' for state in list):
            # some are accepted and non are rejected
            list_type = 'accepted'
            compatible = True
        else:
            # all unlabeled
            compatible = True
            list_type = 'unlabeled'

        return compatible, list_type

    def get_list_type(self, merge_list):
        _c, typ = self.is_compatible_type(merge_list)
        return typ

    def pick_high_scour_pair(self, list_of_mergable_states):# list of disjoint_sets object
        # Sort the list of lists based on the merging_scour (3rd item)
        list_of_mergable_states.sort(key=lambda x: x.merging_scour, reverse=True)

        # pick up the pair with the highest scour
        ds_with_highest_scour = list_of_mergable_states.pop(0)

        return ds_with_highest_scour

    # def add_child(self, red, blue, b_child):
    #     transitions = self.apta.get_transitions_between_states(blue,b_child)
    #     for label in transitions:
    #         self.apta.add_edge(red, b_child, label)

    # def draw(self):
    #     temp_color = self.apta.G.nodes[self.apta.root]['fillcolor']
    #     self.apta.G.nodes[self.apta.root]['fillcolor'] = 'green'
    #     p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
    #     p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
    #     p.write_png(f'output/figure{FSM.figure_num:02d}.png')
    #     FSM.figure_num+=1
    #     self.apta.G.nodes[self.apta.root]['fillcolor'] = temp_color
    #
    # def draw2(self, outputfile):
    #     temp_color = self.apta.G.nodes[self.apta.root]['fillcolor']
    #     self.apta.G.nodes[self.apta.root]['fillcolor'] = 'green'
    #     p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
    #     p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
    #     p.write_png(f'output/{outputfile}.png')
    #     FSM.figure_num+=1
    #     self.apta.G.nodes[self.apta.root]['fillcolor'] = temp_color

    def compute_classes2(self,ds ,work_to_do):
        add_something_new = False
        go_agin = False
        updated_work_to_do= work_to_do.copy()
        for represitative, set_to_merge in work_to_do.items():
            checked_lables = []
            for s1 in set_to_merge:
                current_state_out_transitions = self.pta.G.get_outgoing_transitions_for_state(s1)
                other_state_out_transitions = self.pta.G.get_outgoing_transitions_for_list_of_states(s1, set_to_merge)
                for s1_trans in current_state_out_transitions:
                    label = s1_trans.label
                    if label not in checked_lables:
                        checked_lables.append(label)
                        for other_state_out_trans in other_state_out_transitions:
                            if label == other_state_out_trans.label:
                                s1_target_state = s1_trans.to_state
                                s2_target_state = other_state_out_trans.to_state
                                add_something_new = ds.union(s1_target_state, s2_target_state)
                                updated_work_to_do[ds.find(s1_target_state)] = ds.get_set(s1_target_state)
                                if add_something_new:
                                    go_agin = True
        if go_agin:
            self.compute_classes2(ds, updated_work_to_do)


    #
    # def merge_if_sharing_incoming_transition(self, state1, state2): # state1: an internal state, state2: a leaf
    #     merged = False
    #     s1_incoming_transitions = self.apta.get_in_edges(state1)
    #     s2_incoming_transitions = self.apta.get_in_edges(state2)
    #     for s2_inTrans in s2_incoming_transitions:
    #         for s2_inTrans in s1_incoming_transitions:
    #             if self.apta.get_edge_label(s2_inTrans) == self.apta.get_edge_label(s2_inTrans):
    #                 self.merge_states(state1, [state1, state2])
    #                 merged = True
    #                 break
    #         if merged:
    #             break
    #     return merged