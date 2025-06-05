# report_tool.py

from memory import Memory # Assuming memory.py is in the same directory

def generate_report(memory: Memory) -> str:
    """
    Generates a structured report based on the agent's memory history.

    Args:
        memory (Memory): An instance of the Memory class containing the agent's history.

    Returns:
        str: A Markdown-formatted string representing the agent's activity report.
    """
    report = "📝 **Agentic Chatbot Activity Report**\n\n"
    if not memory.history:
        report += "No activity recorded in memory yet."
        return report

    for i, step in enumerate(memory.history):
        report += f"**Step {i+1}**\n"
        report += f"- **Thought:** {step.get('thought', 'N/A')}\n"
        report += f"- **Action:** {step.get('action', 'N/A')}\n"
        report += f"- **Observation:** {step.get('observation', 'N/A')}\n\n"
    return report