from rich.console import Console
from rich.panel import Panel
from bs4 import BeautifulSoup
import json

# Initialize the console for rich text rendering
console = Console()

# Function to parse HTML content and return a rendered output
def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")
    return str(soup)

# Function to display a specific span of cells from the "text" array
def render_text_span(json_data, cell_index, start_index, end_index, console):
    if "text" in json_data and isinstance(json_data["text"], list):
        try:
            # Fetch the specific outer list
            outer_cell = json_data["text"][cell_index]
                        
            if isinstance(outer_cell, list):
                        # Check if the range is within bounds
                if start_index < 0 or end_index >= len(outer_cell):
                    console.print(f"[bold red]Error:[/] Index out of bounds. Valid range for inner cells is 0 to {len(outer_cell) - 1}.")
                    return
                
                # Render the inner cells in the specified range
                for inner_index in range(start_index, end_index + 1):
                    cell_content = outer_cell[inner_index]
                    # Parse and render HTML content
                    parsed_content = parse_html(cell_content)
                    console.print(Panel(parsed_content, title=f"Genesis {cell_index + 1}:{inner_index + 1}", expand=False))
            else:
                console.print("[bold red]Error:[/] The selected outer cell is not a list.")
        except IndexError:
            console.print(f"[bold red]Error:[/] Index out of bounds. Cell index: {cell_index}, Start index: {start_index}, End index: {end_index}.")
    else:
        console.print("[bold red]Error:[/] No 'text' array found in JSON or it's not a list.")

# Main function
def main():
    # Specify Version
    file_path = "The Contemporary Torah, Jewish Publication Society, 2006.json"

    # Try to load the JSON file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_E = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not open or read the file: {e}")
        return  # Exit the script if the file cannot be loaded

    # Ask the user for the cell index and range of inner indices
    console.print("[bold magenta]Chapter[/]")
    cell_index = int(input("")) - 1  # Get the outer index from the user

    console.print("[bold magenta]Verses[/]")
    index_range = input("")  # Get the range as a string (e.g., "7-29")

    # Parse the index range into start_index and end_index
    try:
        # Ensure the input format is correct (two numbers separated by a hyphen)
        start_index, end_index = map(int, index_range.split('-'))
        start_index -= 1
        end_index -= 1
        
    except ValueError:
        console.print("[bold red]Error:[/] Invalid input format. Please enter two numbers separated by a hyphen (e.g., 7-29).")
        return  # Exit if the format is invalid

    # Check if the cell_index is within valid range for outer cells
    if cell_index < 0 or cell_index >= len(data_E["text"]):
        console.print(f"[bold red]Error:[/] Cell index {cell_index} is out of bounds. The valid range is 0 to {len(data['text']) - 1}.")
        return  # Exit if the cell index is invalid

    # Display the specified span of cells
    console.print(f"[bold magenta]Genesis {cell_index + 1}:{start_index + 1}-{end_index + 1}[/]")
    render_text_span(data_E, cell_index, start_index, end_index, console)

# Run the main function
if __name__ == "__main__":
    main()
