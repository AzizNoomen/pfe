class DocumentService:
    def __init__(self, session: Session):
        self.repository = DocumentRepository(session)

    def create_document(self, document_data: DocumentSchema) -> DocumentSchema:
        document = self.repository.create_document(document_data)
        return document

    def get_all_documents(self) -> List[DocumentSchema]:
        documents = self.repository.get_all_documents()
        return documents

    def close(self):
        self.repository.close()
