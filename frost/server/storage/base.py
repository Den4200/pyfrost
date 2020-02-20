import json


class Base:

    @classmethod
    def search(cls, item):
        contents = Base.data()
        table = Base._get_table(cls)

        return table.get(item)

    @classmethod
    def add(cls, item):
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

    @classmethod
    def update(cls, item):     
        Base._update(
            Base.data(),
            Base._get_table_name(cls),
            item.__dict__
        )

    @staticmethod
    def _update(contents, table_name, data):
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
                                raise KeyError(
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
    def _get_table_name(cls):
        if hasattr(cls, '__tablename__'):
            return cls.__tablename__

        raise AttributeError(
            f'Class {cls} does not have attribute: __tablename__'
        )

    @staticmethod
    def _get_table(cls):
        contents = Base.data()
        table = contents.get(Base._get_table_name(cls))

        if table is not None:
            return table
            
        raise ValueError('Table does not exist.')        

    @staticmethod
    def commit(data):
        with open('storage.json', 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def data():
        with open('storage.json') as f:
            return json.load(f)


class Unique:

    def __init__(self, data):
        self.data = data
