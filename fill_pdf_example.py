# Example: Fill a D&D character sheet PDF using pdfrw
# Requires: pip install pdfrw

from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw import PdfDict

# Map your app's data to PDF field names here
CHARACTER_DATA = {
    'CharacterName': 'Testy McTestface',
    'ClassLevel': 'Wizard 5',
    'Background': 'Sage',
    'PlayerName': 'Matthew',
    'Race': 'Elf',
    'Alignment': 'CG',
    'XP': '6500',
    'STR': '10',
    'DEX': '14',
    'CON': '12',
    'INT': '18',
    'WIS': '13',
    'CHA': '8',
    # ...add more as needed
}

TEMPLATE_PATH = 'character_sheet_template.pdf'
OUTPUT_PATH = 'character_sheet_filled.pdf'

# Fill the PDF fields
def fill_pdf(input_pdf, output_pdf, data):
    pdf = PdfReader(input_pdf)
    for page in pdf.pages:
        annotations = page.Annots
        if annotations:
            for annotation in annotations:
                if annotation.Subtype == '/Widget' and annotation.T:
                    key = annotation.T[1:-1]  # Remove parentheses
                    if key in data:
                        annotation.V = str(data[key])
                        annotation.AP = ''
    PdfWriter().write(output_pdf, pdf)

# List all fields in the fillable PDF
def list_pdf_fields(pdf_path):
    pdf = PdfReader(pdf_path)
    print(f'Fields in {pdf_path}:')
    for page_num, page in enumerate(pdf.pages, 1):
        annots = page.Annots
        if annots:
            for annot in annots:
                if annot.Subtype == '/Widget' and annot.T:
                    field_name = annot.T[1:-1]  # Remove parentheses
                    tooltip = ''
                    if 'TU' in annot:
                        tooltip = annot['TU']
                        if isinstance(tooltip, str) and tooltip.startswith('(') and tooltip.endswith(')'):
                            tooltip = tooltip[1:-1]
                    print(f'Page {page_num}: Field name: {field_name}', end='')
                    if tooltip:
                        print(f' | Tooltip: {tooltip}')
                    else:
                        print()

if __name__ == '__main__':
    fill_pdf(TEMPLATE_PATH, OUTPUT_PATH, CHARACTER_DATA)
    print(f'Filled PDF saved as {OUTPUT_PATH}')
    print('\n--- PDF Field Listing ---')
    list_pdf_fields(TEMPLATE_PATH)
