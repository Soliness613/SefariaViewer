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

# Function to handle user input
def parse_reference(input_str):
    pattern = r'^(?P<book>[A-Za-z]+(?: [A-Za-z]+)*) (\d+):(\d+)(?:-(\d+)(?::(\d+))?)?$'
    match = re.match(pattern, input_str.strip())

    if match:
        book = match.group('book')
        start_chapter = int(match.group(2))
        start_verse = int(match.group(3))

        if match.group(4):
            if match.group(5):
                end_chapter = int(match.group(4))
                end_verse = int(match.group(5))
            else:
                end_chapter = start_chapter
                end_verse = int(match.group(4))
            return {"book": book, "start_chapter": start_chapter, "start_verse": start_verse, "end_chapter": end_chapter, "end_verse": end_verse}
        else:
            return {"book": book, "start_chapter": start_chapter, "start_verse": start_verse}
    else:
        raise ValueError("Please use correct format i.e., 'Genesis 32:4', 'Genesis 32:4-13', or 'Genesis 32:4-36:43'.")

# Function to render text spans
def render_text_span(json_data_english, json_data_hebrew, reference, colors, console):
    if "text" in json_data_english and isinstance(json_data_english["text"], list):
        try:
            outer_cell_E = json_data_english["text"]
            outer_cell_H = json_data_hebrew["text"]

            start_chapter = reference["start_chapter"] - 1
            start_verse = reference["start_verse"] - 1
            end_chapter = reference.get("end_chapter", reference["start_chapter"]) - 1
            end_verse = reference.get("end_verse", reference["start_verse"]) - 1

            for chapter_index in range(start_chapter, end_chapter + 1):
                chapter_E = outer_cell_E[chapter_index]
                chapter_H = outer_cell_H[chapter_index]

                start_verse_index = start_verse if chapter_index == start_chapter else 0
                end_verse_index = end_verse if chapter_index == end_chapter else len(chapter_E) - 1

                for verse_index in range(start_verse_index, end_verse_index + 1):
                    cell_content_E = chapter_E[verse_index]
                    cell_content_H = chapter_H[verse_index]

                    parsed_content_E = parse_html(cell_content_E)
                    parsed_content_E = re.sub(r'<br\s*/?>', '\n', parsed_content_E)
                    parsed_content_E = re.sub(r'<sup class="footnote-marker">.*?</sup><i class="footnote">.*?</i>', '', parsed_content_E)
                    parsed_content_E = re.sub(r'<.*?>', '', parsed_content_E)
                    parsed_content_E = f"[{colors['english']}]" + parsed_content_E + "[/]"

                    parsed_content_H = parse_html(cell_content_H)
                    parsed_content_H = f"[{colors['hebrew']}]" + parsed_content_H + "[/]"

                    combined_content = f"{parsed_content_E}\n\n{parsed_content_H}"
                    title_color = colors['title']
                    border_color = colors['border']

                    console.print(Panel(combined_content, title=f"[{title_color}]{reference['book']} {chapter_index + 1}:{verse_index + 1}", border_style=f"{border_color}", expand=False))
        except IndexError:
            console.print("[bold red]Error:[/] Index out of bounds when processing the reference.")
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")
    else:
        console.print("[bold red]Error:[/] Invalid text data in JSON.")

# Main function
def main():
    user_input = input("Enter reference (e.g., Genesis 32:4, Genesis 32:4-13, Genesis 32:4-36:43): ")

    try:
        reference = parse_reference(user_input)
    except ValueError as e:
        console.print(f"[bold red]Error:[/] {e}")
        return

    english_file_path = f"{reference['book']}/The Contemporary Torah, Jewish Publication Society, 2006.json"
    hebrew_file_path = f"{reference['book']}/Tanach with Text Only.json"

    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        colors = config["colors"]
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not load config: {e}")
        return

    try:
        with open(english_file_path, 'r', encoding='utf-8') as f:
            data_E = json.load(f)
        with open(hebrew_file_path, 'r', encoding='utf-8') as f:
            data_H = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Error:[/] Could not load JSON data: {e}")
        return

    render_text_span(data_E, data_H, reference, colors, console)

if __name__ == "__main__":
    main()
