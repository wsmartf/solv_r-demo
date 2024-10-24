def create_greeting(name=None):
    """Create a greeting message for the given name."""
    if name is None:
        name = 'World'
    return f"Hello, {name}!"
