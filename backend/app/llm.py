import os
import openai
from pathlib import Path
import re
from pydantic_settings import BaseSettings
from flask import jsonify


# class Settings(BaseSettings):
#     api_key: str
#     frontend_url: str

#     class Config:
#         env_file = ".env"


# settings = Settings()

# openai.api_key
completion = openai.chat


def get_html_from_str(string: str):
    pattern = r"<!DOCTYPE html>.*?</html>"
    match = re.search(pattern, string, re.DOTALL)
    modified_string = re.sub(pattern, "", string, flags=re.DOTALL)
    html_document = match.group(0)
    return (modified_string, html_document)


def document_type(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You need to determine what the topic is in the given HTML document"""},
            {"role": "assistant", "content":  "The topic is an email"},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def topics(prompt):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """Determine the overral document structure simmiliar to the given document"""},
            {"role": "assistant", "content":  "The "},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


def analyze(prompt, standart, history: list, origin):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""You are a helpful assistant who needs to analyze and validate given document which was a {origin} format, converted to html.
            In you should give recommendations assuming this is still a file of {origin} format. Compare the
            document against this standard: {standart} of user's organisation and general look of documents of such types. You
            need to recommend autofill suggestions for
            incomplete sections is they are present, and if there is some  historical data: {history}, base it on it. Give the user's document overall score out of 10.
            Print your recommendations, suggest what other things the user may add based on the topic and type of the document. Account for formatting too. Fistly you type what the provided document is, meaning it's orignal format {origin}.
            Do not specify that it has been converted. Then the overall score which should be just
            some number out of 10, then
            by points recommendations for Autofill Suggestions, small conclusion. Do not use hashtags before topic names"""},
            {"role": "assistant", "content":  """The provided document is a ... Overall score: 10/10. Recommendations for Autofill Suggestions: ... Conclusion: ..."""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content


def human_correction(prompt, answer, text, history):
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"""You have to modify the original document {text}
             based on the points the user wants to modify. All the available
             points are here: {answer}. Take into account
             history of prompts and answers: {history}. Print the whole modified document as an answer.
             It always should start with <!DOCTYPE html>"""},
            # {"role" : "assistant", "content" :  """<"""},
            {"role": "user", "content": prompt}
        ]
    )
    history.append(prompt)
    history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content


def parse_check(prompt, standard, history, origin):
    response = analyze(prompt, standard, history, origin)

    # Clean up and print each section
    sections = re.split(
        r'(?i)(?=\b(The provided document is|Overall score|Recommendations for Autofill Suggestions|Conclusion):?)', response
    )

    # Combine headers with their respective content
    parsed_sections = []
    current_section = ""

    for part in sections:
        if re.match(r'(?i)\b(The provided document is|Overall score|Recommendations for Autofill Suggestions|Conclusion):?', part):
            if current_section:  # Save the previous section
                parsed_sections.append(current_section.strip())
            current_section = part  # Start a new section
        else:
            current_section += part  # Append content to the current section

    if current_section:  # Add the last section
        parsed_sections.append(current_section.strip())

    # Output each section
    # for i, section in enumerate(parsed_sections):
    #     print(f"Section {i}:\n{section}\n")

    # Check if sections match the expected ones
    if (
        len(parsed_sections) < 7 or  # Ensure we have at least 7 sections
        parsed_sections[0] != "The provided document is" or
        parsed_sections[2] != "Overall score" or
        parsed_sections[4] != "Recommendations for Autofill Suggestions" or
        parsed_sections[6] != "Conclusion"
    ):
        # If not matching, recursively call the function again
        return parse_check(prompt, standard, history, origin)
    else:
        # Return parsed sections if everything matches
        return parsed_sections
