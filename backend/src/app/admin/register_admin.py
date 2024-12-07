registry = {}


class AdminSite:
    @classmethod
    def register_admin(cls, model, schema, registry=registry):
        registry[model.__name__] = schema
        return registry
