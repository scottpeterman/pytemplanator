from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor


def create_format(color: str) -> QTextCharFormat:
    """Create a QTextCharFormat with the specified color

    Args:
        color (str): Color in hex format (e.g. '#CE9178')

    Returns:
        QTextCharFormat: Formatted text style
    """
    fmt = QTextCharFormat()
    fmt.setForeground(QColor(color))
    return fmt


class BaseHighlighter(QSyntaxHighlighter):
    """Base class for syntax highlighters

    This base class provides common functionality for syntax highlighters
    and defines the interface that derived classes should implement.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.formats = {}  # Will store the different formats for highlighting
        self.initialize_formats()

    def initialize_formats(self):
        """Initialize the format dictionary with QTextCharFormats

        This method should be overridden by derived classes to set up
        their specific color schemes and formats.
        """
        raise NotImplementedError("Derived classes must implement initialize_formats")

    def highlightBlock(self, text: str):
        """Perform the syntax highlighting

        Args:
            text (str): The text block to highlight
        """
        raise NotImplementedError("Derived classes must implement highlightBlock")