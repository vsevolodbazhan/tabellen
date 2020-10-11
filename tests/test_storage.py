from tabellen.storage import db, find, insert_or_replace


class TestStorage:
    collection_name = "test"

    def setup_method(self, test_method):
        document = {"name": "Ivan", "age": 43}
        collection = db[self.collection_name]

        self.person_id = collection.insert_one(document).inserted_id

    def teardown_method(self, test_method):
        db[self.collection_name].remove()

    def test_existing_document_can_be_found(self):
        query = {"name": "Ivan"}
        result = find(self.collection_name, query)

        assert result["_id"] == self.person_id

    def test_non_existent_document_can_not_be_found(self):
        query = {"name": "John"}
        result = find(self.collection_name, query)

        assert result is None

    def test_new_document_cen_be_inserted(self):
        document = {"name": "John", "age": 26}
        query = {"name": "John"}
        insert_or_replace(self.collection_name, query, document)

        assert db[self.collection_name].count_documents({}) == 2

    def test_existing_document_can_be_replaced(self):
        document = {"name": "John", "age": 26}
        query = {"name": "Ivan"}
        insert_or_replace(self.collection_name, query, document)

        assert db[self.collection_name].count_documents({}) == 1
