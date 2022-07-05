from DFA import DFA
from NFA import NFA


if __name__ == "__main__":
    states = ["A", "B", "C", "D"]
    alphabets = ["a", "b", "c"]
    init_state = "A"
    final_states = ["D"]
    transition_func = [
        ["A", "a", "A"], ["A", "e", "B"], ["A", "e", "C"],
        ["B", "b", "B"], ["B", "b", "D"],
        ["C", "c", "C"], ["C", "c", "D"]
    ]

    nfa = NFA(states, alphabets, init_state, final_states, transition_func)
    nfa.draw_graph()
