"""
Agno Package Examples - Combined Hello World and Stub Model

This file demonstrates two simple Agno agent examples:
1. Simple Hello World Agent - Basic agent that echoes user input
2. Agent with Stub Model - Agent using a custom model implementation
"""

from agno.agent import Agent
from agno.models.base import Model

# Example 1: Simple Hello World Agent
class SimpleAgent(Agent):
    """A simple agent that greets users and echoes their input."""
    
    def run(self, input, **kwargs):
        """
        Process user input and return a greeting message.
        
        Args:
            input: The user's input message
            **kwargs: Additional keyword arguments
            
        Returns:
            A greeting message that includes the user's input
        """
        return f"Hello world! You said: {input}"

# Example 2: Agent with Stub Model
class StubMessage:
    """A stub message class that mimics the Agno Message interface."""
    
    def __init__(self, **kwargs):
        """
        Initialize a stub message with common attributes.
        
        Args:
            **kwargs: Message attributes (role, content, tool_calls, etc.)
        """
        self.role = kwargs.get("role", "assistant")
        self.content = kwargs.get("content", "Hello world")
        self.tool_calls = kwargs.get("tool_calls", [])
        self.audio = kwargs.get("audio", None)
        self.images = kwargs.get("images", None)
        self.metadata = kwargs.get("metadata", {})

    def __getattr__(self, name):
        """Return None for any undefined attributes."""
        return None

class SimpleModel(Model):
    """
    A simple stub model that returns predefined responses.
    """
    
    def __init__(self):
        """Initialize the stub model with a dummy ID."""
        super().__init__(id="dummy-model")

    def invoke(self, *args, **kwargs):
        """
        Synchronous invocation that returns a stub message.
        
        Returns:
            StubMessage: A predefined message response
        """
        return StubMessage()

    def invoke_stream(self, *args, **kwargs):
        """
        Synchronous streaming invocation that yields a stub message.
        
        Yields:
            StubMessage: A predefined message response
        """
        yield StubMessage()

    async def ainvoke(self, *args, **kwargs):
        """
        Asynchronous invocation that returns a stub message.
        
        Returns:
            StubMessage: A predefined message response
        """
        return StubMessage()

    async def ainvoke_stream(self, *args, **kwargs):
        """
        Asynchronous streaming invocation that yields a stub message.
        
        Yields:
            StubMessage: A predefined message response
        """
        yield StubMessage()

    def _parse_provider_response(self, response):
        """
        Parse provider response (stub implementation).
        
        Args:
            response: The response to parse
            
        Returns:
            The response unchanged
        """
        return response

    def _parse_provider_response_delta(self, delta):
        """
        Parse provider response delta (stub implementation).
        
        Args:
            delta: The delta to parse
            
        Returns:
            The delta unchanged
        """
        return delta

# Main Execution
def main():
    """Run both examples and display results."""
    
    print("=" * 70)
    print("Example 1: Simple Hello World Agent")
    print("=" * 70)
    
    # Create and run the simple agent
    simple_agent = SimpleAgent()
    result1 = simple_agent.run("test")
    print(f"Input: 'test'")
    print(f"Output: {result1}")
    print()
    
    print("=" * 70)
    print("Example 2: Agent with Stub Model")
    print("=" * 70)
    
    # Create an agent with the stub model
    agent_with_model = Agent(model=SimpleModel())
    result2 = agent_with_model.run("Test input")
    print(f"Input: 'Test input'")
    print(f"Output: {result2.content}")
    print()
    
    print("=" * 70)
    print("Both examples completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
