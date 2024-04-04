scale_map = {
    'x': 2,
    'y': 2,
    'width': 100,
    'height': 40
}

def convert_value(value: str, name: str) -> int:
    value = float(value)
    if name in scale_map:
        value *= scale_map[name]
    
    value = int(value)
    return round_to_base(value) + 12  # required for the diagram to be displayed correctly
    

def round_to_base(int_number: int, base: int = 48) -> int:
    round_down = int_number % base
    round_up = base - round_down
    rounded = int_number + round_up if round_up < round_down else int_number - round_down
    if rounded == 0:
        return base
    return rounded
