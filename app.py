import os
import streamlit as st
import google.generativeai as genai

def main():
    # Set your Gemini API key directly here
    api_key = 'AIzaSyAKBvrkXznMF8GGSND1Gj4gvtGr8IHInb8'  
    genai.configure(api_key=api_key)

    # Set up the Streamlit interface
    st.title("Question-Answering System")

    # User input for the question
    user_input = st.text_area(
        "Please enter your question below:",
        height=100
    )

    # Button to generate an answer
    if st.button("Get Answer"):
        if user_input.strip():
            # Create a prompt for generating the answer
            prompt = f"""
            Based on the following question, please provide a detailed and accurate answer:

            Question: "{user_input}"

            """

            try:
                # Use the Gemini generative model to generate the answer
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                answer = response.text

                # Store the generated answer in the session state to keep it persistent
                st.session_state.generated_answer = answer
                st.session_state.copy_status = "Copy Answer to Clipboard"  # Reset the copy button text

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.warning("We couldn't retrieve the answer. Please try again later.")
        else:
            st.warning("Please provide a question.")

    # Check if the generated answer is in session state
    if 'generated_answer' in st.session_state:
        st.subheader("Your Answer:")
        answer_text_area = st.text_area("Generated Answer:", st.session_state.generated_answer, height=300, key="answer_content")

        # Button to copy answer to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Answer to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var answerContent = document.querySelector('#answer_content');
                    var range = document.createRange();
                    range.selectNode(answerContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
