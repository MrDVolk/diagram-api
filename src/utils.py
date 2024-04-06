scale_map = {
    'x': 2,
    'y': 2,
    'width': 100,
    'height': 40
}

correction_map = {
    'x': 12,
    'y': 12,
    'width': 0,
    'height': 0
}

def convert_value(value: str, name: str) -> int:
    value = float(value)
    if name in scale_map:
        value *= scale_map[name]

    value = round_to_base(int(value))
    correction = correction_map.get(name, 0)
    
    return value + correction
    

def round_to_base(int_number: int, base: int = 48) -> int:
    round_down = int_number % base
    round_up = base - round_down
    rounded = int_number + round_up if round_up < round_down else int_number - round_down
    if rounded == 0:
        return base
    return rounded
