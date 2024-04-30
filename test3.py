def lighten_hex_color(hex_color, factor=0.2):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')

    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Increase RGB values to lighten the color
    r = min(255, int(r * (1 + factor)))
    g = min(255, int(g * (1 + factor)))
    b = min(255, int(b * (1 + factor)))

    # Convert back to hex
    light_hex = "#{:02x}{:02x}{:02x}".format(r, g, b)

    return light_hex


# Example usage
original_color = "#36454F"  # Original color: blue
lighter_color = lighten_hex_color(original_color, factor=0.2)
print("Original color:", original_color)
print("Lighter color:", lighter_color)