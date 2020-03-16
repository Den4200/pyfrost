from typing import Any, Optional

from frost.ext.exceptions import DirectCogInstanceError

_cogs = dict()


class Cog:
    """Children of this class and its methods are automatically routed and then handled by \
    :class:`frost.ext.handler.Handler`. Private methods of the children are ignored and not \
    routed. All children methods are automatically run as static methods.

    :raises DirectCogInstanceError: If this class is directly instantiated. \
    This class can only be subclassed.
    """

    def __new__(cls) -> 'Cog':
        """Automatically routes the subclass and its public methods.

        :raises DirectCogInstanceError: If this class is directly instantiated. \
        This class can only be subclassed.
        :return: An instance of the subclass
        """
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
        """Names the route for the subclass.

        :param route: The path of the route, defaults to the name of the subclass
        :type route: Optional[str]
        """
        super().__init_subclass__(**kwargs)
        cls.route = route or cls.__name__
