from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from tempfile import NamedTemporaryFile
def generate_excel(mcqs: list):
    wb = Workbook()
    ws = wb.active
    ws.title = "MCQs"

    headers = [
        "Question",
        "Option A",
        "Option B",
        "Option C",
        "Option D",
        "Correct Answer",
        "Difficulty",
        "Points"
    ]

    ws.append(headers)

    # Header styling
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")

    # Data rows
    for mcq in mcqs:
        ws.append([
            mcq.get("question"),
            mcq.get("option_a"),
            mcq.get("option_b"),
            mcq.get("option_c"),
            mcq.get("option_d"),
            mcq.get("answer"),
            mcq.get("difficulty"),
            mcq.get("points")
        ])

    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[column_letter].width = max_length + 2

    # Save after formatting
    temp_file = NamedTemporaryFile(delete=False, suffix=".xlsx")
    wb.save(temp_file.name)

    return temp_file.name