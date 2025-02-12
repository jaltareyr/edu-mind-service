import csv
import xml.etree.ElementTree as ET
import zipfile
import os

def convert_csv_to_qti(csv_filename):

    xml_filename = f"qti_{csv_filename.split("_")[1]}"
    zip_filename = f"zip_{csv_filename.split("_")[1]}"

    # Register QTI namespace
    ET.register_namespace("", "http://www.imsglobal.org/xsd/ims_qtiasiv1p2")

    # Read CSV file
    questions = []
    with open(f"output/csv/{csv_filename}.csv", 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        for row in reader:
            questions.append(row)

    # Create QTI XML root element
    root = ET.Element(
        'questestinterop',
        {
            "xmlns": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd"
        }
    )

    # Create Assessment
    assessment = ET.SubElement(root, 'assessment', ident="i478669c7fa549970e36eac591cdca62e", title=f"Quiz - {csv_filename.split("_")[1]}")

    # QTI Metadata
    qtimetadata = ET.SubElement(assessment, 'qtimetadata')
    qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
    fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
    fieldlabel.text = "cc_maxattempts"
    fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
    fieldentry.text = "1"

    # Create root section
    section = ET.SubElement(assessment, 'section', ident="root_section")

    # Iterate through questions and add to XML
    for index, row in enumerate(questions):
        question_type = row[0]  # MC (Multiple Choice) or MR (Multiple Response)
        point_value = row[2]
        question_body = row[3]
        correct_answers = row[4].split(';')  # Can be multiple for MR
        answer_choices = row[5:10]  # Columns F-J

        # Filter out empty answer choices
        valid_answers = [(idx + 1, choice) for idx, choice in enumerate(answer_choices) if choice.strip()]

        # Create Item
        item = ET.SubElement(section, 'item', ident=f"Q{index+1}", title=f"Question {index+1}")

        # Set Item Metadata
        itemmetadata = ET.SubElement(item, 'itemmetadata')
        qtimetadata = ET.SubElement(itemmetadata, 'qtimetadata')

        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "question_type"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = "multiple_choice_question" if question_type == "MC" else "multiple_response_question"

        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "points_possible"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = point_value

        qtimetadatafield = ET.SubElement(qtimetadata, 'qtimetadatafield')
        fieldlabel = ET.SubElement(qtimetadatafield, 'fieldlabel')
        fieldlabel.text = "assessment_question_identifierref"
        fieldentry = ET.SubElement(qtimetadatafield, 'fieldentry')
        fieldentry.text = f"i{index+1:06d}"

        # Presentation Section
        presentation = ET.SubElement(item, 'presentation')
        material = ET.SubElement(presentation, 'material')
        mattext = ET.SubElement(material, 'mattext', texttype="text/html")
        mattext.text = question_body

        # Set response mode: Single vs. Multiple selection
        response_lid = ET.SubElement(presentation, 'response_lid', ident="response1")
        response_lid.set("rcardinality", "Multiple" if question_type == "MR" else "Single")

        render_choice = ET.SubElement(response_lid, 'render_choice')

        # Add each valid answer option
        for idx, option_text in valid_answers:
            option_id = f"{index+1}{idx:03d}"  # Unique identifier for choices
            response_label = ET.SubElement(render_choice, 'response_label', ident=option_id)

            material = ET.SubElement(response_label, 'material')
            mattext = ET.SubElement(material, 'mattext', texttype="text/plain")
            mattext.text = option_text

        # Response Processing
        resprocessing = ET.SubElement(item, 'resprocessing')
        
        # Set Outcomes
        outcomes = ET.SubElement(resprocessing, "outcomes")
        decvar = ET.SubElement(outcomes, "decvar", maxvalue=point_value, minvalue="0", varname="SCORE", vartype="Decimal")

        # Set Response Conditions
        respcondition = ET.SubElement(resprocessing, 'respcondition', attrib={"continue": "No"})  # FIXED SYNTAX ERROR
        conditionvar = ET.SubElement(respcondition, 'conditionvar')

        # Allow multiple correct answers in response processing
        for correct_option in correct_answers:
            correct_option = correct_option.strip()
            if correct_option:
                correct_option_id = f"{index+1}{int(correct_option):03d}"
                varequal = ET.SubElement(conditionvar, 'varequal', respident="response1")
                varequal.text = correct_option_id

        setvar = ET.SubElement(respcondition, "setvar", action="Set", varname="SCORE")
        setvar.text = point_value

    # Write to QTI XML file
    tree = ET.ElementTree(root)
    tree.write(f"output/qti/{xml_filename}.qti", encoding='ISO-8859-1', xml_declaration=True)

    # Create a ZIP file
    with zipfile.ZipFile(f"output/zip/{zip_filename}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f"output/qti/{xml_filename}.qti", os.path.basename(f"{xml_filename}.qti"))
        return xml_filename