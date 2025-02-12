import os
import argparse
import asyncio
from search.global_search import GlobalSearchService
from search.query_interpretation import QueryInterpreter
from processing.format_questions import format_questions
from processing.csv_to_qti import convert_csv_to_qti

# Read API Key from environment variables
API_KEY = os.getenv("API_KEY")

async def generate_questions(query: str, question_type: str, count: int):
    if not API_KEY:
        print("Error: API_KEY is not set!")
        return

    print(f"Using API Key: {API_KEY[:5]}...")  # Only print part of the key for security

    interpreter = QueryInterpreter(api_key=API_KEY)
    query_data = await interpreter.interpret_query(query)

    search_service = GlobalSearchService(api_key=API_KEY)
    result = await search_service.search(query_data, question_type, count)

    csv_filename = format_questions(result)
    qti_filename = convert_csv_to_qti(csv_filename)

    print(f"Generated QTI file: {qti_filename}")

def main():
    parser = argparse.ArgumentParser(description="EduMind CLI Tool for generating quiz questions.")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate", help="Generate quiz questions")
    generate_parser.add_argument("--query", required=True, help="The search query for question generation")
    generate_parser.add_argument("--question_type", required=True, help="Type of question (e.g., multiple choice, multiple response correct)")
    generate_parser.add_argument("--count", type=int, required=True, help="Number of questions to generate")

    args = parser.parse_args()

    if args.command == "generate":
        asyncio.run(generate_questions(args.query, args.question_type, args.count))

if __name__ == "__main__":
    main()