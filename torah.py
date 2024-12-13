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
def render_text_span(json_data_english, json_data_hebrew, book, cell_index, start_index, end_index, console):
    if "text" in json_data_english and isinstance(json_data_english["text"], list):
        try:
            # Fetch the specific outer list
            outer_cell_E = json_data_english["text"][cell_index]              
            outer_cell_H = json_data_hebrew["text"][cell_index]
            if isinstance(outer_cell_E, list):
                        # Check if the range is within bounds
                if start_index < 0 or end_index >= len(outer_cell_E):
                    console.print(f"[bold red]Error:[/] Valid range for verses in {book} {cell_index + 1} is 1 to {len(outer_cell_E)}.")
                    return
                
                # Render the inner cells in the specified range
                for inner_index in range(start_index, end_index + 1):
                    cell_content_E = outer_cell_E[inner_index]
                    cell_content_H = outer_cell_H[inner_index]
                    cell_content_H = cell_content_H.split()
                    cell_content_H = cell_content_H[::-1]
                    cell_content_H = ' '.join(cell_content_H)

                    # Parse and render HTML content
                    parsed_content_E = parse_html(cell_content_E)
                    parsed_content_E = re.sub(r'<br\s*/?>', '\n', parsed_content_E)
                    parsed_content_E = re.sub(r'<.*>', '', parsed_content_E) 
                    parsed_content_E = f"[bold blue]{parsed_content_E}[/]"

                    # parsed_content_E = re.sub(r'יהוה','[bold yellow]יהוה[/]', parsed_content_E)
                    parsed_content_H = parse_html(cell_content_H)
                    parsed_content_H = f"[bold green]{parsed_content_H}[/]"

                    # Combine parsed content with a line break as a plain string
                    parsed_content_combined = f"{parsed_content_E}\n\n{parsed_content_H}"

                    console.print(Panel(parsed_content_combined, title=f"[bold yellow]{book} {cell_index + 1}:{inner_index + 1}[/]", expand=False))
                    
            else:
                console.print("[bold red]Error:[/] The selected outer cell is not a list.")
        except IndexError:
            console.print(f"[bold red]Error:[/] Index out of bounds. {book} {cell_index + 1} has {len(outer_cell_E)} verses.")
    else:
        console.print("[bold red]Error:[/] No 'text' array found in JSON or it's not a list.")

# Main function
def main():
    # Ask which book
    console.print("[bold magenta]Book:")
    book = str(input(""))
    # Specify Versions
    english_file_path = f"{book}/The Contemporary Torah, Jewish Publication Society, 2006.json"
    hebrew_file_path = f"{book}/Tanach with Text Only.json"

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
    console.print("[bold magenta]Chapter:[/]")
    cell_index = int(input("")) - 1  # Get the outer index from the user

    console.print("[bold magenta]Verse(s):[/]")
    index_range = input("")  # Get the range as a string (e.g., "7-29")

    # Parse the index range into start_index and end_index
    try:
        # Ensure the input format is correct (two numbers separated by a hyphen)
        start_index, end_index = map(int, index_range.split('-'))
        start_index -= 1
        end_index -= 1
        
    except ValueError:
        start_index = int(index_range) - 1
        end_index = int(index_range) - 1
    #    console.print("[bold red]Error:[/] Invalid input format. Please enter two numbers separated by a hyphen (e.g., 7-29).")
#        return  # Exit if the format is invalid
    # Check if the cell_index is within valid range for outer cells
    if cell_index < 0 or cell_index >= len(data_E["text"]) or cell_index >=len(data_H["text"]):
        console.print(f"[bold red]Error:[/] Chapter {cell_index} is out of bounds. The valid range is 1 to {len(data['text'])}.")
        return  # Exit if the cell index is invalid

    # Display the specified span of cells
    if start_index == end_index:
        console.print(f"[bold magenta]{book} {cell_index + 1}:{start_index + 1}[/]")
    else:
        console.print(f"[bold magenta]{book} {cell_index + 1}:{start_index + 1}-{end_index + 1}[/]")
    render_text_span(data_E, data_H, book, cell_index, start_index, end_index, console)
# Run the main function
if __name__ == "__main__":
    main()
