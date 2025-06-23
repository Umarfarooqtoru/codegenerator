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
        """Return a simple mock code for testing without the model"""
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
