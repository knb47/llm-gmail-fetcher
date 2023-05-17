import streamlit as st
import gmail_api as gmail
from dotenv import load_dotenv
from env_write import write_to_env_file

def main():
    # Load environment variables from .env
    load_dotenv()

    # Authenticate
    

    ### Display Page ###
    st.title("Google Email Assistant")
    
    # Ask the user for their Google Email API key
    # api_key = st.text_input("Enter your Google Email API key:")
    # st.write("API Key:", api_key)

    # # Update environment variables
    # write_to_env_file(api_key)

    credentials = None

    if st.button("Authenticate and extract"):
        # Call the extract_emails() function
        credentials = gmail.authenticate()
        emails = gmail.extract_emails(credentials)
    
    # print("Credentials ", credentials)

    # # Use the extracted emails as needed
    # if st.button("Fetch emails"):
    #     # Call the extract_emails() function
    #     print("Credentials in")
        
    
        # Use the extracted emails as needed
        # if emails:
        #     for email in emails:
        #         st.write('From:', email['From'])
        #         st.write('Subject:', email['Subject'])
        #         st.write('Snippet:', email['Snippet'])
        #         st.write('---')
        # else:
        #     st.write('No emails found.')
    
    # Create a search bar to input search query
    # search_query = st.text_input("Enter a search query:")
    # st.write("Search Query:", search_query)
    
    # # Display the text results of the query
    # results_box = st.empty()
    # if search_query:
    #     with st.expander("Search Results", expanded=True):
    #         st.write("Result 1")
    #         st.write("Result 2")
    #         st.write("Result 3")
  
if __name__ == '__main__':
    main()