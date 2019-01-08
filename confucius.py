from os import getenv
from typing import get_type_hints


class MetaConfig(type):
    __types__ = {
        bool: lambda v: str(v).lower() in {'yes', 'y', 't', 'true', '1', 'on'},
    }

    def __new__(cls, name, bases, namespace, **kwargs):
        namespace['__slots__'] = ()
        types = {}
        attr_types = {}
        # Walk the parents and collate:
        # - all the __types__ dicts.
        # - all the attribute types
        for parent in reversed(bases):
            types.update(getattr(parent, '__types__', {})
            attr_types.update({
                k: v
                for k, v in get_type_hints(parent).items()
                if k.isupper()
            })
        types.update(namespace.get('__types__', {}))
        namespace['__types__'] = types

        new_cls = type.__new__(cls, name, bases, namespace, **kwargs)

        # Validate we don't re-type anything
        for k, v in get_type_hints(new_cls).items():
            if not k.isupper() or not k in type_map:
                continue
            assert v == type_map[k], f"Type of locally declared {k} ({v}) does not match parent ({type_map[k]})"

        return new_cls

    def __call__(cls):
        raise TypeError(f'Can not create instance of singleton config {cls.__name__}')

    def as_dict(cls):
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if key.isupper()
        }

    def __getattribute__(cls, key):
        if not key.isupper():
            return object.__getattribute__(cls, key)

        raw = super().__getattribute__(key)

        _type = get_type_hints(cls).get(key, None)
        if callable(raw):
            raw = raw(cls)

        _type = cls.__types__.get(_type, _type)

        value = getenv(key, raw)

        if _type is not None:
            value = _type(value)

        return value


class BaseConfig(object, metaclass=MetaConfig):
    '''Base Config class'''

