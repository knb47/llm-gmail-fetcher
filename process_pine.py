from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os

load_dotenv()

# Initialize Pinecone and openAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV')
PINECONE_INSTANCE_NAME = os.environ.get('PINECONE_INSTANCE_NAME')

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
index_name = f"{PINECONE_INSTANCE_NAME}"

# Chunk and embed incoming emails
def chunk_and_embed(emails):
  for email in emails:
    # parse email into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    email_chunks = text_splitter.split_text(email["Body"])
    for i in range(len(email_chunks)):
      email_chunks[i] += " From: " + email["From"] + " Date: " + email["Date"] + " Subject: " + email["Subject"]
  
    # embed chunks into Pinecone DB
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    for chunk in email_chunks:
      print("Chunk", chunk)
    Pinecone.from_texts(email_chunks, embeddings, index_name=index_name)

# Semantic search functionality
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
chain = load_qa_chain(llm, chain_type="stuff")

def semantic_search(query):
  llmQuery = query + "You are given a list of emails and a query that appears before this sentence. Please return the subject and date for the email that best matches this query and provide additional information about this email if the query asks for additional information."
  docsearch = Pinecone.from_existing_index(index_name, embeddings)
  # semantic search
  docs = docsearch.similarity_search(query)
  # first document found
  print(docs[0].page_content)
  # llm assisted response grab
  response = chain.run(input_documents=docs, question=llmQuery)
  return response
