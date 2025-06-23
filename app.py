import streamlit as st
from deepseek_client import DeepSeekClient
from code_generator import generate_code

def main():
    st.title("AI App Generator")
    st.write("Enter a prompt to generate an application:")

    prompt = st.text_area("Prompt", height=150)

    if st.button("Generate App"):
        if prompt:
            with st.spinner("Generating your app..."):
                client = DeepSeekClient()
                generated_code = client.generate_code(prompt)
                formatted_code = generate_code(prompt, generated_code)

                st.subheader("Generated Code:")
                st.code(formatted_code, language='python')
                
                # Add download button
                st.download_button(
                    label="Download App",
                    data=formatted_code,
                    file_name="generated_app.py",
                    mime="text/plain"
                )
        else:
            st.error("Please enter a prompt.")

if __name__ == "__main__":
    main()
