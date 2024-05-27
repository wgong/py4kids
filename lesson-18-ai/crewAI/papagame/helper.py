import string

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