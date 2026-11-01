"""Read-only checks of the exported service/sales component."""
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

PROJECT = Path(__file__).resolve().parents[2]
QA = PROJECT / '08-qa/t05s-workbook'
verification = json.loads((QA / 'verification.json').read_text())
cell_map = json.loads((QA / 'cell-map.json').read_text())
file = Path(verification['workbook_path'])
file_hash = hashlib.sha256(file.read_bytes()).hexdigest()
assert file_hash == verification['workbook_sha256']
assert cell_map['quantity_input_column'] == 'D'
ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
checks = []

def check(detail, passed):
    checks.append({'passed': bool(passed), 'detail': detail})
    assert passed, detail

with zipfile.ZipFile(file) as archive:
    wb = ET.fromstring(archive.read('xl/workbook.xml'))
    check('Two named worksheets retained in order', [x.attrib['name'] for x in wb.findall('m:sheets/m:sheet', ns)] == ['Service cost', 'Inputs'])
    shared = [''.join(x.itertext()) for x in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
    sheets = [ET.fromstring(archive.read(f'xl/worksheets/sheet{i}.xml')) for i in [1, 2]]
    cells = [{x.attrib['r']: x for x in s.findall('.//m:sheetData/m:row/m:c', ns)} for s in sheets]

    def value(sheet, address):
        cell = cells[sheet].get(address)
        if cell is None:
            return None
        v = cell.find('m:v', ns)
        if v is None:
            return None
        kind = cell.attrib.get('t')
        if kind == 's':
            return shared[int(v.text)]
        return v.text if kind in ['str', 'e'] else float(v.text)

    check('Programme hours and cost retain explicit unavailable cached results', value(0, 'E6') == value(0, 'E7') == 'n.a.')
    check('Working briefing unit retains five hours and GBP248 comparison', value(0, 'C20') == 5 and value(0, 'F20') == 248)
    check('Fifteen programme quantities remain blank', all(value(1, f'D{r}') is None for r in range(19, 34)))
    check('Commercial value remains blank and active hourly rate unavailable', value(1, 'E14') is None and value(1, 'F14') == 'n.a.')
    check('Case selector and day divisor saved in restored state', value(1, 'D4') == 2 and value(1, 'F8') == 7.5)
    check('Final partner label identifies administration rather than a full package', value(0, 'B18') == 'Partner administration')
    check('Hours and programme totals contain formulas', all(cells[0][a].find('m:f', ns) is not None for a in ['C20', 'F20', 'H26', 'I26']))
    check('Input case and quantity validation retained', sheets[1].find('m:dataValidations', ns) is not None)
    check('No external workbook dependency', not any(x.startswith('xl/externalLinks/') for x in archive.namelist()))
    check('Pasted-text selector guard retained in export', cells[1]['F4'].find('m:f', ns).text.startswith('IF(ISNUMBER(D4),IF('))

old = PROJECT.parent.parent / 'outputs/jga-t05-research-costs-2026-10-31/Research staffing costs.xlsx'
check('First research workbook untouched', hashlib.sha256(old.read_bytes()).hexdigest() == 'b28a46219d4a74fdf49afc35f6f084aaac024ef403d0cc30dc4f683541b36677')
(QA / 'export-check.json').write_text(json.dumps({'date': '2026-11-01', 'status': 'passed', 'workbook_path': str(file), 'workbook_sha256': file_hash, 'checks': checks, 'native_Excel_application_tested': False, 'scope': 'Saved OpenXML structure, restored inputs, cached outputs and formula presence, not native Excel execution.'}, indent=2) + '\n')
print(json.dumps({'saved_file_checks': len(checks), 'workbook_sha256': file_hash}))
