import os
from typing import List, Optional

# go to workspace directory
from dotenv import load_dotenv
load_dotenv()
os.chdir(os.getenv('WORKSPACE_DIRECTORY'))

# loading and plitting 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document

class PDFVectorDatabase:
    def __init__(self, 
                 pdf_directories: Optional[List[str]] = None,
                 embedding_model: str = 'text-embedding-ada-002'):
        """Initialize Database"""

        # make embeddings
        self.embeddings = OpenAIEmbeddings(model=embedding_model)

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200, # for more context
            length_function=len
        )

        self.pdf_directories = pdf_directories or []

        self.vectorstore = None
        
        self.loaded_documents = []

    def add_pdf_directory(self, directory: str):
        """ adds to the pdf directory"""
        if os.path.exists(directory):
            print("Directory exists")
        else:
            print("Directory does not exist")

        self.pdf_directories.append(directory)

    def load_pdfs(self):
        """load pdfs by taking in the pdf, splitting them and adding their chunks in the vector """
        all_docs = []
                
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
        
        self.loaded_documents.extend(all_docs)
        
        return all_docs

    def build_database(self):
        """
        Build FAISS vector database
        
        Args:
            new_directory (Optional[str]): Directory to add to existing database
        """
        print(self.loaded_documents)
        
        # If no existing vectorstore, create a new one
        if self.vectorstore is None:
            self.vectorstore = FAISS.from_documents(self.loaded_documents, self.embeddings)
        else:
            # Add new documents to existing vectorstore
            vectorstore_addition = FAISS.from_documents(self.loaded_documents, self.embeddings)
            self.vectorstore.merge_from(vectorstore_addition)
    
    def search_with_metadata(self, 
                              query: str, 
                              k: int = 4, 
                              filter_source: Optional[str] = None) -> List[Document]:
        """
        Perform similarity search with optional source filtering
        
        Args:
            query (str): Search query
            k (int): Number of top results to return
            filter_source (Optional[str]): Filter results by specific PDF source
        
        Returns:
            List of most similar document chunks
        """
        if not self.vectorstore:
            raise ValueError("Vector database not initialized")
        
        # If filtering by source, use metadata filter
        if filter_source:
            return self.vectorstore.similarity_search(
                query, 
                k=k, 
                filter={"source": filter_source}
            )
        
        # Regular similarity search
        return self.vectorstore.similarity_search(query, k=k)
