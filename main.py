import streamlit as st
import process_gmail as gmail
from dotenv import load_dotenv
import process_pine

def main():
    # Load environment variables from .env
    load_dotenv()

    ### Display Page ###
    st.title("Google Email Assistant")

    # Authenticate and Extract button
    if st.button("Authenticate and Extract"):
        # Call the extract_emails() function
        credentials = gmail.authenticate()
        emails = gmail.extract_emails(credentials)
        process_pine.chunk_and_embed(emails)

    response = "awaiting response"
    
    # Search bar to input search query
    search_query = st.text_input("Enter a search query:")
    st.write("Search Query:", search_query)
    if search_query:
         response = process_pine.semantic_search(search_query)
         with st.expander('Query: {}'.format(search_query), expanded=True):
          st.write(response)
  
if __name__ == '__main__':
    main()