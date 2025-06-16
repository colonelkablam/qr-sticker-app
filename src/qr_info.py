# src/qr_info.py

def get_qr_capacity_lookup():
    # Approximate max character capacities for versions 1–8 (UTF-8/alphanumeric)
    return {
        "L": [25, 47, 77, 114, 154, 195, 224, 279],
        "M": [20, 38, 61, 90, 122, 154, 178, 221],
        "Q": [16, 29, 47, 67, 87, 108, 125, 157],
        "H": [10, 20, 35, 50, 64, 84, 93, 122],
    }

def get_module_size(version: int) -> int:
    """Returns the number of modules (blocks) per side of the QR code."""
    return 21 + (version - 1) * 4

def get_max_chars(version: int, level: str) -> int:
    """Returns the approximate max number of characters for version + error level."""
    table = get_qr_capacity_lookup()
    if 1 <= version <= 8 and level in table:
        return table[level][version - 1]
    return -1  # unsupported or unknown