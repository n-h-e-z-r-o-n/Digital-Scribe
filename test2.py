def modify_css_file(file_path, modification_function):
    # Read the content of the CSS file
    with open(file_path, 'r') as file:
        css_content = file.read()

    # Apply the modification function to the CSS content
    modified_css_content = modification_function(css_content)

    # Write the updated CSS content back to the file
    with open(file_path, 'w') as file:
        file.write(modified_css_content)

def add_custom_style(css_content):
    # Add custom CSS rules
    custom_css = """
    /* Custom styles */
    .custom-class {
        color: red;
        font-weight: bold;
    }
    """
    # Append the custom CSS rules to the existing content
    modified_css_content = css_content + custom_css
    return modified_css_content

# Example usage: modify the CSS file by adding custom styles
modify_css_file('styles.css', add_custom_style)