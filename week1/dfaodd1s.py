import sys

class DFA:
    def __init__(self, states, start_state, accepting_states):
        self.states = states
        self.start_state = start_state

    def accepts(self, pattern):
        current_state = self.start_state

        for s in pattern:
            current_state = current_state.nextState(s)

        return current_state.is_accepting


class State:
    def __init__(self, is_accepting):
        self.is_accepting = is_accepting
        self.next_states = {}

    def nextState(self, symbol):
        return self.next_states[symbol]


s1 = State(False)
s2 = State(True)

s1.next_states = {'0': s1, '1': s2}
s2.next_states = {'0': s2, '1': s1}

dfa = DFA((s1,s2),s1,(s2))

p1 = sys.argv[1]
if dfa.accepts(p1):
    print("DFA accepted %s" % p1)
else:
    print("DFA didn't accept %s" % p1)