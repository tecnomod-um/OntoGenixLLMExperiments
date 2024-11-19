# Define the function to modify the TTL file and save it as TXT
def modify_ttl_to_txt(ttl_file, txt_file):
    try:
        # Open the TTL file and read its content
        with open(ttl_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Add the "```turtle" at the beginning and "```" at the end
        modified_content = "```turtle\n" + content + "\n```"

        # Write the modified content into a TXT file
        with open(txt_file, 'w', encoding='utf-8') as file:
            file.write(modified_content)

        print(f"File successfully converted and saved as {txt_file}")
    except Exception as e:
        print(f"Error: {e}")

# Call the function with the desired files
modify_ttl_to_txt('./ontologies_vs/afo.ttl', './ontologies_vs/afo.txt')
