# import other packages
import os
from typing import List, Optional

# import langchain packages
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document


class PDFVectorDatabase:
    def __init__(self, 
                 pdf_directories: Optional[List[str]] = None,
                 embedding_model: str = 'text-embedding-ada-002'):
        """
        initialize vector database
        """
        # create embeddings
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        # create splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100, # for more context
            length_function=len
        )

        # create the directories, store, and loaded pdf
        self.pdf_directories = pdf_directories or []
        self.vectorstore = None
        self.loaded_documents = []

    def add_pdf_directory(self, directory: str):
        """
        adds to the pdf directory
        """
        if not os.path.exists(directory):
            print("Directory does not exist")

        self.pdf_directories.append(directory)

    def load_pdfs(self):
        """load pdfs by taking in the pdf, splitting them and adding their chunks in the vector."""
        all_docs = []
        
        # adds all pdf in the directory
        for pdf_dir in self.pdf_directories:
            for filename in os.listdir(pdf_dir):
                if filename.endswith('.pdf'):
                    filepath = os.path.join(pdf_dir, filename)
                    
                    # load PDF and split
                    loader = PyPDFLoader(filepath)
                    docs = loader.load_and_split(self.text_splitter)
                    
                    # add filename as metadata
                    for doc in docs:
                        doc.metadata['source'] = filename
                    
                    all_docs.extend(docs)

        # optimization to only extend what is not already in the database 
        self.loaded_documents.extend(all_docs)
        
        return all_docs

    def build_database(self):
        """
        build FAISS vector database
        """
        
        # if no existing vectorstore, create a new one
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(self.loaded_documents, self.embeddings)
        else:
            # used later for re-addition
            vectorstore_addition = FAISS.from_documents(self.loaded_documents, self.embeddings)
            self.vectorstore.merge_from(vectorstore_addition)
    
    def search_with_metadata(self, 
                              query: str, 
                              k: int = 4, 
                              filter_source: Optional[str] = None) -> List[Document]:
        """
        perform similarity search with optional source filtering
        """
        if not self.vectorstore:
            raise ValueError("Vector database not initialized")
        
        # optimized way later, where llm can view all of the possible pdf and get the file name and know which one is important which could be faster 
        # similarity search on the metadata?
        if filter_source:
            return self.vectorstore.similarity_search(
                query, 
                k=k, 
                filter={"source": filter_source}
            )
        
        # similarity search
        return self.vectorstore.similarity_search(query, k=k)
