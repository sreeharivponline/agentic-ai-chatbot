# memory.py

class Memory:
    def __init__(self):
        """Initializes the memory with an empty history."""
        self.history = []

    def add(self, thought: str, action: str, observation: str):
        """
        Adds a new entry to the agent's memory history.

        Args:
            thought (str): The agent's internal thought process.
            action (str): The action the agent performed.
            observation (str): The result or observation from the action.
        """
        self.history.append({
            "thought": thought,
            "action": action,
            "observation": observation
        })

    def get_context(self) -> str:
        """
        Retrieves the entire memory history formatted as a single string.
        Useful for providing context to an LLM or for debugging.
        """
        return "\n".join([
            f"Thought: {h['thought']}\nAction: {h['action']}\nObservation: {h['observation']}"
            for h in self.history
        ])