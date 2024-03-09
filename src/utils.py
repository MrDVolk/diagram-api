scale_map = {
    'x': 2,
    'y': 1.5,
    'width': 100,
    'height': 40
}

def convert_value(value: str, name: str) -> int:
    value = float(value)
    if name in scale_map:
        value *= scale_map[name]
    
    value = int(value)
    return round_to_base(value)
    

def round_to_base(int_number: int, base: int = 48) -> int:
    round_up = int_number % base
    round_down = base - round_up
    rounded = int_number + round_down if round_down < round_up else int_number - round_up
    if rounded == 0:
        return base
    return rounded
