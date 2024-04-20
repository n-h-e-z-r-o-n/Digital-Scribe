def modify_css(css_file_path):
    # Read the content of the CSS file

    css_style = """
    /* Your CSS styles go here */
    body {
        background-color: #f0f0f0;
        color: white
    }
    """

    # Write the modified content back to the CSS file
    with open(css_file_path, 'w') as file:
        file.write(css_style)

# Example usage:
css_file_path = './html/styles.css'  # Path to your CSS file
modify_css(css_file_path)