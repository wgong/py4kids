import string


def normalize_text(text, delimitor="-"):
    """
    Normalizes a text phrase into an alpha-numeric string.
    
    Args:
      text: The text phrase to normalize.
    
    Returns:
      A new string where any non-alphanumeric characters are replaced by hyphens.
    """
    new_text = ""
    for char in text:
        if char.isalnum() or char.isspace():
            new_text += char
        else:
            new_text += ' '
    return delimitor.join([w for w in new_text.split() if w])

def convert_to_filename(text, join_char="_", file_ext="md"):
  """
  Converts a text string into a valid OS filename with the .md extension.

  Args:
      text: The text string to convert.

  Returns:
      A valid OS filename with the .md extension.
  """

  # Replace special characters with underscores
  valid_chars = "-_ %s%s" % (string.ascii_letters, string.digits)
  filename = ''.join(c for c in text if c in valid_chars)

  # Remove leading/trailing whitespace
  filename = join_char.join(filename.strip().lower().split())

  # Add .md extension
  filename = f"{filename}.{file_ext}"

  return filename

if __name__ == "__main__":
    # Example usage
    text = "This is a Title_with-Special Chars (#&*)"
    filename = convert_to_filename(text, "-", "txt")
    print(filename)   # this_is_a_title_with-special_chars.md