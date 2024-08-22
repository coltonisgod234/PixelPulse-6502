# The PixelPulse code style

## General Principles
- Code should be clear and easy to understand.
- Follow consistent naming conventions and formatting rules.
- Document your code thoroughly using docstrings.

## Naming Conventions
- **Variables and Functions**: Use snake_case (e.g., `calculate_total`).
- **Classes**: Use CamelCase (e.g., `ColorSystem`).
- **Constants**: Use ALL_UPPERCASE with underscores (e.g., `MAX_SIZE`).
- **Spellings**: Use Candian English spellings, for example, 
  - say "colour" instead of "color"
  - say "organize" instead of "organise"
  - say "catalouge" instead of "catalog"

## Code Formatting
- **Indentation**: Use 4 spaces for indentation.
- **Line Length**: Limit lines to 100 characters, and yea, I'm aware I 
                   violate this rule *everywhere* but I can't figure out how to NOT do it.

- **Braces**: Place opening braces on the same line as the statement.

## Docstrings and Comments
- **Function Docstrings**: Follow the format:
    ```
    """
    A breif description of the function

    ...

    Arguments
    ---------
    varible_name : varible_type
        A breif description of what the varible does

    varible_name : varible_type
        A breif description of what the varible does

    Returns
    -------
    return_type
        A breif description of the data contained in the return value
    """
    ```
- **Return**: Specify the return type in your docstring (unless it is None, then do not)