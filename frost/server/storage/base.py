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

        if str(data['id']) in contents[table_name]:
            raise KeyError(
                f'ID {data["id"]} already exists in "{table_name}" table'
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
        id_ = str(data['id'])
        other = {
            k: v for k, v in data.items() if k != 'id'
        }
        commit_data = dict()

        commit = True
        for k, v in other.items():

            if isinstance(v, Unique):

                for val in contents[table_name].values():

                    if val[k] == str(v.data):
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
            Base.commit(contents)

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
