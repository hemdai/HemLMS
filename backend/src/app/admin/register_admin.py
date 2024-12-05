registry = {}


def register_admin(cls, schema, registry=registry):
    registry[cls.__name__] = schema
    return registry
