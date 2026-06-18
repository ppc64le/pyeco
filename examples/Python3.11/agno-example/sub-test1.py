import unittest
import importlib.metadata

class TestAgnoExamples(unittest.TestCase):
    """Test cases for both Agno examples."""
    
    def test_agno_import(self):
        """Check if agno can be imported."""
        try:
            import agno
        except ImportError:
            self.fail("agno is not installed")

    def test_agno_version(self):
        """Verify agno version."""
        version = importlib.metadata.version("agno")
        # Check that version exists and is a valid version string
        self.assertIsNotNone(version)
        self.assertTrue(len(version) > 0)
        print(f"Agno version: {version}")

    def test_simple_agent_import(self):
        """Test that we can import the SimpleAgent."""
        try:
            from agno_example import SimpleAgent
            self.assertIsNotNone(SimpleAgent)
        except ImportError as e:
            self.fail(f"Failed to import SimpleAgent: {e}")

    def test_simple_agent_run(self):
        """Test that the SimpleAgent runs correctly."""
        from agno_example import SimpleAgent
        
        agent = SimpleAgent()
        result = agent.run("test")
        
        # Verify the result contains expected text
        self.assertIn("Hello world", result)
        self.assertIn("test", result)
        print(f"SimpleAgent output: {result}")

    def test_stub_model_import(self):
        """Test that we can import the SimpleModel and related classes."""
        try:
            from agno_example import SimpleModel, StubMessage
            self.assertIsNotNone(SimpleModel)
            self.assertIsNotNone(StubMessage)
        except ImportError as e:
            self.fail(f"Failed to import from agno_example: {e}")

    def test_stub_message_creation(self):
        """Test that StubMessage can be created with default values."""
        from agno_example import StubMessage
        
        msg = StubMessage()
        self.assertEqual(msg.role, "assistant")
        self.assertEqual(msg.content, "Hello world")
        self.assertEqual(msg.tool_calls, [])
        self.assertIsNone(msg.audio)
        self.assertIsNone(msg.images)
        self.assertEqual(msg.metadata, {})

    def test_simple_model_creation(self):
        """Test that SimpleModel can be instantiated."""
        from agno_example import SimpleModel
        
        model = SimpleModel()
        self.assertIsNotNone(model)
        self.assertEqual(model.id, "dummy-model")

    def test_simple_model_invoke(self):
        """Test that SimpleModel.invoke returns a message."""
        from agno_example import SimpleModel
        
        model = SimpleModel()
        result = model.invoke()
        
        self.assertIsNotNone(result)
        self.assertEqual(result.content, "Hello world")

    def test_agent_with_stub_model(self):
        """Test that an agent can be created with the stub model."""
        from agno.agent import Agent
        from agno_example import SimpleModel
        
        agent = Agent(model=SimpleModel())
        self.assertIsNotNone(agent)
        self.assertIsNotNone(agent.model)

    def test_agent_run_with_stub_model(self):
        """Test that the agent with stub model can run."""
        from agno.agent import Agent
        from agno_example import SimpleModel
        
        agent = Agent(model=SimpleModel())
        result = agent.run("Test input")
        
        # Verify the result has content
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'content'))
        print(f"Agent with stub model output: {result.content}")

if __name__ == "__main__":
    unittest.main()
