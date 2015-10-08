class StateMachine:
    def __init__(self, state):
        self.current_state = state

    def update(self, message_text):
        self.current_state.update(message_text)
