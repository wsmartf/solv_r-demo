# Calculator Application

A Flask-based calculator application that demonstrates best practices for working with Solver AI.

## Running the Application

To run the calculator application, execute the following command:
```
flask --app app.calculator_server run
```

## Project Structure

- `app/`: Application source code
  - `calculator_server.py`: Main Flask application
  - `calculator.py`: Core calculation logic
  - `templates/`: HTML templates
- `scratch/`: Test and development files
  - `test_calculator.py`: Main test suite
  - `minimal_tester.py`: Test framework
  - `universal_template.py`: Test template
- `SOLVER_CAPABILITIES.md`: Comprehensive guide to Solver AI capabilities

## Key Features

- Simple calculator web interface
- Supports both equation strings ("2+3*4") and JSON operations
- Maintains calculation history
- Comprehensive test coverage
- Clear error handling

## Development Notes

- See `SOLVER_CAPABILITIES.md` for detailed information about working with Solver AI
- The capabilities guide is designed to be read at the start of each new session
- Keep the guide focused on permanent, verified capabilities
- Avoid temporary or session-specific details

## Documentation Strategy

- `README.md`: Quick start and high-level overview
- `SOLVER_CAPABILITIES.md`: Detailed capabilities guide
  - Organized by topic for easy reference
  - Includes code examples for common patterns
  - Stays within context window (~200 lines)
  - Focuses on verified, permanent capabilities

## File Management

- Files cannot be deleted or renamed
- Deprecated files are marked with header comments
- Focus on clear documentation and organization
- Use `scratch/` directory for development and testing

## Testing

- Run tests with: `python scratch/test_calculator.py`
- Tests cover both direct functions and API endpoints
- UI elements are verified through HTML inspection
- Test framework manages Flask server lifecycle

## Important Context

- This project serves as a reference implementation
- Demonstrates proper test organization
- Shows effective error handling
- Illustrates documentation best practices
