# Solver AI Capabilities Guide

## About This Document
This guide is designed to be read at the start of each new Solver AI session. It's maintained at a length (~200 lines) that fits within Solver's context window, ensuring the entire document can be processed at once. The content is organized by topic for easy reference and focuses on permanent, verified capabilities.

This document serves as a comprehensive guide to Solver AI's capabilities, limitations, and best practices, helping both users and Solver itself understand how to work effectively within the environment.

## Core Capabilities

1. **File Operations**:
   - Can create files (`create`)
   - Can edit files (`edit`)
   - Can view files (`open`)
   - Can revert changes made in current session (`revert`)
   - `revert` works with:
     * Edit IDs (to undo specific changes)
     * File paths (to undo all changes to a file)
   - Cannot permanently delete or rename files
   - Best practice: Mark unused files as deprecated
   - Important: `revert` undoes changes, doesn't delete files

2. **Available Python Environment**:
   - Python 3.11 with full standard library access
   - Pre-installed packages: Flask, pytest, async-lru
   - Cannot install new packages during execution
   - Use `python -c "help('modules')"` to list available modules
   - PYTHONPATH automatically includes project root


3. **Process Management**:
   - Can execute Python scripts (`python`)
   - Can run Flask applications
   - Can use subprocess for background processes
   - Limited terminal interaction (no interactive input)

4. **Search Capabilities**:
   - Text search within files (`text_search`)
   - Semantic search across repository (`semantic_search`)
   - Documentation search (`search_in_docs`)

## Testing Strategies

1. **Verification Hierarchy**:
   - Start with direct function testing (most reliable)
   - Then test API endpoints (HTTP layer)
   - Finally verify UI elements (HTML/JS presence)
   - Avoid complex UI interaction tests
   - Focus on verifiable, deterministic outcomes

2. **API Testing Best Practices**:
   ```python
   # Use universal_template.py for consistent testing
   class MyTestSession(TestSession):
       def test_api_endpoints(self):
           # Test successful cases
           status, data = self.tester.request('POST', '/endpoint', 
               json_data={"key": "value"})
           self.tester.assert_equal(status, 200)
           
           # Test error cases
           status, data = self.tester.request('POST', '/endpoint', 
               json_data={"invalid": "data"})
           self.tester.assert_equal(status, 400)
           self.tester.assert_in('error', data)
   ```

2. **UI Testing Approaches**:
   - Focus on API functionality first
   - Use built-in libraries for basic UI verification:
     - urllib for HTTP requests
     - json for data handling
     - subprocess for server management
   - Document manual testing steps when needed

3. **Test File Organization**:
   - Keep tests in `scratch/` directory
   - Use descriptive test file names
   - Separate unit tests from integration tests
   - Maintain minimal test dependencies

## Common Patterns & Solutions

1. **Working with Flask Apps**:
   ```python
   # Start server in background
   import threading
   server_thread = threading.Thread(target=lambda: app.run())
   server_thread.daemon = True
   server_thread.start()
   ```

2. **Handling Missing Dependencies**:
   ```python
   try:
       from optional_module import feature
       has_feature = True
   except ImportError:
       has_feature = False
       print("Feature not available")
   ```

3. **File Path Management**:
   ```python
   import os
   project_root = os.path.dirname(os.path.dirname(__file__))
   file_path = os.path.join(project_root, 'path', 'to', 'file')
   ```

## Best Practices

1. **Code Organization**:
   - Keep test files separate from production code
   - Use clear, descriptive file names
   - Maintain consistent file structure
   - Document assumptions and requirements

2. **Testing Approach**:
   - Start with API/backend tests
   - Add UI tests only for critical paths
   - Keep tests focused and minimal
   - Use built-in Python libraries creatively

3. **Error Handling**:
   - Always verify error cases
   - Test both success and failure paths
   - Include meaningful error messages
   - Document expected error conditions

4. **Documentation**:
   - Document test requirements
   - Include example usage
   - Explain any workarounds
   - Keep documentation up-to-date

## Limitations and Workarounds

1. **Process Control**:
   - Cannot control/stop long-running processes
   - Flask server must be run in a managed way (e.g., in a thread we can control)
   - Use subprocess with timeout mechanisms
   - Always implement cleanup procedures
   - Best practice: Use test framework to manage server lifecycle

2. **Package Installation**:
   - Cannot install new packages during execution
   - Use standard library alternatives
   - Implement minimal versions of needed functionality
   - Focus on core features that don't require external packages

2. **Interactive Features**:
   - No interactive terminal input
   - Use subprocess with predefined inputs
   - Simulate user interactions via HTTP requests
   - Document manual testing steps

3. **Environment Constraints**:
   - Limited file system access
   - No persistent storage between sessions
   - No network access except HTTP
   - No system command execution

## Command Understanding

1. **Command Limitations**:
   - Available commands are explicitly listed at session start
   - No implicit operations (like delete or rename) exist
   - Commands do exactly what their help text states
   - Don't assume Unix-like command capabilities
   - When in doubt, refer to command documentation

2. **Command Documentation Reading**:
   - Pay attention to exact command syntax
   - Note the specific arguments required
   - Understand the scope of each command
   - Don't assume additional functionality
   - Test command behavior when uncertain

## Tips for Success

1. **Command Usage Best Practices**:
   - Verify file existence before operations (`tree`, `open`)
   - Check command output carefully
   - Don't assume command failure means command is unreliable
   - Use `tree` to verify current state before operations
   - Core commands (open, edit, create, python) are fundamental
   - Always verify command success before proceeding
   - When unable to delete files, mark them as deprecated
   - Use clear documentation to point to new locations
   - Keep old files readable but clearly marked as obsolete

2. Always verify file paths and imports early
2. Test incrementally and verify each step
3. Keep code changes small and focused
4. Document any assumptions or requirements
5. Use built-in Python features creatively
6. Maintain clear separation of concerns
7. Prefer simple, maintainable solutions
8. Always run tests after making changes

## Command Reference

```bash
# File Operations
open [--line LINE] [--definition DEF] PATH  # View file contents
edit PATH EDIT_PAIR [EDIT_PAIR ...]         # Modify existing files
create PATH CONTENT                         # Create new files
tree [--depth DEPTH] [PATH]                 # View directory structure

# Search Operations
text_search [PATH] PATTERN                  # Search for exact text
semantic_search QUERY                       # Search conceptually
search_in_docs PROJECT TOPIC                # Search documentation

# Execution
python [ARGS ...]                           # Run Python scripts
submit                                      # Submit changes
revert TARGET [TARGET ...]                  # Revert changes
```
