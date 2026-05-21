from db import init_db
from assistant import index, documents

if __name__ == '__main__':
    print('Initializing database...')
    init_db()
    print('Database initialized.')

    print(f'Loaded {len(documents)} documents into search index.')
    print('Ready to use.')
