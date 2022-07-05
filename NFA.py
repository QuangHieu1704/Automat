import numpy as np
import re
from graphviz import Digraph
from DFA import DFA

class NFA:
    def __init__(self, states, alphabets, init_state, final_states, transition_func):
        self.states = states    # list
        self.alphabets = alphabets   # list 
        self.init_state = init_state  # string
        self.final_states = final_states   # list  
        self.transition_func = transition_func # list


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
        for transition in self.transition_func:
            graph.edge(str(transition[0]), str(transition[2]), label = str(transition[1]))
        graph.render('{0}'.format("NFA"), view=True)


def nfa_to_dfa(nfa):
    dfa_states = []
    dfa_alphabets = nfa.alphabets
    dfa_init_state = []
    dfa_final_states = []
    dfa_transition_func = {}

    dfa_states.append(nfa.init_state)

    for in_state in dfa_states:
        for char in dfa_alphabets:
            