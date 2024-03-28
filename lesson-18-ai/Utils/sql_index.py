#!/usr/bin/env python
# coding: utf-8
# !pip install bidict

import re
import uuid
from bidict import bidict

def normalize_text(s, ignore_case=True, ignore_space=True, 
                   ignore_non_ascii=True, strip_semi_colon_at_end=True):
    """Normalize text by removing noise and normalizing whitespace/punctuation.

    Args:
      s: The text string to preprocess.

    Returns:
      The preprocessed text string.
    """
    text = str(s)
    
    if ignore_case:
        text = text.lower()
        
    if ignore_non_ascii:
        # Remove punctuation (ASCII and non-ASCII)
        text = re.sub(r"[^\w\s]", "", text)

    if ignore_space:
        # replace various whitespace characters (ASCII and non-ASCII) with a single whitespace
        text = re.sub(r"\s+", " ", text)

    text = text.strip()
    if strip_semi_colon_at_end and text.endswith(";"):
        text = text[:-1]
        
    return text.strip()

# Create a bidirectional map to store SQL queries and their IDs
sql_index = bidict()         # key-SQL: value-ID


def add_query(sql_query, ignore_case=True, ignore_space=True, 
              ignore_non_ascii=False, strip_semi_colon_at_end=True):
    """
    Adds an SQL query to the index and returns its unique ID.

    Args:
      sql_query: The SQL query string.

    Returns:
      The unique ID assigned to the SQL query.
    """
    # Normalize the SQL query (remove unnecessary characters, etc.)
    normalized_query = normalize_text(sql_query, 
                                      ignore_case=ignore_case, 
                                      ignore_space=ignore_space, 
                                      ignore_non_ascii=ignore_non_ascii,
                                      strip_semi_colon_at_end=strip_semi_colon_at_end)

    # Check if the query already exists in the bidict
    if normalized_query in sql_index:
        return sql_index.get(normalized_query)  # return ID
    
    # Generate a unique ID (using UUID)
    unique_id = str(uuid.uuid4())
    # Add the query and ID to the bidict
    sql_index[normalized_query] = unique_id
    return unique_id


def get_query_by_id(unique_id):
    """
    Retrieves the SQL query for a given unique ID using the forward lookup method.

    Args:
      unique_id: The unique ID of the SQL query.

    Returns:
      The corresponding SQL query string, or None if not found.
    """
    return sql_index.inverse.get(unique_id)


def get_id_by_query(query, ignore_case=True, ignore_space=True, 
                    ignore_non_ascii=False, strip_semi_colon_at_end=True):
    """
    Retrieves the unique ID for a given normalized SQL query using the inverse lookup method.

    Args:
      normalized_query: The normalized SQL query string.

    Returns:
      The unique ID associated with the query, or None if not found.
    """
    normalized_query = normalize_text(query, 
                                      ignore_case=ignore_case, 
                                      ignore_space=ignore_space, 
                                      ignore_non_ascii=ignore_non_ascii,
                                      strip_semi_colon_at_end=strip_semi_colon_at_end)
    
    return sql_index.get(normalized_query)


if __name__ == "__main__":
    # Example usage
    sql_query1 = " SELECT * FROM users WHERE id = 10; "
    sql_query2 = " SELECT name, email FROM customers ORDER BY name ASC; "

    unique_id1 = add_query(sql_query1)
    unique_id2 = add_query(sql_query2)

    print(unique_id1, unique_id2)

    print(get_query_by_id(unique_id1))
    print(get_query_by_id(unique_id2))

    sql3 = """
      SELECT 
          name, 
          email 
      FROM customers 
      ORDER BY name ASC
      ; 
    """
    id3 = get_id_by_query(sql3, ignore_non_ascii=False)

    print(id3 == unique_id2)
