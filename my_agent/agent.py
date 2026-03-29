from google.adk.agents.llm_agent import Agent

def isPrime(number: int) -> dict:
    """Returns whether a number is prime."""
    if number < 2:
        return {"status": "success", "number": number, "isPrime": False}
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return {"status": "success", "number": number, "isPrime": False}
    return {"status": "success", "number": number, "isPrime": True}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the number is prime or not.",
    instruction="You are a helpful assistant that tells the number is prime or not. Use the 'isPrime' tool for this purpose.",
    tools=[isPrime],
)