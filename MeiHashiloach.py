from rich.console import Console
from rich.panel import Panel
from bs4 import BeautifulSoup
import json
import re

# Initialize the console for rich text rendering
console = Console()

# Function to parse HTML content and return a rendered output
def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    return str(soup)

# Function to display a specific span of cells from the "text" array
def render_text_span(json_data_english, cell_index, start_index, end_index, console):
    if "text" in json_data_english and isinstance(json_data_english["text"], list):
        try:
            # Fetch the specific outer list
            outer_cell_E = json_data_english["text"][cell_index]
            if isinstance(outer_cell_E, list):
                        # Check if the range is within bounds
                if start_index < 0 or end_index >= len(outer_cell_E):
                    console.print(f"[bold red]Error:[/] Index out of bounds. Valid range for inner cells is 0 to {len(outer_cell) - 1}.")
                    return
                
                # Render the inner cells in the specified range
                for inner_index in range(start_index, end_index + 1):
                    cell_content_E = outer_cell_E[inner_index]\
                    # Parse and render HTML content
                    parsed_content_E = parse_html(cell_content_E)
                    parsed_content_E = re.sub(r'<.*>', '', parsed_content_E) 
                    parsed_content_E = f"[bold blue]{parsed_content_E}[/]"
                    console.print(Panel(parsed_content_E, expand=False))
            else:
                console.print("[bold red]Error:[/] The selected outer cell is not a list.")
        except IndexError:
            console.print(f"[bold red]Error:[/] Index out of bounds. Cell index: {cell_index}, Start index: {start_index}, End index: {end_index}.")
    else:
        console.print("[bold red]Error:[/] No 'text' array found in JSON or it's not a list.")

# Main function
def main():
    # Specify Versions
    english_file_path = "MeiHashiloachVayishlach.json"

    # Try to load the JSON file
    try:
        with open(english_file_path, 'r', encoding='utf-8') as f:
            data_E = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not open or read the file: {e}")
        return  # Exit the script if the file cannot be loaded

    cell_index = 0# Get the outer index from the user
    index_range = "0-37"  # Get the range as a string (e.g., "7-29")

    # Parse the index range into start_index and end_index
    try:
        # Ensure the input format is correct (two numbers separated by a hyphen)
        start_index, end_index = map(int, index_range.split('-'))
        
    except ValueError:
        console.print("[bold red]Error:[/] Invalid input format. Please enter two numbers separated by a hyphen (e.g., 7-29).")
        return  # Exit if the format is invalid


    # Display the specified span of cells
    render_text_span(data_E, cell_index, start_index, end_index, console)
# Run the main function
if __name__ == "__main__":
    main()
