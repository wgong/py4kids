from typing import Any, Dict, List

def pquery(table, **kwargs) -> List[Dict[str, Any]]:
    responses = []
    start_key = True
    while start_key is not None:
        if start_key != True:
            kwargs["ExclusiveStartKey"] = start_key
        response = table.query(**kwargs)
        responses.append(response)
        start_key = response.get("LastEvaluatedKey", None)
    return responses
