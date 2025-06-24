import re
serial_number = "	LI/LSI/LDI 25/1283419-2 - 62H028754"
serial_regex = "\b(\d{2}[A-Z]\d{6})\b"

patern = serial_regex.replace("\\", "\\\\")  # Escapar barras invertidas para regex

print(patern)
    
serial_para_usar = serial_number
if serial_regex:
    match = re.search(serial_regex, serial_number)
    if match:
        serial_para_usar = match.group(1)
        print(f"Número de série tratado pela regex: '{serial_para_usar}'")
    else:
        print(f"Regex '{serial_regex}' não encontrou correspondência. Usando número de série original.")