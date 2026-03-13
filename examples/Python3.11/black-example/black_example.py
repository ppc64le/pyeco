import black

def format_code_with_black(code: str) -> str:
    """
    Formats Python code using Black formatter.
    """
    try:
        # Mode defines formatting options (line length, etc.)
        mode = black.Mode()
        # Format code string using Black
        formatted_code = black.format_str(code, mode=mode)
        return formatted_code
    except Exception as e:
        return f"Error formatting code: {e}"


if __name__ == "__main__":
    # Sample unformatted Python code
    sample_code = "def  add(a,b):\n return  a+  b"

    print("Original Code:\n")
    print(sample_code)

    # Format using Black
    formatted = format_code_with_black(sample_code)

    print("\nFormatted Code:\n")
    print(formatted)
