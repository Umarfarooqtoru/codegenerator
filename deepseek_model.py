import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class DeepSeekClient:
    def __init__(self):
        # Since we're using local model, initialize it here
        # Note: This requires significant system resources
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "deepseek-ai/deepseek-coder-7b-instruct"
        
        # For offline use, you can download the model once
        # and use from_pretrained with local path
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map=self.device
            )
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Using simplified mock generation for testing")
            self.tokenizer = None
            self.model = None

    def generate_code(self, prompt):
        """
        Generate code based on the given prompt using DeepSeek model.
        
        For local testing without GPU, returns a sample app.
        """
        if self.model is None or self.tokenizer is None:
            # Return mock code for testing if model loading failed
            return self._get_mock_code(prompt)
            
        messages = [
            {"role": "user", "content": f"Generate a streamlit app that {prompt}. Only return the Python code, no explanations."}
        ]
        
        input_ids = self.tokenizer.apply_chat_template(
            messages, 
            return_tensors="pt"
        ).to(self.device)
        
        outputs = self.model.generate(
            input_ids, 
            max_new_tokens=2000,
            temperature=0.7,
            do_sample=True
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the assistant's response
        return response.split("assistant:")[-1].strip()
    
    def _get_mock_code(self, prompt):
        """Return a sample code based on the prompt for testing without the model"""
        # Check if HTML form is requested
        if "html" in prompt.lower() and "form" in prompt.lower():
            return f"""
import streamlit as st

def main():
    st.title("HTML Sign Up Form")
    
    # Using HTML for the form with custom styling
    html_form = '''
    <style>
        .form-container {{
            max-width: 400px;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin: 0 auto;
        }}
        .form-field {{
            margin-bottom: 15px;
        }}
        .form-field label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        .form-field input {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        .submit-button {{
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }}
        .submit-button:hover {{
            background-color: #45a049;
        }}
    </style>
    
    <div class="form-container">
        <form>
            <div class="form-field">
                <label for="fullname">Full Name</label>
                <input type="text" id="fullname" placeholder="Enter your full name">
            </div>
            <div class="form-field">
                <label for="email">Email Address</label>
                <input type="email" id="email" placeholder="Enter your email">
            </div>
            <div class="form-field">
                <label for="password">Password</label>
                <input type="password" id="password" placeholder="Create a password">
            </div>
            <div class="form-field">
                <label for="confirm-password">Confirm Password</label>
                <input type="password" id="confirm-password" placeholder="Confirm your password">
            </div>
            <button type="submit" class="submit-button">Sign Up</button>
        </form>
    </div>
    '''
    
    st.markdown(html_form, unsafe_allow_html=True)
    
    # Simulating form submission with Streamlit components
    with st.expander("Streamlit Form Alternative"):
        with st.form("signup_form"):
            st.text_input("Full Name")
            st.text_input("Email Address")
            st.text_input("Password", type="password")
            st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                st.success("Form submitted successfully!")

if __name__ == "__main__":
    main()
"""
        # Default mock code for other prompts
        else:
            return f"""
import streamlit as st

def main():
    st.title("App for: {prompt}")
    st.write("This is a sample app generated based on your prompt.")
    
    # Basic UI elements
    st.slider("Sample slider", 0, 100, 50)
    user_input = st.text_input("Enter some text")
    
    if st.button("Process"):
        st.write(f"You entered: {{user_input}}")

if __name__ == "__main__":
    main()
"""
