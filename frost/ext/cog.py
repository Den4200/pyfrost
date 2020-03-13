from typing import Any, Optional

from frost.ext.exceptions import DirectCogInstanceError


_cogs = dict()


class Cog:

    def __new__(cls) -> 'Cog':
        self = super().__new__(cls)
        members = cls.__dict__.items()
        try:
            route = cls.route

        except AttributeError:
            raise DirectCogInstanceError(
                'The Cog class cannot be directly instantiated. It must be subclassed.'
            ) from None

        else:
            _cogs.update({
                route: {
                    k: v for k, v in members
                    if not k.startswith('_') and k != 'route'
                }
            })
            return self

    def __init_subclass__(cls, route: Optional[str] = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.route = route or cls.__name__
