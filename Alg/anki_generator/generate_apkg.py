import os
import re
import json
import random
import markdown
import genanki
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

# CSS styling for a beautiful, premium card design (supports both Light and Dark mode)
CARD_CSS = """
.card {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #f8fafc;
  color: #0f172a;
  margin: 0;
  padding: 10px;
}
.card-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
  max-width: 800px;
  margin: 20px auto;
  padding: 30px;
  border: 1px solid #e2e8f0;
  text-align: left;
}
.header {
  font-size: 13px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  margin-bottom: 20px;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 8px;
}
.content {
  font-size: 16px;
  line-height: 1.6;
  color: #1e293b;
}
.answer {
  margin-top: 10px;
  color: #0f172a;
}
.divider {
  border: none;
  height: 1px;
  background-color: #e2e8f0;
  margin: 25px 0;
}
pre {
  background-color: #272822 !important; /* Monokai background */
  color: #f8f8f2 !important;
  border-radius: 6px;
  padding: 14px;
  overflow-x: auto;
  font-family: Consolas, Monaco, "Andale Mono", monospace;
  font-size: 14px;
  line-height: 1.5;
  margin: 15px 0;
}
code {
  font-family: Consolas, Monaco, "Andale Mono", monospace;
  font-size: 14px;
  background-color: #f1f5f9;
  color: #0f172a;
  padding: 2px 5px;
  border-radius: 4px;
}
pre code {
  background-color: transparent;
  padding: 0;
  color: inherit;
}
img {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 20px auto;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}
/* Anki MathJax */
.MathJax_Display, .MathJax {
  font-size: 105%;
}
"""

def render_markdown_with_math_and_code(text):
    if not text:
        return ""
    
    # 1. Extract code blocks
    code_blocks = []
    def code_repl(match):
        indent = match.group(1)
        lang = match.group(2).strip() if match.group(2) else "text"
        code_content = match.group(3)
        placeholder = f"{indent}CODEBLOCKPLACEHOLDER{len(code_blocks)}"
        code_blocks.append((lang, code_content))
        return placeholder
    
    # Regex to find fenced code blocks with optional leading indentation
    text = re.sub(r"^([ \t]*)```(\w*)\n(.*?)\n[ \t]*```", code_repl, text, flags=re.DOTALL | re.MULTILINE)
    
    # 2. Extract math blocks (block and inline)
    block_math = []
    inline_math = []
    
    def block_math_repl(match):
        math_content = match.group(1)
        placeholder = f"BLOCKMATHPLACEHOLDER{len(block_math)}"
        block_math.append(math_content)
        return placeholder
        
    def inline_math_repl(match):
        math_content = match.group(1)
        placeholder = f"INLINEMATHPLACEHOLDER{len(inline_math)}"
        inline_math.append(math_content)
        return placeholder
    
    # Parse block math
    text = re.sub(r"\$\$(.*?)\$\$", block_math_repl, text, flags=re.DOTALL)
    text = re.sub(r"\\\[(.*?)\\\]", block_math_repl, text, flags=re.DOTALL)
    
    # Parse inline math (avoid matching single $ when used for money, but standard is fine here)
    text = re.sub(r"\\\((.*?)\\\)", inline_math_repl, text, flags=re.DOTALL)
    # We also handle single $...$ if they exist, but avoid overlapping with placeholders
    text = re.sub(r"(?<!\\)\$(.*?)(?<!\\)\$", inline_math_repl, text)
    # 2.5 Fix markdown list formatting (ensuring there's a blank line before list items)
    lines = text.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_list_item = stripped.startswith('* ') or stripped.startswith('- ') or bool(re.match(r'^\d+\. ', stripped))
        if is_list_item and i > 0:
            prev_line = lines[i-1].strip()
            prev_is_list_item = prev_line.startswith('* ') or prev_line.startswith('- ') or bool(re.match(r'^\d+\. ', prev_line))
            if prev_line and not prev_is_list_item:
                new_lines.append("")
        new_lines.append(line)
    text = '\n'.join(new_lines)

    # 3. Convert markdown to HTML
    html = markdown.markdown(text, extensions=['tables', 'fenced_code'])
    
    # 4. Restore inline math as Anki MathJax \( ... \)
    for i in range(len(inline_math) - 1, -1, -1):
        html = html.replace(f"INLINEMATHPLACEHOLDER{i}", f"\\({inline_math[i]}\\)")
        
    # 5. Restore block math as Anki MathJax \[ ... \]
    for i in range(len(block_math) - 1, -1, -1):
        html = html.replace(f"BLOCKMATHPLACEHOLDER{i}", f"\\[{block_math[i]}\\]")
        
    # 6. Restore and highlight code blocks
    for i in range(len(code_blocks) - 1, -1, -1):
        lang, code_content = code_blocks[i]
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except Exception:
            lexer = TextLexer()
        
        # Use Monokai style for dark code block highlighting
        formatter = HtmlFormatter(noclasses=True, style='monokai')
        highlighted_code = highlight(code_content, lexer, formatter)
        html = html.replace(f"CODEBLOCKPLACEHOLDER{i}", highlighted_code)
        
    return html

def create_deck_from_json(json_dir, output_apkg_path):
    # Model definition
    model_id = 1847293847 # Fixed model ID
    my_model = genanki.Model(
        model_id,
        'Advanced Algorithms Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
            {'name': 'ExerciseNum'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<div class="card-container"><div class="header">Advanced Algorithms - {{ExerciseNum}}</div><div class="content">{{Question}}</div></div>',
                'afmt': '<div class="card-container"><div class="header">Advanced Algorithms - {{ExerciseNum}}</div><div class="content">{{Question}}</div><hr class="divider"><div class="content answer">{{Answer}}</div></div>',
            },
        ],
        css=CARD_CSS
    )
    
    deck_id = 2058374921 # Fixed deck ID
    my_deck = genanki.Deck(deck_id, 'Advanced Algorithms (Exercises)')
    
    cards_added = 0
    # Walk and read all json files in json_dir
    for file in sorted(os.listdir(json_dir)):
        if file.endswith(".json"):
            file_path = os.path.join(json_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                cards = json.load(f)
                
            for card in cards:
                q_html = render_markdown_with_math_and_code(card.get("question", ""))
                a_html = render_markdown_with_math_and_code(card.get("answer", ""))
                ex_num = card.get("sheet", "Exercise")
                
                note = genanki.Note(
                    model=my_model,
                    fields=[q_html, a_html, ex_num]
                )
                my_deck.add_note(note)
                cards_added += 1
                
    # Find all media files in the media directory if it exists
    media_files = []
    media_dir = os.path.join(os.path.dirname(output_apkg_path), "media")
    if os.path.exists(media_dir):
        for file in os.listdir(media_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                media_files.append(os.path.join(media_dir, file))

    # Save the deck package with media
    package = genanki.Package(my_deck)
    package.media_files = media_files
    package.write_to_file(output_apkg_path)
    print(f"Successfully generated Anki package: {output_apkg_path} with {cards_added} cards (including {len(media_files)} media files).")

if __name__ == "__main__":
    json_dir = r"C:\Users\lovek\Documents\EX\Alg\anki_generator\json_cards"
    output_apkg = r"C:\Users\lovek\Documents\EX\Alg\anki_generator\Advanced_Algorithms_Exercises.apkg"
    
    if os.path.exists(json_dir):
        create_deck_from_json(json_dir, output_apkg)
    else:
        print(f"Error: JSON directory {json_dir} does not exist.")
