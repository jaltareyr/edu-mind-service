import pandas as pd
import json
from datetime import datetime

def format_questions(result):

    start_tag = result.find('<JSON>')
    end_tag = result.find('</JSON>')

    if start_tag != -1 and end_tag != -1:
        json_content = result[start_tag + 6:end_tag]

    data = json.loads(json_content)

    formatted_data = []
    for item in data:
        question_type = "MR" if len(item["correct_options"]) > 1 else "MC"
        correct_answers = ",".join([str(opt + 1) for opt in item["correct_options"]])

        row = {
            "Type": question_type,
            "Unused": "",
            "Points": "1",
            "Question": item["question"],
            "CorrectAnswer": correct_answers
        }

        for i in range(5):
            row[f"Option {chr(65 + i)}"] = item["options"][i] if i < len(item["options"]) else ""

        formatted_data.append(row)

    df = pd.DataFrame(formatted_data)
    csv_filename = f"questions_{datetime.now().strftime("%H%M%S%d%m%y")}"
    csv_filepath = f"output/csv/{csv_filename}.csv"
    df.to_csv(csv_filepath, index=False)
    return csv_filename