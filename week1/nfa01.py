import sys
import queue
class NFA:
    def __init__(self, states, start_state, accepting_states):
        self.states = states
        self.start_state = start_state
        self.q = queue.Queue()

    def exploreSons(self, current_state, s):
            if ( isinstance(current_state.nextState(s), list) ):
                for listValue in current_state.nextState(s):
                    self.q.put([listValue,s])
            else:
                self.q.put([current_state.nextState(s),s])
    def accepts(self, pattern):
        current_state = self.start_state
        for s in pattern:
            print(s)
            current_state_data = []
            while True:

                self.exploreSons(current_state,s)
                current_state_data = self.q.get()
                print(str(current_state_data))
                current_state = current_state_data[0]
                if self.q.empty() or current_state_data[1] != s:
                    break
                input()
        return current_state.is_accepting


class State:
    def __init__(self, is_accepting):
        self.is_accepting = is_accepting
        self.next_states = {}

    def nextState(self, symbol):
        return self.next_states[symbol]


q0 = State(False)
q1 = State(False)
q2 = State(True)

q0.next_states = {'0': [q0,q1], '1': q0}
q1.next_states = {'1': q2}
q2.next_states = {}

nfa = NFA((q0,q1,q2),q0,(q2))

p1 = sys.argv[1]
if nfa.accepts(p1):
    print("NFA accepted %s" % p1)
else:
    print("NFA didn't accept %s" % p1)
