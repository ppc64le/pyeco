## Purpose: Demonstrates basic Agno agent functionality with simple, self-contained examples.

### Packages used:
- agno==2.6.13

### Python Version:
- Python 3.11

### Main Example File: `agno_example.py`

This single file contains two complete examples demonstrating Agno agent functionality:

#### Example 1: Simple Hello World Agent
A minimal example demonstrating how to define and use a basic Agno agent.

**Functionality:**
- Defines a custom `SimpleAgent` class that extends `Agent`
- Implements a simple `run()` method that echoes user input with a greeting
- Demonstrates basic agent instantiation and execution

#### Example 2: Agent Using a Stub Model
Demonstrates how an Agno Agent can work with a custom model implementation.

**Functionality:**
- Implements a `StubMessage` class that mimics the Agno Message interface
- Creates a `SimpleModel` class that extends the Agno `Model` base class
- Provides stub implementations for synchronous and asynchronous invocation methods
- Shows how to create an agent with a custom model
- Returns predefined responses without requiring external APIs or credentials

### How to run the examples:
```bash
chmod +x install_test_example.sh
./install_test_example.sh
```

### License:
It's covered under Apache 2.0 licenses