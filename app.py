import streamlit as st
from deepseek_model import DeepSeekClient
from code_generator import generate_code

def main():
    st.title("AI App Generator")
    st.write("Enter a prompt to generate an application:")

    prompt = st.text_area("Prompt", height=150)
    
    # Example suggestions
    st.caption("Try these examples:")
    example_prompts = [
        "make a sign up form for me in html",
        "create a calculator app",
        "build a todo list application",
        "create a data visualization dashboard"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(example_prompts):
        if cols[i % 2].button(f"Example {i+1}", key=f"example_{i}"):
            prompt = example
            st.session_state.prompt = example

    if "prompt" in st.session_state:
        st.session_state.prompt = prompt

    if st.button("Generate App"):
        if prompt:
            with st.spinner("Generating your app..."):
                client = DeepSeekClient()
                generated_code = client.generate_code(prompt)
                formatted_code = generate_code(prompt, generated_code)

                # Display code
                st.subheader("Generated Code:")
                st.code(formatted_code, language='python')
                
                # Add download button
                st.download_button(
                    label="Download App",
                    data=formatted_code,
                    file_name="generated_app.py",
                    mime="text/plain"
                )
                
                # Preview section
                st.subheader("Live Preview:")
                st.write("Below is a live preview of how the app would look:")
                
                try:
                    # Create an expander for the preview
                    with st.expander("App Preview", expanded=True):
                        # For HTML content, try to render it
                        if "html_form" in formatted_code and "st.markdown" in formatted_code:
                            # Extract HTML content between triple quotes
                            import re
                            html_match = re.search(r"html_form\s*=\s*'''(.*?)'''", formatted_code, re.DOTALL)
                            if html_match:
                                html_content = html_match.group(1)
                                st.markdown(html_content, unsafe_allow_html=True)
                            else:
                                st.warning("HTML content found but couldn't be extracted for preview")
                        else:
                            st.info("This is a simplified preview. Download and run the app for full functionality.")
                            # Extract and run basic UI elements if possible
                            if "st.slider" in formatted_code:
                                st.slider("Sample slider", 0, 100, 50)
                            if "st.text_input" in formatted_code:
                                st.text_input("Sample input")
                            if "st.button" in formatted_code:
                                st.button("Sample button")
                except Exception as e:
                    st.error(f"Error rendering preview: {e}")
        else:
            st.error("Please enter a prompt.")

if __name__ == "__main__":
    main()
