import re

def remove_styles_from_html(html_content):
    """
    Removes all 'style' attributes from the given HTML content.

    :param html_content: The HTML string to clean.
    :return: The cleaned HTML string.
    """
    # Remove all style attributes
    html_content = re.sub(r'<(\w+)[^>]*>\s*(?:&nbsp;|\s)*<\/\1>', '', html_content)
    cleaned_html = re.sub(r'style="[^"]*"', '', html_content).strip()
    return cleaned_html

# Read HTML content from input file
with open("removeStyleTag/input.txt", "r") as input_file:
    html_content = input_file.read()

# Process the HTML to remove styles
cleaned_html = remove_styles_from_html(html_content)

# Write the cleaned HTML to output file
with open("removeStyleTag/output.txt", "w") as output_file:
    output_file.write(cleaned_html)

print("HTML cleaned and written to output.html")
