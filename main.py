from agent.agent import Agent

agent = Agent()

while True:
    prompt = input(">>> ")
    if prompt.lower() in {"exit", "quit"}:
        break

    print(agent.run(prompt))