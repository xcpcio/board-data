def hello_world():
    """Return a hello world message."""
    return "Hello, World!"


def test_hello_world():
    """Test the hello_world function."""
    result = hello_world()
    assert result == "Hello, World!"
    assert isinstance(result, str)
