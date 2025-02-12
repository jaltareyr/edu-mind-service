EduMind CLI

EduMind is a Python-based CLI tool for generating quiz questions on various topics. It interacts with a search service to fetch relevant questions and converts them into a standard format.

Prerequisites

Ensure you have the following installed on your system:

Python 3.8+

Pip

Installation

Clone the repository:

git clone https://github.com/your-username/edumind.git
cd edumind

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Running EduMind

To run EduMind without parameters, simply execute:

python edumind.py

This will display the CLI options available for generating quiz questions.

Usage

To generate quiz questions with parameters, use:

python edumind.py generate --query "Frontend development" --question_type "multiple choice" --count 5

Environment Variables

If you are using an API key, create a .env file in the root directory and add:

API_KEY=your_secret_api_key_here

Contributing

Fork the repository.

Create a new branch (feature-branch).

Commit your changes.

Push to the branch and submit a pull request.

License

This project is licensed under the MIT License.

