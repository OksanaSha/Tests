DOCUMENTS = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

DIRECTORIES = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

commands = {
    'p': 'вывести имя владельца по номеру документа',
    's': 'вывести номер полки на которой лежит документ',
    'l': 'список документов',
    'a': 'добавить новый документ',
    'd': 'удалить документ',
    'm': 'переместить документ на другую полку',
    'as': 'добавить новую полку',
    'ls': 'список полок',
    'quit': 'выход',
    'help': 'помощь'
}


def _check_doc(doc_num, directories):
    for doc in directories.values():
        if doc_num in doc:
            return True
    return False


def _check_shelf(shelf, directories):
    if shelf in directories:
        return True



def _del_doc_from_shelf(doc_num, directories):
    for doc in directories.values():
        if doc_num in doc:
            del doc[doc.index(doc_num)]


def find_people(doc_num, documents=DOCUMENTS, directories=DIRECTORIES):
    if _check_doc(doc_num, directories):
        for doc in documents:
            if doc['number'] == doc_num:
                return doc['name']


def find_shelf(doc_num, directories=DIRECTORIES):
    if _check_doc(doc_num, directories):
        for shelf, doc in directories.items():
            if doc_num in doc:
                return shelf


def print_doc(documents=DOCUMENTS) -> list:
    docs_str_format = []
    for doc in documents:
        list_values = list(doc.values())
        doc_string_format = '{0} "{1}" "{2}"'.format(*list_values)
        docs_str_format.append(doc_string_format)
    return docs_str_format


def add_doc(tpe, num, owner, shelf, directories=DIRECTORIES, documents=DOCUMENTS):
    new_doc = dict(type = tpe, number = num, name = owner)
    if new_doc in documents:
        return 'Документ уже существует'
    if _check_shelf(shelf, directories):
        documents.append(new_doc)
        directories[shelf] += [num]
        return 'Документ добавлен'
    return 'Такой полки не существует'


def delete_doc(doc_num, documents=DOCUMENTS, directories=DIRECTORIES):
    if _check_doc(doc_num, directories):
        _del_doc_from_shelf(doc_num, directories)
        for i, doc in enumerate(documents):
            if doc['number'] == doc_num:
                doc_position = i
                break
        del documents[doc_position]
        return True


def move_doc(doc_num, shelf, directories=DIRECTORIES):
    if not _check_doc(doc_num, directories):
        return 'Документ не существует'
    if _check_shelf(shelf, directories):
        if doc_num in directories[shelf]:
            return 'Документ уже находится на полке'
        _del_doc_from_shelf(doc_num, directories)
        directories[shelf] += [doc_num]
        return 'Документ перемещен'
    return 'Такой полки не существует'


def add_shelf(new_shelf, directories=DIRECTORIES):
    if new_shelf not in directories:
        directories.setdefault(new_shelf, [])
        return True


def print_shelves(directories=DIRECTORIES):
    print(*(f'{key} - {val}' for key, val in directories.items()), sep='\n')


def user_command():
    while True:
        user_input = input('Введите команду (quit - выход, help - помощь): ').lower()

        if user_input == 'p':  # test
            doc_num = input('Введите номер документа: ')
            if find_people(doc_num):
                print(find_people(doc_num))
            else:
                print('Такого документа нет, попробуйте еще раз')

        elif user_input == 's':  # test
            doc_num = input('Введите номер документа: ')
            if find_shelf(doc_num):
                print(find_shelf(doc_num))
            else:
                print('Такого документа нет, попробуйте еще раз')

        elif user_input == 'l':  # test
            print_doc()

        elif user_input == 'a':  # test
            num = input('Введите номер документа: ')
            tpe = input('Введите тип: ')
            owner = input('Введите владельца: ')
            shelf = input('Введите номер полки: ')
            return_value = add_doc(tpe, num, owner, shelf)
            if return_value == 'doc_add':
                print('Документ успешно добавлен')
            elif return_value == 'doc_no_add':
                print('Документ не добавлен')
            else:
                print('Документ уже существует')

        elif user_input == 'd':  # test
            doc_num = input('Введите номер документа: ')
            if delete_doc(doc_num):
                print('Документ удален')
            else:
                print('Такого документа нет, попробуйте еще раз')

        elif user_input == 'm':  # test
            doc_num = input('Введите номер документа: ')
            shelf = input('Введите номер полки: ')
            return_value = move_doc(doc_num, shelf)
            if return_value == 'doc_move':
                print('Документ перемещен')
            elif return_value == 'doc_no_move':
                print('Документ не добавлен')
            elif return_value == 'doc_in_shelf':
                print('Документ уже хранится на полке')
            else:
                print('Такого документа нет, попробуйте еще раз')

        elif user_input == 'as':
            new_shelf = input('Введите номер полки: ')
            if add_shelf(new_shelf):
                print('Полка добавлена')
            else:
                print('Такая полка уже существует')

        elif user_input == 'ls':
            print_shelves()

        elif user_input == 'quit':
            print('Всего доброго!')
            break

        elif user_input == 'help':
            for key, value in commands.items():
                print(f'{key} - {value}')

        else:
            print('Такой команды не существует')
        print()

if __name__ == '__main__':
    # user_command()

    print(*print_doc(), sep='\n')
