from .util import BaseHighlighter, create_format


class TextFSMHighlighter(BaseHighlighter):
    def initialize_formats(self):
        """Initialize formats for TextFSM output"""
        self.formats = {
            'header': create_format("#569CD6"),  # Blue for header
            'data': create_format("#B5CEA8"),  # Light green for data
            'label': create_format("#CE9178"),  # Orange for labels
        }

    def highlightBlock(self, text: str):
        """Apply highlighting to TextFSM output"""
        if text.startswith("Header:"):
            self.setFormat(0, 7, self.formats['label'])  # "Header:" label
            self.setFormat(7, len(text) - 7, self.formats['header'])  # Header content

        elif text.startswith("Data:"):
            self.setFormat(0, 5, self.formats['label'])  # "Data:" label
        elif text.startswith("["):
            self.setFormat(0, len(text), self.formats['data'])  # Data content