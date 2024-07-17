import copy
import random
import networkx as nx

from Utilities.DISJOINTSETS import DisjointSet
from Utilities.PTA import PTA

class EDSM:
    figure_num = 2
    def __init__(self, pta:PTA):
        self.pta = pta

        red = self.pta.G.initial_state
        # self.apta.set_color(red, 'red')
        self.red_states = [red]

        self.found_blue=False
        self.visited=[]
        self.blue_states=[]

    def is_all_states_red(self):
        state_list = list(self.pta.G.graph.keys())
        return self.red_states == state_list

    def run_EDSM_learner(self):
        if self.is_all_states_red():
            return

        self.found_blue = False
        self.blue_states = []
        self.visited = []
        self.pick_next_blue(self.pta.G.initial_state)
        # print(f'BLUE_STATES: {self.blue_states}')
        # self.draw()
        # mergable_states is  a list contains all pairs of state that are valid to be merged with their merging scour
        mergable_states=[]
        blue=None
        valid_for_at_least_one_red = False
        for blue in self.blue_states:
            for red in self.red_states:
                # print(f'BLUE: {blue} - RED: {red}')
                # Create a new disjoint set data structure
                ds = DisjointSet()
                ds.s1 = red
                ds.s2 = blue
                self.make_set_for_every_state_rooted_at(ds, red)
                self.make_set_for_every_state_rooted_at(ds, blue)

                shared_labels = self.pta.G.have_shared_outgoing_transition(red, blue)
                work_to_do = {}
                if shared_labels:
                    add_new_state = ds.union(red, blue)
                    work_to_do[ds.find(red)] = ds.get_set(red)
                    if add_new_state:
                        self.compute_classes2(ds,work_to_do)

                if self.is_valid_merge(ds):
                    merging_scour = self.compute_scour(ds)
                    ds.merging_scour = merging_scour
                    mergable_states.append(ds)
                    if merging_scour > 0:
                        # ds.print()
                        valid_for_at_least_one_red = True
                    # print(f'merging scour for {red} & {blue}: {merging_scour}')
                else:
                    ds.merging_scour = -1
                    # ds.print()

        if not valid_for_at_least_one_red:
             # the blue_state can't be merged with any red_state
            # print(f'{blue} cannot be merged with any red_state')
            self.apta.set_color(blue, 'red') # make it red
            self.red_states.append(blue) #addit to red_states list
            # self.draw()
        else:
            ds_with_highest_scour = self.pick_high_scour_pair(mergable_states)
            # print(f'{ds_with_highest_scour.s1} & {ds_with_highest_scour.s2} has the highest scour : {ds_with_highest_scour.merging_scour}')
            self.merge_sets(ds_with_highest_scour)
            # self.draw()

        self.update_red_states()
        self.run_EDSM_learner()


    def pick_next_blue(self, red):
            if self.found_blue:
                return
            if red in self.red_states:
                self.visited.append(red)
                # Get a list of all neighbors of the red state
                neighbors = self.pta.G.get_children(red)
                # Exclude red states
                self.blue_states = [s for s in neighbors if s not in self.red_states]

                # self.draw()
                if self.blue_states:
                    self.found_blue = True
                    return
                else:
                    for vs in self.visited:
                        if vs in neighbors:
                            neighbors.remove(vs)
                    if red in neighbors:
                        neighbors.remove(red)
                    for neighbor in neighbors:
                        self.pick_next_blue(neighbor)  # Recursive call to explore neighbors

    def make_leaves_red(self):
        for state in self.apta.G.nodes:
            if self.apta.is_leaf(state):
                self.apta.set_color(state, 'red')

    def update_red_states(self):
        new_list = []
        for state in self.apta.G.nodes:
            if self.apta.is_red(state) and not self.apta.is_leaf(state):
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

    def compute_classes(self, ds, red, blue):
        if self.apta.is_leaf(red) or self.apta.is_leaf(blue):
            return
        have_shared_transition, shared_labels = self.have_shared_outgoing_transition(red, blue)
        if (have_shared_transition):
            ds.union(red, blue)

            for shared_label in shared_labels:
                blue_child = self.apta.get_child_nodes_with_label(blue, shared_label)
                red_child = self.apta.get_child_nodes_with_label(red, shared_label)
                ds.union(red_child,blue_child)
                self.compute_classes(ds, red_child, blue_child)
                if not ds.is_representative(red_child):
                    representative = ds.find(red_child)
                    self.compute_classes(ds, representative, blue_child)

    def is_valid_merge(self, ds):
        all_sets = ds.get_sets()
        for representative, _set in all_sets.items():
            compatible, list_type = self.is_compatible_type(_set)
            if not compatible:
                return False
        return True

    def compute_scour(self, ds):
        # merging_scour = 0
        # states_before_merge = self.apta.G.number_of_nodes()
        # backup = copy.deepcopy(self.apta)
        # self.merge_sets(ds)
        # states_after_merge = self.apta.G.number_of_nodes()
        # self.apta = backup
        # if states_before_merge != states_after_merge:
        #     merging_scour = states_before_merge - states_after_merge -1
        # return merging_scour
        merging_scour = 0
        all_sets = ds.get_sets()
        for representative, elements in all_sets.items():
            if len(elements)>1:
                merging_scour += (len(elements)-1)

        return merging_scour -1





    def merge_sets(self, ds):
        sets = ds.get_sets()
        for set in sets.items():
            represinitive, states = set
            if len(states)>1:
                self.merge_states(represinitive, states)

    def merge_states(self, target, merge_list):
        list_type = self. get_list_type(merge_list)
        if any (self.apta.get_color(state) == 'red' for state in merge_list):
            self.apta.set_color(target, 'red')
        merge_list.remove(target)

        for i in range(0, len(merge_list)):
            source = merge_list[i]
            self.transfer_out_edge(source, target)
            self.transfer_in_coming_edges(source, target)

            if source == self.apta.root:
                self.apta.root = target
            if source != target:  # this if to solve butterfly problem
                self.apta.delete_state(source)
            self.apta.set_state_type(target,list_type)
        return target

    def transfer_out_edge(self, source, target):
        if source == target:
            return
        # mylist is temp list to make a copy of the out_edges list
        source_out_edges = copy.deepcopy(self.apta.get_out_edges(source))

        for e in source_out_edges:
            target_out_edges = copy.deepcopy(self.apta.get_out_edges(target))
            if self.is_in_target_out_edges(e, target_out_edges):
                continue
            temp_lbl = self.apta.get_edge_label(e)
            self.apta.delete_edge(e)
            # if the edge is a self loop in the source state move it to the target state
            if e[0] == e[1]:
                self.apta.add_edge(target, target, temp_lbl)

            else:
                self.apta.add_edge(target, e[1], temp_lbl)

    def is_in_target_out_edges(self, edge_tuple, edges_list):
        for e in edges_list:
            # if both edges have the same label
            if self.apta.get_edge_label(e) == self.apta.get_edge_label(edge_tuple):
                return True
        return False

    def is_self_loop(self, edge_tuple):
        return edge_tuple[0] == edge_tuple[1]

    def transfer_in_coming_edges(self, source, target):
        copylist = copy.deepcopy(self.apta.get_in_edges(source))

        for e in copylist:
            temp_lbl = self.apta.get_edge_label(e)
            if not self.apta.has_in_edge(target, e):
                self.apta.add_edge(e[0], target, temp_lbl)
            self.apta.delete_edge(e)

    # is_compatible_type: boolean
    # return true is s1 and s2 of the same type or at least of them is unlabeled
    # return false if one is rejected the other is accepted
    def is_compatible_type(self,list):
        compatible = False
        list_type = 'unlabeled'
        if any (self.apta.get_state_type(state) == 'rejected' for state in list):
            if any(self.apta.get_state_type(state) == 'accepted' for state in list):
                # some rejected and some accepted
                compatible = False
            else: # at least one is rejected and all other are unlabeled
                compatible = True
                list_type = 'rejected'
        elif any(self.apta.get_state_type(state) == 'accepted' for state in list):
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
    def add_child(self, red, blue, b_child):
        transitions = self.apta.get_transitions_between_states(blue,b_child)
        for label in transitions:
            self.apta.add_edge(red, b_child, label)

    def draw(self):
        temp_color = self.apta.G.nodes[self.apta.root]['fillcolor']
        self.apta.G.nodes[self.apta.root]['fillcolor'] = 'green'
        p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
        p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
        p.write_png(f'output/figure{FSM.figure_num:02d}.png')
        FSM.figure_num+=1
        self.apta.G.nodes[self.apta.root]['fillcolor'] = temp_color

    def draw2(self, outputfile):
        temp_color = self.apta.G.nodes[self.apta.root]['fillcolor']
        self.apta.G.nodes[self.apta.root]['fillcolor'] = 'green'
        p = nx.nx_agraph.pygraphviz_layout(self.apta.G, prog='dot')
        p = nx.drawing.nx_pydot.to_pydot(self.apta.G)
        p.write_png(f'output/{outputfile}.png')
        FSM.figure_num+=1
        self.apta.G.nodes[self.apta.root]['fillcolor'] = temp_color

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


    def merge_remaining_leaves(self):
        leaves = []
        for node in self.apta.G.nodes:
            if self.apta.is_leaf(node):
                leaves.append(node)
        print(f'Leaves: {leaves}')
        for leaf in leaves:
            merged = False
            print(f'leaf: {leaf}')
            leaf_type = self.apta.get_state_type(leaf)
            print(f'leaf_type: {leaf_type}')
            siblings = self.apta.get_siblings(leaf)
            print(f'try siblings: {siblings}')
            for sib in siblings:
                if self.apta.get_state_type(sib) == leaf_type:
                    self.merge_states(sib, [sib, leaf])
                    merged = True
                    print(f'merged with: {sib}')
                    break
            if not merged:
                # try to merge it with a parent
                parent_nodes = list(self.apta.G.predecessors(leaf))
                print(f'try parents: {parent_nodes}')
                for parent in parent_nodes:
                    print(f'parent: {parent}')
                    compatible, _t = self.is_compatible_type([parent, leaf])
                    if not compatible:
                        continue
                    elif self.apta.get_state_type(parent) == leaf_type:
                        self.merge_states(parent, [parent, leaf])
                        merged = True
                        print(f'merged with: {parent}')
                    else:
                        merged = self.merge_if_sharing_incoming_transition(parent, leaf)
                        print(f'merged with: {parent}')
                    if merged:
                        break
            if not merged:
                # try to merge it with any compatible state
                # first: try states of the same type
                # then: try unlabeled states with sharing incoming transition

                # Get a list of all nodes (states) in the graph
                all_states = self.apta.G.nodes
                # filttering states to include just intranal states with the sae type of the leaf
                same_type_states = [s for s in all_states if self.apta.get_state_type(s) == leaf_type and not self.apta.is_leaf(s)]
                print(f'try any same type:{same_type_states}')
                if same_type_states:
                    self.merge_states(same_type_states[0], [same_type_states[0], leaf])
                    merged = True
                else:
                    unlabeled_states = [s for s in all_states if
                                        self.apta.get_state_type(s) == 'unlabeled' and not self.apta.is_leaf(s)]
                    print(f'try any unlabeled: {unlabeled_states}')
                    for unlabeled_s in unlabeled_states:
                        merged = self.merge_if_sharing_incoming_transition(unlabeled_s, leaf)
                        if merged:
                            break

    def merge_if_sharing_incoming_transition(self, state1, state2): # state1: an internal state, state2: a leaf
        merged = False
        s1_incoming_transitions = self.apta.get_in_edges(state1)
        s2_incoming_transitions = self.apta.get_in_edges(state2)
        for s2_inTrans in s2_incoming_transitions:
            for s2_inTrans in s1_incoming_transitions:
                if self.apta.get_edge_label(s2_inTrans) == self.apta.get_edge_label(s2_inTrans):
                    self.merge_states(state1, [state1, state2])
                    merged = True
                    break
            if merged:
                break
        return merged