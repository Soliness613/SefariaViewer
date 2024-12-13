from rich.console import Console
from rich.panel import Panel
from bs4 import BeautifulSoup
import json
import re
import yaml

# Initialize the console for rich text rendering
console = Console()

# Function to parse HTML content and return a rendered output
def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    return str(soup)

# Function to display a specific span of cells from the "text" array
def render_text_span(json_data_english, json_data_hebrew, cell_index, colors, console):
    if "text" in json_data_english and isinstance(json_data_english["text"], list):
        try:
            # Fetch the specific outer list
            outer_cell_E = json_data_english["text"][cell_index]             
            outer_cell_H = json_data_hebrew["text"][cell_index]
            start_index = 0
            end_index = len(outer_cell_E) - 1
            
            if isinstance(outer_cell_E, list):                
                # Render the inner cells in the specified range
                for inner_index in range(start_index, end_index + 1):
                        cell_content_E = outer_cell_E[inner_index]
                        cell_content_H = outer_cell_H[inner_index]
                        cell_content_H = cell_content_H.split()
                        cell_content_H = cell_content_H[::-1]
                        cell_content_H = ' '.join(cell_content_H)
                        
                        # Parse and render HTML content
                        parsed_content_E = parse_html(cell_content_E)
                        pattern1 = r'L<small>ORD</small>'
                        replacement1 = f"[{colors['namesOfGod']}]LORD[/]"
                        parsed_content_E = re.sub(pattern1, replacement1, parsed_content_E)
                        parsed_content_E = re.sub(r'<br\s*/?>', '\n', parsed_content_E)
                        parsed_content_E = re.sub(r'<sup class="footnote-marker">.*?</sup><i class="footnote">.*?</i>', '', parsed_content_E)
                        parsed_content_E = re.sub(r'<.*>', '', parsed_content_E) 
                        parsed_content_E = f"[{colors['english']}]{parsed_content_E}[/]"
                        
                        parsed_content_H = parse_html(cell_content_H)
                        parsed_content_H = f"[{colors['hebrew']}]{parsed_content_H}[/]"
                        
                        # Combine parsed content with a line break as a plain string
                        parsed_content_combined = f"{parsed_content_E}\n\n{parsed_content_H}"
                        
                        # Display the content in a Rich Panel
                        title_color = f"{colors['title']}"
                        border_color = f"{colors['border']}"
                        console.print(Panel(parsed_content_combined, title=f"[{title_color}]{cell_index + 1}:{inner_index + 1}", border_style=f"{border_color}", expand=False))
                    
                    
            else:
                console.print("[bold red]Error:[/] The selected outer cell is not a list.")
        except IndexError:
            console.print(f"[bold red]Error:[/] Index out of bounds. {book} {cell_index + 1} has {len(outer_cell_E)} verses.")
    else:
        console.print("[bold red]Error:[/] No 'text' array found in JSON or it's not a list.")

# Main function
def main():
    # Specify Versions
    english_file_path = f"Tehillim_en.json"
    hebrew_file_path = f"Tehillim_he.json"

    # Load config gile

    with open ('config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    colors = config["colors"]

    # Try to load the JSON file
    try:
        with open(english_file_path, 'r', encoding='utf-8') as f:
            data_E = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not open or read the file: {e}")
        return  # Exit the script if the file cannot be loaded

    try:
        with open(hebrew_file_path, 'r', encoding='utf-8') as f:
            data_H = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not open or read the file: {e}")
        return
    # Ask the user for the cell index and range of inner indices
    console.print("[bold magenta]Which Psalm?")
    cell_index = int(input("")) - 1  # Get the outer index from the user

    # Check if the cell_index is within valid range for outer cells
    if cell_index < 0 or cell_index >= len(data_E["text"]) or cell_index >=len(data_H["text"]):
        console.print(f"[bold red]Error:[/] Chapter {cell_index} is out of bounds. The valid range is 1 to {len(data['text'])}.")
        return  # Exit if the cell index is invalid
    render_text_span(data_E, data_H, cell_index, colors, console)
# Run the main function
if __name__ == "__main__":
    main()
