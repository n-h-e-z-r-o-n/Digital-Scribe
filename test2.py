def modify_css(css_file_path):
    # Read the content of the CSS file
    try:
    with open(css_file_path, 'r') as file:
        css_content = file.read()
    
    # Modify the CSS content (for demonstration, let's add a new style)
    new_style = "\n/* New Style */\n"
    new_style += "h2 {\n"
    new_style += "    color: green;\n"
    new_style += "}\n"

    modified_css_content = css_content + new_style

    # Write the modified content back to the CSS file
    with open(css_file_path, 'w') as file:
        file.write(modified_css_content)

# Example usage:
css_file_path = 'styles.css'  # Path to your CSS file
modify_css(css_file_path)