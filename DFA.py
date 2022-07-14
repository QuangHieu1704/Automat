import numpy as np
import re
from graphviz import Digraph

class DFA:
    def __init__(self, states, alphabets, init_state, final_states, transition_func):
        self.states = states    # list
        self.alphabets = alphabets   # list 
        self.init_state = init_state  # string
        self.final_states = final_states   # list  
        self.transition_func = transition_func # dict


    # DFA accepts string
    def accepts(self, str):
        for char in str:
            if char not in self.alphabets:
                return False
        init_state = self.init_state
        for i in range(len(str)):
            if i == 0:
                old_state = init_state
                new_state = self.transition_func[old_state][str[i]]
            else:
                old_state = new_state
                new_state = self.transition_func[old_state][str[i]]
            print(f"Get char {str[i]} Move from state {old_state} to {new_state}")

        return new_state in self.final_states


    # From a current state, travel to next state by value
    def get_to_state(self, curr_state, value):
        for k1, v1 in self.transition_func.items():
            if k1 == curr_state:
                for k2, v2 in v1.items():
                    if value == str(k2):
                        return str(v2)
        return None


    # Get unreachable state
    def get_unreachable_state(self):
        unreachable_states = []
        reachable_states = []
        new_states = []
        reachable_states.append(self.init_state)
        new_states.append(self.init_state)
        while len(new_states) != 0:
            temp = []
            for state in new_states:
                for char in self.alphabets:
                    if self.get_to_state(state, char) is not None:
                        temp.append(self.get_to_state(state, char))
            new_states = list(set(temp) - set(reachable_states))
            reachable_states.extend(new_states)
        unreachable_states = list(set(self.states) - set(reachable_states))

        return reachable_states, unreachable_states

    # Check if two states are final states or not 
    def check_pair_final(self, state1, state2):
        if (state1 in self.final_states and state2 not in self.final_states) or (state2 in self.final_states and state1 not in self.final_states):
            return True
        
        return False


    # Draw graph by graphviz
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
            for value, new_state in trans_func.items():
                graph.edge(str(curr_state), str(new_state), label = str(value))
        graph.render('{0}'.format("DFA"), view=True)


    def get_intermediate_states(self):
        active_states = []
        active_states.append(self.init_state)
        active_states.extend(self.final_states)
        return [state for state in self.states if state not in active_states]


    def get_precdecessors(self, state):
        precdecessors = []
        for curr_state, trans_func in self.transition_func.items():
            for value, next_state in trans_func.items():
                if next_state == state:
                    precdecessors.append(curr_state)
        precdecessors = list(dict.fromkeys(precdecessors))
        
        return precdecessors

    def get_successors(self, state):
        successors = []
        for curr_state, trans_func in self.transition_func.items():
            if curr_state  == state:
                for value, next_state in trans_func.items():
                    successors.append(next_state)
        successors = list(dict.fromkeys(successors))

        return successors

    def get_if_loop(self, state):
        


    def get_regex(self):
        # Handle if init state has incoming state
        has_init_incoming = False
        for curr_state, trans_func in self.transition_func.items():
            for value, next_state in trans_func.items():
                if next_state == self.init_state:
                    has_init_incoming = True
                    old_init_state = self.init_state
                    new_init_state = old_init_state + "'"
                    self.states.insert(0, new_init_state)
                    self.init_state = new_init_state
                    self.transition_func[new_init_state] = {"@": old_init_state}
                    break
            if has_init_incoming is True:
                break
        
        # Handle final outgoing state
        has_final_outgoing = False
        if len(self.final_states) > 1:
            has_final_outgoing = True
        else: 
            for curr_state, trans_func in self.transition_func.items():
                if curr_state == self.final_states[0]:
                    has_final_outgoing = True
        if has_final_outgoing:
            new_final_state = "F"
            self.states.append(new_final_states)
            old_final_states = self.final_states
            self.final_states = [new_final_state]
            for old_final in old_final_states:
                for curr_state, trans_func in self.transition_func.items():
                    if curr_state == old_final:
                        trans_func["@"] = new_final_state
        # Convert to ReGex
        intermediate_states = self.get_intermediate_states()
        for inter in intermediate_states:
            precdecessors = self.get_precdecessors(inter)
            successors = self.get_successors(inter)

            for prec in precdecessors:
                for succ in successors:
                    inter_loop = 
                    



def dfa_minimization(dfa):
    working_states = []
    # Remove unreachable state
    reachable_state, unreachable_state = dfa.get_unreachable_state()
    working_states = dfa.states
    for state in unreachable_state:
        working_states.remove(state)

    # Step 2
    size = len(working_states)
    marking_arr = np.zeros(shape = (size, size), dtype = np.int32)
    for i in range(0, size):
        for j in range(i + 1, size):
            if dfa.check_pair_final(working_states[i], working_states[j]):
                marking_arr[i][j] = 1
    # Step 3
    new_marked = 1
    while new_marked != 0:
        new_marked = 0
        for i in range(0, size):
            for j in range(i + 1, size):
                if marking_arr[i][j] == 0:
                    for char in dfa.alphabets:
                        p_x = dfa.get_to_state(working_states[i], char)
                        q_x = dfa.get_to_state(working_states[j], char)
                        i_p_x = working_states.index(p_x)
                        i_q_x = working_states.index(q_x)
                        if marking_arr[i_p_x][i_q_x] == 1:
                            marking_arr[i][j] = 1
                            new_marked += 1
    
    list_combined_state = []
    for i in range(0, size):
        temp = []
        for j in range(i + 1, size):
            if marking_arr[i][j] == 0:
                temp.append(working_states[j])
        if len(temp) != 0:
            temp.insert(0, working_states[i])
            list_combined_state.append(temp)

    
    combine_state = {}
    for pair_state in list_combined_state:
        new_state = ""
        for state in pair_state:
            new_state += str(state)
        
        for state in pair_state:
            key = state
            value = new_state
            combine_state[key] = value
    
    new_states = working_states
    new_alphabets = dfa.alphabets
    new_init_state = dfa.init_state
    new_final_states = dfa.final_states
    old_transition_func = dfa.transition_func
    new_transition_func = {}

    for old_state, new_state in combine_state.items():
        for i in range(len(new_states)):
            if new_states[i] == old_state:
                new_states[i] = new_state
    new_states = list(dict.fromkeys(new_states))

    for old_state, new_state in combine_state.items():
        if old_state == new_init_state:
            new_init_state = new_state
            break
    
    for k1, v1 in old_transition_func.items():
        for old_state1, new_state1 in combine_state.items():
            if k1 == old_state1:
                k1 = new_state1
                break
        sub_dict = {}
        for k2, v2 in v1.items():
            for old_state2, new_state2 in combine_state.items():
                if v2 == old_state2:
                    v2 = new_state2
                    break
            sub_dict[k2] = v2
        new_transition_func[k1] = sub_dict

    new_dfa = DFA(new_states, new_alphabets, new_init_state, new_final_states, new_transition_func)

    return new_dfa
