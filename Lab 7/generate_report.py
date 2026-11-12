from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    PageBreak, KeepTogether
)
from reportlab.lib.utils import ImageReader
from pathlib import Path

BASE = Path(__file__).parent
SCREENSHOTS = BASE / "screenshots"
OUTPUT = BASE / "Lab_7_Fuzz_Testing_Report.pdf"

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=0.65 * inch,
    leftMargin=0.65 * inch,
    topMargin=0.65 * inch,
    bottomMargin=0.65 * inch,
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    textColor=colors.HexColor("#17365D"),
    fontSize=22,
    leading=28,
    spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="Section",
    parent=styles["Heading2"],
    textColor=colors.HexColor("#17365D"),
    spaceBefore=12,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="SmallBody",
    parent=styles["BodyText"],
    fontSize=9,
    leading=13,
    spaceAfter=7,
))

story = []

def para(text, style="SmallBody"):
    story.append(Paragraph(text, styles[style]))

def add_screenshot(filename, caption):
    path = SCREENSHOTS / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing screenshot: {path}")

    reader = ImageReader(str(path))
    width, height = reader.getSize()

    max_width = 7.0 * inch
    max_height = 8.2 * inch
    scale = min(max_width / width, max_height / height)

    img = Image(
        str(path),
        width=width * scale,
        height=height * scale,
    )

    story.append(Paragraph(caption, styles["Section"]))
    story.append(img)
    story.append(Spacer(1, 10))

# Title and overview
para("LAB 7: FUZZ TESTING", "ReportTitle")
para("<b>Experiment:</b> Finding and fixing bugs using Hypothesis")
para("<b>Programming language:</b> Python 3.12.10")
para("<b>Testing framework:</b> pytest")
para("<b>Fuzz testing library:</b> Hypothesis 6.170.15")
para("<b>Student:</b> Vijay Kumar")
story.append(Spacer(1, 12))

para("1. Objective", "Section")
para(
    "The objective of this experiment is to explore fuzz testing using "
    "the Hypothesis library. Property-based tests generate a variety of "
    "inputs automatically to identify unexpected failures in Python "
    "functions. The discovered bugs are corrected and the tests are "
    "executed again to verify the fixes."
)

para("2. Functions Tested", "Section")
para(
    "<b>first_character_type(pw):</b> Identifies whether the first "
    "character is a digit, letter, or symbol.<br/>"
    "<b>split_credentials(text):</b> Splits a username and password "
    "separated by a colon.<br/>"
    "<b>digit_ratio(pw):</b> Calculates the proportion of digits in "
    "a string."
)

para("3. Original Program Execution", "Section")
para(
    "The original application was executed with normal inputs to verify "
    "its expected behavior before fuzz testing."
)
add_screenshot("01_original_output.png", "Screenshot 1: Original program execution")

story.append(PageBreak())
para("4. Bugs Discovered Using Hypothesis", "Section")
para(
    "Hypothesis generated empty strings and None values that exposed "
    "six distinct failure cases across the three functions:"
)
para(
    "<b>first_character_type:</b> Empty input caused IndexError; "
    "None caused TypeError.<br/>"
    "<b>split_credentials:</b> Empty input caused ValueError; "
    "None caused AttributeError.<br/>"
    "<b>digit_ratio:</b> Empty input caused ZeroDivisionError; "
    "None caused TypeError."
)
para(
    "The following screenshots show the failing test output and the "
    "minimal failing examples reported by Hypothesis."
)
add_screenshot("02_failing_tests_1.png", "Screenshot 2: Hypothesis failure output (part 1)")
story.append(PageBreak())
add_screenshot("02_failing_tests_2.png", "Screenshot 3: Hypothesis failure output (part 2)")

story.append(PageBreak())
para("5. Bug Fixes Implemented", "Section")
para(
    "The application was updated to handle invalid and empty inputs "
    "without crashing:"
)
para(
    "<b>first_character_type:</b> Returns 'unknown' for empty or "
    "non-string inputs.<br/>"
    "<b>split_credentials:</b> Returns ('', '') when the input is "
    "not a string or does not contain a colon. The partition method "
    "allows additional colons in the password.<br/>"
    "<b>digit_ratio:</b> Returns 0.0 for empty or non-string inputs."
)
para(
    "Normal valid inputs retain their original behavior."
)

para("6. Re-testing After Fixes", "Section")
para(
    "The same three Hypothesis tests were executed again against the "
    "corrected application. All three tests passed."
)
add_screenshot("03_passing_tests.png", "Screenshot 4: All Hypothesis tests passing")

story.append(PageBreak())
para("7. Corrected Program Execution", "Section")
para(
    "The corrected application was executed with normal inputs. "
    "It continued to classify the first character, split credentials, "
    "and calculate the digit ratio correctly."
)
add_screenshot("04_fixed_program_output.png", "Screenshot 5: Corrected application output")

story.append(PageBreak())
para("8. Edge-Case Validation", "Section")
para(
    "Additional manual checks were performed using empty strings and "
    "None values. The functions returned safe values instead of raising "
    "exceptions."
)
para(
    "<b>Expected results:</b> unknown, unknown, ('', ''), ('', ''), "
    "0.0, and 0.0."
)
add_screenshot("05_edge_case_validation.png", "Screenshot 6: Edge-case validation")

para("9. Conclusion", "Section")
para(
    "The experiment demonstrated how property-based fuzz testing can "
    "automatically discover unexpected input-related bugs. Hypothesis "
    "identified six failure cases in the original implementation. "
    "After defensive input handling was added, all three property-based "
    "tests passed, and normal program behavior was preserved."
)

para("10. Deliverable Files", "Section")
para(
    "The submission includes the corrected processor.py application, "
    "the updated test_processor.py Hypothesis tests, requirements.txt, "
    "the screenshots, and this PDF report."
)

doc.build(story)
print(f"Report created successfully: {OUTPUT}")
