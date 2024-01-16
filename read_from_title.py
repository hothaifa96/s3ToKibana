import math

import pandas as pd

import subprocess
import boto3
import os

# AWS CLI sync command
sync_command = ["aws", "s3", "sync", "s3://itaybuck", ".", "--exclude", "img/*" , "--exclude", "*.zip" , "--exclude","ארתמטיקה כתה ד.xlsx"]

# Execute AWS CLI sync command
subprocess.run(sync_command)

# List all files with extension .xlsx in the current directory
files = [file for file in os.listdir('.') if file.endswith('.xlsx')]
for f in files:
    print(f)
print(len(files))

for url in files:
    df = pd.read_excel(url)

    # Create SQL file for INSERT commands
    with open('./all.sql', 'a+', encoding='utf-8') as insert_data_file:
        insert_data_file.write(f'-- new file here {url[url.rfind("/") + 1:]}--\n')

        # Insert data into topics table (avoid duplicates)
        inserted_topics = set()
        for index, row in df.iterrows():
            try:
                topic_id = int(str(row.iloc[1])[2:6])  # Assuming the 'מזהה' column is topic_id
            except:
                continue
            if topic_id not in inserted_topics:

                topic_name = row.iloc[0]  # Assuming the 'נושאים מקדימים' column is topic_name
                insert_data_file.write(
                    f"INSERT INTO topics (topic_id, topic_name) VALUES ({topic_id}, '{topic_name}') ON CONFLICT (topic_id) DO NOTHING;\n")
                inserted_topics.add(topic_id)

        # Insert data into questions and answer_options tables
        for index, row in df.iterrows():
            question_id = str(row.iloc[1])  # Assuming the 'מזהה' column is question_id
            language_id = 1  # You can change this value based on your requirements
            # if not str(row.iloc[1]).isdigit():
            #     continue
            try:
                topic_id = int(str(row['מזהה'])[2:6])
            except:
                continue
            c_grade_id = int(question_id[-1])  # Set c_grade_id to the last digit of question_id
            level = int(question_id[-1])
            question_text = row['שאלה'].replace("'", "`") if isinstance(row['שאלה'], str) else row[
                'שאלה']  # Assuming the 'שאלה' column is question_text
            if 'ארתמטיקה' in url :
                explanation = str(row['הסבר']).replace("'", "`") if isinstance(row['הסבר'], str) else row['הסבר']   # You can add explanation if available in your dataset
                interesting_fact =""
            else:
                explanation = ""
                interesting_fact = row['עובדה מעניינת'].replace("'", "`") if isinstance(row['עובדה מעניינת'], str) else row['עובדה מעניינת']  # Assuming the 'אפשרות_4' column is interesting_fact

            insert_data_file.write(f"""
    INSERT INTO questions (question_id, language_id, topic_id, c_grade_id, level, question_text, explanation, interesting_fact)
    VALUES ('{question_id}', {language_id}, {topic_id}, {c_grade_id}, {level}, '{question_text}', '{explanation}', '{interesting_fact}') ON CONFLICT (question_id) DO UPDATE SET language_id = {language_id} ,topic_id= {topic_id},c_grade_id ={c_grade_id},level={level},question_text='{question_text}',explanation='{explanation}',interesting_fact='{interesting_fact}';

    """)

            correct_answer = row['אפשרות1_נכונה'].replace("'", "`") if isinstance(row['אפשרות1_נכונה'], str) else row[
                'אפשרות1_נכונה']  # Assuming the 'אפשרות1_נכונה' column is correct_answer
            insert_data_file.write(f"""
    INSERT INTO answer_options (question_id, correct_answer, answer_text)
    VALUES ('{question_id}', TRUE, '{correct_answer}') ;
    """)

            wrong_answers = [row['אפשרות_2'], row['אפשרות_3'], row[
                'אפשרות_4']]  # Assuming columns 'אפשרות_2', 'אפשרות_3', and 'אפשרות_4' are wrong answers
            for i, answer in enumerate(wrong_answers):
                insert_data_file.write(f"""
    INSERT INTO answer_options (question_id, correct_answer, answer_text)
    VALUES ('{question_id}', FALSE, '{answer.replace("'", "`") if isinstance(answer, str) else answer}');
    """)

    print("INSERT commands SQL file generated successfully.")
