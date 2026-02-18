https://tdj28.github.io/

20240802.2116

## Getting Started

To run the blog locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tdj28/blog.git
    cd blog
    ```

2.  **Initialize submodules:**
    ```bash
    git submodule update --init --recursive
    ```

3.  **Install dependencies:**
    ```bash
    npm install
    ```

4.  **Run the server:**
    ```bash
    hugo server -D
    ```

## Alert Shortcodes

Custom `alert` shortcode with `title` and `color` parameters. Use `{{</* alert */>}}` syntax (angle brackets, not percent signs).

```markdown
{{</* alert title="My Title" color="primary" */>}}
Alert content here (supports **Markdown**).
{{</* /alert */>}}
```

### Available Types

| Color | Icon | Background | Use For |
|-------|------|------------|---------|
| `primary` | ℹ️ circle-info | Blue (theme primary) | Notes, remarks, general info |
| `info` / `note` | ℹ️ circle-info | Blue (theme primary) | Same as primary |
| `secondary` | 💡 lightbulb | Cyan (theme secondary) | Definitions, examples, tips |
| `success` | ✓ check | Green | Confirmed results, summaries |
| `warning` | ⚠️ triangle-exclamation | Light pink | Cautions, caveats |
| `error` / `danger` | ☠️ skull-crossbones | Light red | Critical warnings |

Override the default icon with `icon="icon-name"`. Available icons are in `themes/blowfish/assets/icons/`.