from turtle import write_docstringdict
import numpy as np
import re
from graphviz import Digraph

class DFA:
    def __init__(self, states, alphabets, init_state, final_states, transition_func):
        self.states = states    # list
        self.alphabets = alphabets   # list 
        self.init_state = init_state  # string
        self.final_states = final_states   # list  
        self.transition_func = transition_func # dictionary


    def accepts(self, str):
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


    def get_to_state(self, curr_state, value):
        for k1, v1 in self.transition_func.items():
            if k1 == curr_state:
                for k2, v2 in v1.items():
                    if value == str(k2):
                        return str(v2)
        return None


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

    def check_pair_final(self, state1, state2):
        if (state1 in self.final_states and state2 not in self.final_states) or (state2 in self.final_states and state1 not in self.final_states):
            return True
        
        return False


    def dfa_minimization(self):
        working_states = []
        new_states = []
        # Remove unreachable state
        reachable_state, unreachable_state = self.get_unreachable_state()
        working_states.extend(reachable_state)
        # Step 2

        size = len(working_states)
        marking_arr = np.zeros(shape = (size, size), dtype = np.int32)
        for i in range(0, size):
            for j in range(i + 1, size):
                if self.check_pair_final(working_states[i], working_states[j]):
                    marking_arr[i][j] = 1
        for i in range(0, size):
            for j in range(i + 1, size):
                if marking_arr[i][j] == 0:
                    for char in self.alphabets:
                        p_x = self.get_to_state(working_states[i], char)
                        q_x = self.get_to_state(working_states[j], char)
                        i_p_x = working_states.index(p_x)
                        i_q_x = working_states.index(q_x)
                        if marking_arr[i_p_x][i_q_x] == 1:
                            marking_arr[i][j] = 1

        return marking_arr


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


if __name__ == "__main__":
    states = ["1", "2", "3", "4", "5", "6"]
    alphabets = ["a", "b"]
    init_state = "1"
    final_states = ["2", "3", "6"]
    transition_func = {
            "1": {"a": "2", "b": "3"},
            "2": {"a": "4", "b": "5"},
            "3": {"a": "5", "b": "4"},
            "4": {"a": "6", "b": "6"},
            "5": {"a": "6", "b": "6"},
            "6": {"a": "6", "b": "6"}
        }

    dfa = DFA(states, alphabets, init_state, final_states, transition_func)
    print(dfa.dfa_minimization())
    # dfa.draw_graph()

    # str = "0110"
    # print(dfa.accepts(str))