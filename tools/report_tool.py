def generate_report(memory):
    report = "📝 **Agentic Chatbot Report**\n\n"
    for i, step in enumerate(memory.history):
        report += f"**Step {i+1}**\n"
        report += f"- Thought: {step['thought']}\n"
        report += f"- Action: {step['action']}\n"
        report += f"- Observation: {step['observation']}\n\n"
    return report
