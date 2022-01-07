import pytest
import main

DOCUMENTS_TEST = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

NEW_DOC = ['certificate', 'VI-12345', 'Иван Демидов']

DIRECTORIES_TEST = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


class TestDocs:

    def setup(self):
        self.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]
        self.directories = {
            '1': ['2207 876234', '11-2'],
            '2': ['10006'],
            '3': []
        }

    def get_docs_string(self):
        new_docs_list = []
        for doc_test_dict in self.documents:
            doc_str = '{} "{}" "{}"'.format(*doc_test_dict.values())
            new_docs_list.append(doc_str)
        return new_docs_list

    def get_doc_list(self):
        pass

    @pytest.mark.parametrize(
        'doc_num,expected_result',
        [
            ('10006', True),
            ('11-12', False),
            ('', False)
        ]
    )
    def test_check_doc(self, doc_num, expected_result):
        assert main._check_doc(doc_num, self.directories) == expected_result

    @pytest.mark.parametrize(
        'shelf,expected_result',
        [
            ('1', True),
            ('4', None),
            ('', None)
        ]
    )
    def test_check_shelf(self, shelf, expected_result):
        assert main._check_shelf(shelf, self.directories) == expected_result

    @pytest.mark.parametrize(
        'doc_num,expected_result',
        [
            ('10006', 'Аристарх Павлов'),
            ('11-12', None),
            ('', None)
        ]
    )
    def test_find_people(self, doc_num, expected_result):
        assert main.find_people(doc_num, self.documents, self.directories) == expected_result

    @pytest.mark.parametrize(
        'doc_num,expected_result',
        [
            ('10006', '2'),
            ('11-12', None),
            ('', None),
            ('11-2', '1')
        ]
    )
    def test_find_shelf(self, doc_num, expected_result):
        assert main.find_shelf(doc_num, self.directories) == expected_result

    def test_print_doc(self):
        print(self.documents)
        assert main.print_doc(self.documents) == self.get_docs_string()

    # def test_print_doc(self):
    #     assert main.print_doc(DOCUMENTS_TEST) == get_docs_string(DOCUMENTS_TEST)

    @pytest.mark.parametrize(
        'doc_num,expected_result',
        [
            ('10006', True),
            ('11-12', None),
            ('', None),
            ('10006', None)
        ]
    )
    def test_delete_doc_result(self, doc_num, expected_result):
        assert main.delete_doc(doc_num, self.documents) == expected_result

    def test_delete_doc_len(self):
        len_docs = len(self.documents)
        len_dirs = len(self.directories['2'])
        main.delete_doc('10006', self.documents, self.directories)
        print('len', len(self.directories['2']))
        assert len(self.documents) == (len_docs - 1)
        assert len(self.directories['2']) == (len_dirs - 1)

    @pytest.mark.parametrize(
        'doc_inf,shelf,expected_result,changed_len_val',
        [
            (NEW_DOC, '3', 'Документ добавлен', 1),
            (NEW_DOC, '4', 'Такой полки не существует', 0),
            (DOCUMENTS_TEST[0].values(), '1', 'Документ уже существует', 0)

        ]
    )
    def test_add_doc(self, doc_inf, shelf, expected_result, changed_len_val):
        # len_docs = len(self.documents)
        assert main.add_doc(*doc_inf, shelf, self.directories, self.documents) == expected_result
        # assert len(self.documents) == (len_docs + changed_len_val)
        if shelf in self.directories:
            len_dirs = len(DIRECTORIES_TEST[shelf])
            assert len(self.directories[shelf]) == len_dirs + changed_len_val
        else:
            len_dirs = len(self.directories)
            assert len(self.directories) == len_dirs + changed_len_val

    @pytest.mark.parametrize(
        'doc_num,shelf,expected_result,changed_len_val',
        [
            ('11-11', '5', 'Документ не существует', 0),
            ('10006', '2', 'Документ уже находится на полке', 0),
            ('10006', '3', 'Документ перемещен', 1),
            ('10006', '6', 'Такой полки не существует', 0),
        ]
    )
    def test_move_doc(self, doc_num, shelf, expected_result, changed_len_val):
        assert main.move_doc(doc_num, shelf, self.directories) == expected_result
        if main._check_doc(doc_num, self.directories):
            shelf_before = main.find_shelf(doc_num, DIRECTORIES_TEST)
            len_shelf_before = len(DIRECTORIES_TEST[shelf_before])
            assert len(self.directories[shelf_before]) == len_shelf_before - changed_len_val
        if shelf in self.directories:
            len_shelf_after = len(DIRECTORIES_TEST[shelf])
            assert len(self.directories[shelf]) == len_shelf_after + changed_len_val

    @pytest.mark.parametrize(
        'new_shelf,expected_result,changed_len',
        [
            ('1', None, 0),
            ('5', True, 1)
        ]
    )
    def test_add_shelf(self, new_shelf, expected_result, changed_len):
        len_directories = len(self.directories)
        assert main.add_shelf(new_shelf, self.directories) == expected_result
        assert len(self.directories) == len_directories + changed_len