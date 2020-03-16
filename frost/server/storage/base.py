import json
from typing import Any, Dict, Optional

from frost.server.storage.exceptions import DuplicateValueError


class Base:
    """The base model for data storage.
    """

    @classmethod
    def search(cls, item: Any) -> Any:
        """Searches the saved data for a specific item.

        :param item: The item to search for
        :type item: Any
        :return: The data found under the specific item, returns None if not found
        :rtype: Any
        """
        return Base._get_table(cls).get(item)

    @classmethod
    def add(cls, item: Any) -> str:
        """Adds an item under the given specific table.

        :param item: The item to add
        :type item: Any
        :raises KeyError: If an item under a given ID already exists
        :return: The ID of the given item stored under the given table.
        :rtype: str
        """
        contents = Base.data()
        table_name = Base._get_table_name(cls)
        data = item.__dict__

        id_ = Base._get_id(contents, table_name, data)

        if str(id_) in contents[table_name]:
            raise KeyError(
                f'ID {id_} already exists in "{table_name}" table'
            )

        else:
            Base._update(
                contents,
                table_name,
                data
            )

        return str(id_)

    @classmethod
    def update(cls, item: Any) -> None:
        """Updates the given item's data. \
        Does not care if the item already exists.

        :param item: The item to update
        :type item: Any
        """
        Base._update(
            Base.data(),
            Base._get_table_name(cls),
            item.__dict__
        )

    @staticmethod
    def _update(contents: Dict[str, Any], table_name: str, data: Dict[str, Any]) -> None:
        """Updates the given item's data.

        :param contents: All saved data
        :type contents: Dict[str, Any]
        :param table_name: The name of the table where the item is/will be stored
        :type table_name: str
        :param data: The item's data
        :type data: Dict[str, Any]
        :raises ValueError: If a value stored in the item is an instance of \
        :class:`frost.server.storage.base.Unique` and it already exists within the table
        """
        id_ = str(Base._get_id(contents, table_name, data))
        commit_data = dict()

        commit = True
        for k, v in data.items():

            if k != 'id':

                if isinstance(v, Unique):
                    items = contents[table_name].items()

                    for key, val in items:

                        if key != 'meta':

                            if val[k] == str(v.data) and key != id_:
                                commit = False
                                raise DuplicateValueError(
                                    f'{v.data} already exists in {k}'
                                )

                        else:
                            commit_data[k] = v.data

                else:
                    commit_data[k] = v

        if commit:
            contents[table_name][id_] = commit_data
            contents[table_name]['meta']['last_id'] = str(len(
                contents[table_name]
            ) - 1)

            Base.commit(contents)

    @staticmethod
    def _get_id(contents, table_name, data):
        if data.get('id') is None:
            return int(contents[table_name]['meta']['last_id']) + 1
        return data['id']

    @staticmethod
    def _get_table_name(cls) -> Optional[str]:
        """Gets the table name of the subclass.

        :raises AttributeError: If the subclass does not have a class attribute of \
        :code:`__tablename__`
        :return: The table name of the subclass
        :rtype: Optional[str]
        """
        if hasattr(cls, '__tablename__'):
            return cls.__tablename__

        raise AttributeError(
            f'Class {cls} does not have attribute: __tablename__'
        )

    @staticmethod
    def _get_table(cls) -> Dict[str, Any]:
        """Get the entries under the specified table.

        :raises ValueError: If the table does not exist
        :return: The entries under the specified table
        :rtype: Dict[str, Any]
        """
        contents = Base.data()
        table = contents.get(Base._get_table_name(cls))

        if table is not None:
            return table

        raise ValueError('Table does not exist.')

    @staticmethod
    def commit(data: Dict[str, Any]) -> None:
        """Commits and saves the data.

        :param data: The data to be saved
        :type data: Dict[str, Any]
        """
        with open('storage.json', 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def data() -> Dict[str, Any]:
        """Gets the contents of the saved data.

        :return: The contents of the saved data
        :rtype: Dict[str, Any]
        """
        with open('storage.json') as f:
            return json.load(f)

    @classmethod
    def entries(cls) -> Dict[str, Any]:
        """Get the entries under the specified table.

        :return: The entries under the specified table
        :rtype: Dict[str, Any]
        """
        return Base._get_table(cls)


class Unique:
    """Ensures that the data stored is unique within its table.

    :param data: The unique data to be stored in a table
    :type data: Any
    """

    def __init__(self, data: Any) -> None:
        """The constructor method.
        """
        self.data = data
