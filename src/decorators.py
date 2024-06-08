from functools import partial, wraps
import inspect
from typing import Callable, Optional


def recursive_check(data: dict, fields: str) -> tuple[bool, str]:
    fields = fields.split(".")
    found_fields = []
    for field in fields:
        if field not in data:
            return False, ".".join([*found_fields, field])
        data = data[field]
        found_fields.append(field)

    return True, ""


def required_fields(
    func: Optional[Callable] = None,
    *,
    fields: [str] = [],
):
    if func is None:
        return partial(required_fields, fields=fields)

    @wraps(func)
    async def wrapper(data, *args, **kwargs):
        missing_fields = []
        for field in fields:
            found, missing = recursive_check(data, field)
            reply = kwargs.get("reply")
            if not found:
                all_fields_found = False
                missing_fields.append(missing)
                continue

        if len(missing_fields) > 0:
            await reply({"missing": missing_fields})
            return
            
        if inspect.iscoroutinefunction(func):
            await func(data=data, *args, **kwargs)
        else:
            func(data=data, *args, **kwargs)

    return wrapper



