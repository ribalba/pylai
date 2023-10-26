#!/home/didi/code/pylai/venv/bin/python
# -*- coding: utf-8 -*-

import subprocess
import openai
import re
import sys
import dotenv

env_vars = dotenv.dotenv_values()

# Initialize the OpenAI API client
# If you want to set as a string
#openai.api_key = 'KEYHERE PLEASE'

# If you want to use .dotenv
openai.api_key = env_vars["OPENAI_API_KEY"]

def get_pylint_messages(file_name):
    """Run Pylint and get the linting messages."""
    result = subprocess.run(['pylint', file_name], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return output

def extract_issues_from_pylint(pylint_output):
    """Extract issues from the Pylint output."""
    # Split the output by lines and filter out lines with "***** Module" prefix
    lines = [line for line in pylint_output.split('\n') if not line.startswith('************* Module')]

    # Join the lines back to get the cleaned pylint output
    cleaned_output = '\n'.join(lines)

    # Format: "filename:line_number:column_number: message (message-id)"
    pattern = re.compile(r"([^:]+):(\d+):(\d+): (.*) \((.*)\)")
    matches = pattern.findall(cleaned_output)

    issues = [{
        'filename': match[0].strip(),
        'line': int(match[1]),
        'column': int(match[2]),
        'message': match[3],
        'message_id': match[4]
    } for match in matches]

    return issues


def get_fix_from_openai(issue, code_context):
    """Request a fix from the OpenAI API."""
    prompt = f"I have a Python code with an issue reported by Pylint: '{issue['message']}' at line {issue['line']} and column {issue['column']}. The relevant code is:\n{code_context}\nHow can I fix it?"
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=350)
    return response.choices[0].text.strip()

def apply_fix_to_code(file_name, issue, fix):
    """Apply the given fix to the code."""
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # This needs some matching logic as openai does not always return the full code lines
    with open(file_name, 'w') as file:
        file.writelines(lines)

def read_lines_around(filename, line_number, context=5):
    """Read a few lines around the given line number for context."""
    with open(filename, 'r') as file:
        lines = file.readlines()

    start = max(0, line_number - context - 1)
    end = min(len(lines), line_number + context)
    return lines[start:end]

def main():
    issues = extract_issues_from_pylint(sys.stdin.read())

    for issue in issues:
    #     # Get a context around the problematic line for better understanding
        code_context = "".join(read_lines_around(issue['filename'], issue['line']))
        print('')
        print(f"-------Issue: {issue['message']} in {issue['line']}")
        print(code_context)
        print('------> Fix')
        fix = get_fix_from_openai(issue, code_context)
        print(fix)

    #     apply_fix_to_code(file_name, issue, fix)


if __name__ == "__main__":
    main()
