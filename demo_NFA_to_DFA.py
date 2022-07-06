from DFA import DFA
from NFA import NFA, nfa_to_dfa


if __name__ == "__main__":
    states = ["p0", "p1", "p2"]
    alphabets = ["a", "b", "c"]
    init_state = "p0"
    final_states = ["p1", "p2"]
    transition_func = {
        "p0": {"a": ["p1"], "b": ["p1", "p2"], "c": ["p2"]},
        "p1": {"a": ["p2"], "b": ["@"], "c": ["p0", "p2"]},
        "p2": {"a": ["p1"], "b": ["p1"], "c": ["p2"]}
    }
    nfa = NFA(states, alphabets, init_state, final_states, transition_func)
    dfa = nfa_to_dfa(nfa)
    dfa.draw_graph()
