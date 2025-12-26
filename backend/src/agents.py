"""
Mock agents module to allow the backend to start.
This provides the necessary classes/functions that the code expects.
"""

class Agent:
    def __init__(self, name, model, tools, instructions):
        self.name = name
        self.model = model
        self.tools = tools
        self.instructions = instructions

class Runner:
    @staticmethod
    async def run(starting_agent, input):
        # This is a mock implementation
        # In the real implementation, this would run the agent with the given input
        class MockResult:
            def __init__(self):
                self.content = "Mock response for testing purposes"
                self.tool_calls = []

        return MockResult()

class RunResult:
    def __init__(self):
        self.content = ""
        self.tool_calls = []

def function_tool(func):
    """Decorator to mark a function as a tool"""
    func.is_tool = True
    return func

class AsyncOpenAI:
    def __init__(self, api_key, base_url, default_headers=None):
        self.api_key = api_key
        self.base_url = base_url
        self.default_headers = default_headers

class OpenAIChatCompletionsModel:
    def __init__(self, openai_client, model):
        self.openai_client = openai_client
        self.model = model

class RunConfig:
    def __init__(self, model, model_provider):
        self.model = model
        self.model_provider = model_provider