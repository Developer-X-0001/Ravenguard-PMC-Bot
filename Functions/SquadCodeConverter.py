def squad_code_to_squad_name(input_str):
    callsign = ""
    numeric_part = ""
    
    if len(input_str) > 1:
        callsign = input_str[-1]
        numeric_part = input_str[:-1]
    
    numeric_part = int(numeric_part)
    
    if type(callsign) == int:
        return '00'
    
    if callsign == "B":
        callsign = "Bravo"
    elif callsign == "A":
        callsign = "Alpha"

    return callsign + " " + str(numeric_part)

