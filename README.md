# AI App Generator

This project is an AI-powered application generator that utilizes the DeepSeek model to create applications based on user prompts. The main interface is built using Streamlit, allowing users to easily interact with the application and generate code.

## Project Structure

```
ai-app-generator
├── src
│   ├── app.py                 # Main Streamlit application
│   ├── models
│   │   ├── __init__.py
│   │   └── deepseek_client.py # Interface with DeepSeek model
│   ├── utils
│   │   ├── __init__.py
│   │   └── code_generator.py  # Code generation utilities
│   └── templates              # Templates for generated apps
│       ├── __init__.py
│       └── basic_app.py
├── requirements.txt
├── .env.example               # Example environment variables
└── README.md
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ai-app-generator
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   - Copy `.env.example` to `.env` and fill in the required variables, including your DeepSeek API key.

5. **Run the Application**
   ```bash
   streamlit run src/app.py
   ```

## Usage

- Open your web browser and navigate to `http://localhost:8501` to access the application.
- Enter a prompt describing the application you want to generate.
- The application will communicate with the DeepSeek model to generate the corresponding code.
- The generated code will be displayed, and you can download it or use it directly.

## Obtaining the DeepSeek API

To use the DeepSeek model, you will need to obtain an API key. Follow these steps:

1. Visit the DeepSeek website and sign up for an account.
2. Navigate to the API section of your account dashboard.
3. Generate a new API key and copy it.
4. Paste the API key into your `.env` file under the appropriate variable.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.