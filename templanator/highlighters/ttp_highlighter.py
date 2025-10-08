from .util import BaseHighlighter, create_format


class TTPHighlighter(BaseHighlighter):
    def initialize_formats(self):
        """Initialize formats for JSON output"""
        self.formats = {
            'string': create_format("#CE9178"),  # Orange for strings
            'number': create_format("#B5CEA8"),  # Light green for numbers
            'bool': create_format("#569CD6"),  # Blue for booleans and null
            'null': create_format("#569CD6"),  # Blue for null
            'brackets': create_format("#D4D4D4"),  # Light gray for brackets
            'key': create_format("#9CDCFE"),  # Light blue for JSON keys
        }

    def highlightBlock(self, text: str):
        """Apply highlighting to JSON output"""
        in_string = False
        in_key = False
        start = 0

        for i, char in enumerate(text):
            if char == '"':
                if not in_string:
                    start = i
                    in_string = True
                    # Check if this is a key (followed by :)
                    in_key = i + 1 < len(text) and ':' in text[
                                                          i + 1:text.find(',', i + 1) if ',' in text[i + 1:] else len(
                                                              text)]
                else:
                    length = i - start + 1
                    self.setFormat(start, length,
                                   self.formats['key'] if in_key else self.formats['string'])
                    in_string = False
                    in_key = False
            elif not in_string:
                # Handle numbers
                if char.isdigit() or char in '.-':
                    self.setFormat(i, 1, self.formats['number'])
                # Handle brackets and punctuation
                elif char in '[]{},:':
                    self.setFormat(i, 1, self.formats['brackets'])
                # Handle boolean and null values
                elif text[i:].startswith('true') or text[i:].startswith('false'):
                    self.setFormat(i, 4 if text[i:i + 4] == 'true' else 5, self.formats['bool'])
                elif text[i:].startswith('null'):
                    self.setFormat(i, 4, self.formats['null'])