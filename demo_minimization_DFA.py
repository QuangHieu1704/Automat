import numpy as np
from DFA import DFA, dfa_minimization


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
    # dfa.draw_graph()
    new_dfa = dfa_minimization(dfa)
    new_dfa.draw_graph()
