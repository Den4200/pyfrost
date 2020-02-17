import json

class Base:

    @classmethod
    def search(cls, item):
        contents = Base.data()
        table = Base._get_table(cls)

        return table.get(item)

    @classmethod
    def update(cls, item):
        contents = Base.data()
        table_name = Base._get_table_name(cls)

        data = item.__dict__
        id_ = str(data['id'])
        other = {
            k: v for k, v in data.items() if k != 'id'
        }
        
        if isinstance(contents[table_name], dict):
            contents[table_name][id_] = other

        else:
            contents[table_name].append(other)

        Base.commit(contents)

    @staticmethod
    def _get_table_name(cls):
        if not hasattr(cls, '__tablename__'):
            raise AttributeError(
                f'Class {cls} does not have attribute: __tablename__'
            )

        return cls.__tablename__

    @staticmethod
    def _get_table(cls):
        contents = Base.data()

        table = contents.get(Base._get_table_name(cls))

        if table is None:
            raise ValueError('Table does not exist.')

        return table

    @staticmethod
    def commit(data):
        with open('storage.json', 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def data():
        with open('storage.json') as f:
            return json.load(f)
