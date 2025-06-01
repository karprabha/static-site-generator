# Static Site Generator

A lightweight, custom-built static site generator written in Python that converts Markdown content into a complete HTML website with modern styling and responsive design.

## Features

- **Markdown to HTML Conversion**: Converts Markdown files to clean, semantic HTML
- **Template-based Generation**: Uses a customizable HTML template system
- **Recursive Directory Processing**: Automatically processes nested content directories
- **Static Asset Management**: Copies and serves static files (CSS, images, etc.)
- **Built-in Development Server**: Includes a local development server for testing
- **Multiple Content Types**: Supports various Markdown elements including:
  - Headings (H1-H6)
  - Bold and italic text
  - Code blocks and inline code
  - Images and links
  - Ordered and unordered lists
  - Blockquotes
- **Responsive Design**: Mobile-friendly output with modern CSS
- **Custom Base Path Support**: Configurable base paths for deployment flexibility

## Project Structure

```
static-site-generator/
├── src/                    # Python source code
│   ├── main.py            # Main application entry point
│   ├── helper.py          # Markdown processing utilities
│   ├── htmlnode.py        # Base HTML node class
│   ├── parentnode.py      # Parent HTML nodes (containers)
│   ├── leafnode.py        # Leaf HTML nodes (content)
│   ├── blocknode.py       # Block-level HTML elements
│   ├── textnode.py        # Text processing nodes
│   └── test_*.py          # Unit tests
├── content/               # Markdown source content
│   ├── index.md          # Homepage content
│   ├── blog/             # Blog posts
│   └── contact/          # Contact pages
├── static/               # Static assets
│   ├── index.css         # Main stylesheet
│   └── images/           # Image assets
├── docs/                 # Generated HTML output
├── template.html         # HTML template for pages
├── main.sh              # Development server script
├── build.sh             # Production build script
└── test.sh              # Test runner script
```

## Installation

### Prerequisites

- Python 3.7 or higher
- zsh or bash shell

### Setup

1. Clone the repository:

```bash
git clone git@github.com:karprabha/static-site-generator.git
cd static-site-generator
```

2. No additional dependencies are required - the project uses only Python standard library modules.

## Usage

### Development Mode

To build the site and start a local development server:

```bash
./main.sh
```

This will:

- Generate the static site from your Markdown content
- Start a local server at `http://localhost:8888`
- Serve the generated site for local testing

### Production Build

To build the site for deployment with a custom base path:

```bash
./build.sh
```

Or with a custom base path:

```bash
python3 ./src/main.py "/your-custom-path/"
```

### Running Tests

To run the test suite:

```bash
./test.sh
```

This executes all unit tests using Python's built-in unittest framework.

### Adding Content

1. **Create Markdown files** in the `content/` directory
2. **Use standard Markdown syntax** for formatting
3. **Add images** to `static/images/` and reference them in Markdown
4. **Update CSS** in `static/index.css` for styling changes

#### Example Markdown Content

````markdown
# Page Title

This is a paragraph with **bold text** and _italic text_.

![Alt text](/images/example.png)

[Link text](/other-page)

## Code Example

```python
def hello_world():
    print("Hello, World!")
```
````

- List item 1
- List item 2

> This is a blockquote

```

## Template Customization

The `template.html` file defines the structure of generated pages:

- `{{ Title }}` - Replaced with the page title (first H1 heading)
- `{{ Content }}` - Replaced with the converted HTML content

You can modify this template to change the overall page structure, add meta tags, or include additional stylesheets.

## How It Works

1. **Content Processing**: The generator recursively scans the `content/` directory for `.md` files
2. **Markdown Parsing**: Each Markdown file is parsed into an AST (Abstract Syntax Tree)
3. **HTML Generation**: The AST is converted to semantic HTML using custom node classes
4. **Template Application**: The HTML content is injected into the template
5. **Asset Copying**: Static files are copied to the output directory
6. **Path Resolution**: Internal links are adjusted for the target deployment path

## Architecture

The codebase follows a modular design with clear separation of concerns:

- **Node System**: HTML generation uses a tree structure with `ParentNode` and `LeafNode` classes
- **Text Processing**: `TextNode` handles inline formatting (bold, italic, code, links, images)
- **Block Processing**: Different Markdown block types are handled by specific functions
- **Recursive Generation**: The system processes nested directory structures automatically

## Development

### Adding New Markdown Features

1. Extend the parsing logic in `helper.py`
2. Add corresponding HTML node types if needed
3. Update the test suite with new test cases
4. Test thoroughly with `./test.sh`

### Extending the Template System

The template system currently supports simple variable replacement. You can extend it by:

1. Adding new placeholder variables in `main.py`
2. Implementing more complex template logic
3. Supporting conditional content or loops

## Testing

The project includes comprehensive unit tests covering:

- HTML node generation and rendering
- Markdown parsing and conversion
- Text node processing and formatting
- Block-level element handling

Run tests frequently during development to ensure stability.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of a static site generator course from Boot.dev and is intended for educational purposes.

## Acknowledgments

- Built as part of the [Boot.dev](https://www.boot.dev) "Build a Static Site Generator" course
- Inspired by modern static site generators like Hugo and Jekyll
- Uses Python's standard library for maximum portability
```
