class Memory:
    def __init__(self):
        self.history = []

    def add(self, thought, action, observation):
        self.history.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })

    def get_context(self):
        return "\n".join([
            f"Thought: {h['thought']}\nAction: {h['action']}\nObservation: {h['observation']}"
            for h in self.history
        ])
