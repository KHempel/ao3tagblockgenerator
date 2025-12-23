from typing import List, Optional
import argparse
from urllib.parse import quote

def create_css_block(tags: List[str]) -> str:
    """Create a CSS block for the given tags.

    Args:
        tags: A list of tag strings.
    Returns:
        A string representing the CSS block.
        `.blurb:has(a[href$="/tags/<tag>/works"]),`
        and so on for each tag.
        should be combined into a single CSS rule that sets
        `display: none;` for matching elements.
    """
    if not tags:
        return ""
    selectors = [f'.blurb:has(a[href$="/tags/{tag}/works"])' for tag in tags]
    selector_block = ",\n".join(selectors)
    return f"{selector_block} {{\n    display: none;\n}}"

def parse_tags(csv: Optional[str]) -> List[str]:
    """Parse a comma-separated list of strings into a cleaned list.

    - Splits on commas
    - Strips whitespace from each item
    - Ignores empty items
    - Percent-encodes each tag (UTF-8) so non-ASCII and reserved
      characters are safely represented for URLs/ CSS selectors.
    - Percent-encoding exceptions:
        - '/' characters are changed to '*s*'.
        - '&' characters are changed to '*a*'.
        - '.' characters are changed to '*d*'.
        - '?' characters are changed to '*q*'.
        - '#' characters are changed to '*h*'.
        - Open and close parentheses are left as-is.
        - Colons are left as-is.
        - '@' characters are left as-is.

    Args:
        csv: A comma-separated string, or None

    Returns:
        A list of non-empty, stripped, percent-encoded or otherwise modified tag strings.
    """
    if csv is None:
        return []

    taglist = [t.strip() for t in csv.split(",") if t.strip()]
    for i in range(len(taglist)):
        taglist[i] = quote(taglist[i], encoding="utf-8", safe="")
        taglist[i] = (
            taglist[i]
                .replace("%2F", "*s*")
                .replace("%26", "*a*")
                .replace("%2E", "*d*")
                .replace("%3F", "*q*")
                .replace("%23", "*h*")
                .replace(".", "*d*")
                .replace("%28", "(")
                .replace("%29", ")")
                .replace("%3A", ":")
                .replace("%40", "@")
        )

    return taglist


def main() -> None:
    parser = argparse.ArgumentParser(prog="ao3tagblockgenerator")
    parser.add_argument(
        "tags",
        nargs="?",
        help="Comma-separated list of tags (or use --tags)",
        default=None,
    )
    parser.add_argument("--tags", dest="tags_opt", help="Comma-separated list of tags")
    args = parser.parse_args()

    csv_input = args.tags_opt if args.tags_opt is not None else args.tags
    tags = parse_tags(csv_input)
    if not tags:
        print("No tags provided. Exiting.")
        return

    css_output = create_css_block(tags)
    print(css_output)


if __name__ == "__main__":
    main()
