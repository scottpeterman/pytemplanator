from typing import Tuple

class CodeGenerator:
    @staticmethod
    def get_example_data(template_name: str) -> Tuple[str, str]:
        """Returns (source, code) for a given template"""
        examples = {
            'textfsm': (
                "",  # Source handled by CDPExamples
                '''import textfsm

# Read command output
with open('show_commands.txt', 'r') as f:
    cmd_output = f.read()

# Parse with TextFSM template
with open('template.textfsm', 'r') as f:
    template = textfsm.TextFSM(f)
    result = template.ParseText(cmd_output)

# Print structured data
print(f"Headers: {template.header}")
for row in result:
    for field, value in zip(template.header, row):
        if value:
            print(f"{field}: {value}")'''
            ),
            'ttp': (
                "",  # Source handled by CDPExamples
                '''from ttp import ttp

# Read command output
with open('show_commands.txt', 'r') as f:
    cmd_output = f.read()

# Parse with TTP template
parser = ttp(data=cmd_output)
parser.parse()

# Print results as JSON
import json
print(json.dumps(parser.result()[0], indent=2))'''
            )
        }
        return examples.get(template_name, ("", ""))