# Helper functions

def convert_unit(value: float, unit_in: str, unit_out: str) -> float:
    multiplyer = {
        'm': 0.001,
        'k': 1000
    }
    # Determine unit_in Type and Multiplyer
    if len(unit_in) == 1:
        in_multiplyer = 1
        in_type = unit_in[0]
    else:
        in_multiplyer = multiplyer.get(unit_in[0])
        in_type = unit_in[1]

    # Determine unit_ouy Type and Multiplyer
    if len(unit_out) == 1:
        out_multiplyer = 1
        out_type = unit_out[0]
    else:
        out_multiplyer = multiplyer.get(unit_out[0])
        out_type = unit_out[1]

    # Check if units given are valid
    if (in_type != out_type):
        return None

    return value * in_multiplyer / out_multiplyer
