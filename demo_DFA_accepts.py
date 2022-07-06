import numpy as np
from DFA import DFA, dfa_minimization

if __name__ == "__main__":
    states = ["0", "1", "2", "3", "4"]
    alphabets = ["a", "b"]
    init_state = "0"
    final_states = ["3"]
    transition_func = {
            "0": {"a": "1", "b": "4"},
            "1": {"a": "2", "b": "4"},
            "2": {"a": "3", "b": "1"},
            "3": {"a": "4", "b": "4"},
            "4": {"a": "4", "b": "4"}
        }

    dfa = DFA(states, alphabets, init_state, final_states, transition_func)

    str = "aabaa"
    print(dfa.accepts(str))