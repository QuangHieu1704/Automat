import numpy as np
import re
from graphviz import Digraph
from DFA import DFA
from itertools import combinations

from DFA import dfa_minimization

class NFA:
    def __init__(self, states, alphabets, init_state, final_states, transition_func):
        self.states = states    # list
        self.alphabets = alphabets   # list 
        self.init_state = init_state  # string
        self.final_states = final_states   # list  
        self.transition_func = transition_func # dict


    def get_to_state(self, curr_state, value):
        for k1, v1 in self.transition_func.items():
            if k1 == curr_state:
                for k2, v2 in v1.items():
                    if value == str(k2):
                        return v2
        return None

    def draw_graph(self):
        graph = Digraph(format = "svg")
        graph.attr('node', shape='point')
        graph.node('qi')
        for state in self.states:
            if state in self.final_states:
                graph.attr("node", shape = "doublecircle", color = "green", style = "")
            elif state in self.init_state:
                graph.attr("node", shape = "circle", color = "black", style = "")
            else:
                graph.attr("node", shape = "circle", color = "black", style = "")
            graph.node(str(state))

            if state in self.init_state:
                graph.edge('qi', str(state), "start")
        for curr_state, trans_func in self.transition_func.items():
            for value, new_states in trans_func.items():
                for state in new_states:
                    graph.edge(str(curr_state), str(state), label = str(value))

        graph.render('{0}'.format("NFA"), view=True)


def nfa_to_dfa(nfa):
    dfa_states = []
    dfa_alphabets = nfa.alphabets
    dfa_init_state = nfa.init_state
    dfa_final_states = []
    dfa_transition_func = {}

    list_combinations = list()
    states_set = set(nfa.states)
    for n in range(len(states_set) + 1):
        list_combinations += list(combinations(states_set, n))
    list_combinations = [list(item) for item in list_combinations]
    list_combinations.remove([])

    is_empty_state = False

    for working_state in list_combinations:
        working_state.sort()

        dfa_new_state = ""
        is_final_state = False
        for state in working_state:
            dfa_new_state += str(state)
            if state in nfa.final_states:
                is_final_state = True
        if is_final_state:
            dfa_final_states.append(dfa_new_state)
        dfa_states.append(dfa_new_state)

        sub_trans_func = {}
        for char in dfa_alphabets:
            dist_states = list()
            for state in working_state:
                new_state = nfa.get_to_state(state, char)
                dist_states.extend(new_state)
            dist_states = list(dict.fromkeys(dist_states))

            if "@" in dist_states and len(dist_states) > 1:
                dist_states.remove("@")

            if "@" in dist_states:
                is_empty_state = True

            dist_states.sort()
            trans_state = ""
            for s in dist_states:
                trans_state += str(s)
            sub_trans_func[char] = trans_state
        dfa_transition_func[dfa_new_state] = sub_trans_func

    if is_empty_state:
        sub_empty_trans = {}
        for char in dfa_alphabets:
            sub_empty_trans[char] = "@"
        dfa_transition_func["@"] = sub_empty_trans
        dfa_states.append("@")
    
    # print("DFA alphabets", dfa_alphabets)
    # print("DFA states: ", dfa_states)
    # print("DFA init state: ", dfa_init_state)
    # print("DFA final states: ", dfa_final_states)
    # print("DFA transition func", dfa_transition_func)

    # Remove error state
    remove_states = []
    for state in dfa_states:
        count_access = 0
        # Check if state don't have any coming state
        for curr_state, trans in dfa_transition_func.items():
            for k, v in trans.items():
                if v == state:
                    count_access += 1
        if count_access == 0 and state != dfa_init_state:
            remove_states.append(state)
    
    for del_state in remove_states:
        dfa_states.remove(del_state)
        dfa_final_states.remove(del_state)
        del dfa_transition_func[del_state]

    dfa_states.remove("@")
    new_trans_func = {}
    for k1, v1 in dfa_transition_func.items():
        if k1 != "@":
            tmp_dict = {}
            for k2, v2 in v1.items():
                if v2 != "@":
                    tmp_dict[k2] = v2
            new_trans_func[k1] = tmp_dict
    dfa_transition_func = new_trans_func

    dfa = DFA(dfa_states, dfa_alphabets, dfa_init_state, dfa_final_states, dfa_transition_func)

    return dfa
