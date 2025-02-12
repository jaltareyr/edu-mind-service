# EduMind CLI Tool

EduMind CLI Tool is a command-line interface application for generating quiz questions. It interprets a user-provided query, fetches relevant information, generates questions, formats them, and converts the output into QTI (Question and Test Interoperability) format.

## Features

- **Query Interpretation:** Understand and process the search query provided by the user.
- **Content Generation:** Utilize a global search service to fetch information and generate quiz questions.
- **Formatting & Conversion:** Format generated questions and convert them into QTI files for easy integration with learning management systems.

## Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package installer)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/edumind-cli-tool.git
   cd edumind-cli-tool
   ```
2. **(Optional) Create and Activate a Virtual Environment:**

    ```bash
    Copy
    python3 -m venv venv
    source venv/bin/activate  # For Windows use: venv\Scripts\activate
    ```

3. **Install the Required Packages:**

    Make sure you have a requirements.txt file in the project directory. Then run:

    ```bash
    Copy
    pip install -r requirements.txt
    ```

## Configuration
1. **Create a .env File:**
    
    In the root directory of the project, create a file named .env.

2. **Add Your API Key:**

    Add your API key to the .env file with the following format:

    ```env
    GRAPHRAG_API_KEY=your_api_key_here
    ```
    Replace your_api_key_here with your actual API key.

## Usage
The CLI tool provides a generate command for creating quiz questions. You can run the function from the command line using the following syntax.

### Command Syntax

```bash
Copy
python main.py generate --query "your search query" --question_type "question type" --count number_of_questions
```

### Arguments
- `--query`: The search query for generating questions. (Example: "History of World War II")
- `--question_type`: The type of questions to generate. Examples include "multiple choice" or "multiple response correct".
- `--count`: The number of quiz questions to generate.

### Example
To generate 10 multiple choice questions about Docker application in Software Engineering, run:

```bash
python main.py generate --query "Why Dockers are used in Software Engineering" --question_type "multiple choice" --count 10
```

Upon successful execution, the script will:

1. Interpret the query.
2. Fetch information using the global search service.
3. Generate and format the quiz questions.
4. Convert the formatted questions into a QTI file.
5. Print the location of the generated QTI file.

## Project Structure

```bash
edumind-cli-tool/
│
├── main.py                      # Entry point for the CLI tool
├── requirements.txt             # Required Python packages
├── .env                         # Environment file containing the API key (to be created by the user)
│
├── search/
│   ├── global_search.py         # Module for fetching content from the global search service
│   └── query_interpretation.py  # Module for interpreting the search query
│
└── processing/
    ├── format_questions.py      # Module for formatting the generated questions
    └── csv_to_qti.py            # Module for converting CSV data to QTI format
```

Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

Contact
For questions or support, please open an issue in the repository or contact the maintainer at jaltareyr@gmail.com.