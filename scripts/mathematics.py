"""Replace legacy MathJax bootstraps with one pinned local loader."""
import re


def reflow_formula(match):
    """Break top-level TeX spacers; leave matrices, cases and arguments intact."""
    formula = match[2].strip()
    aligned = formula.startswith(r"\begin{aligned}") and formula.endswith(r"\end{aligned}")
    if aligned:
        formula = formula[len(r"\begin{aligned}"):-len(r"\end{aligned}")].strip()
    depth, brackets, environments, cuts = 0, 0, [], []
    row_start = 0
    changed = False
    i = 0
    while i < len(formula):
        token = re.match(r"\\(begin|end)\{([^}]+)\}", formula[i:])
        if token:
            if token[1] == "begin":
                environments.append(token[2])
            elif environments and environments[-1] == token[2]:
                environments.pop()
            i += len(token[0])
            continue
        char = formula[i]
        escaped = i > 0 and formula[i - 1] == "\\"
        if char == "{" and not escaped:
            depth += 1
        elif char == "}" and not escaped:
            depth -= 1
        elif char in "([" and not escaped:
            brackets += 1
        elif char in ")]" and not escaped:
            brackets = max(0, brackets - 1)
        if not depth and not brackets and not environments:
            if formula.startswith(r"\\", i):
                cuts.append((i, i + 2))
                i += 2
                row_start = i
                continue
            spacer = re.match(r"\\q(?:quad|uad)\b\s*", formula[i:])
            if spacer:
                # A spacer at the start of an aligned continuation is indentation.
                if formula[row_start:i].replace("&", "").strip():
                    cuts.append((i, i + len(spacer[0])))
                    changed = True
                    row_start = i + len(spacer[0])
                i += len(spacer[0])
                continue
        i += 1
    if not changed:
        return match[0]
    # Each new row shares one alignment column; existing aligned rows retain theirs.
    rows, start = [], 0
    for cut, end in cuts:
        rows.append(formula[start:cut])
        start = end
    rows.append(formula[start:])
    rows = [row.strip() for row in rows if row.strip()]
    rows = [row if "&" in row else "&" + row for row in rows]
    return match[1] + r"\begin{aligned}" + "\n" + ("\\\\\n".join(rows)) + "\n" + r"\end{aligned}" + match[3]


def decorate_math(ctx, entry, text):
    if entry.get("reading_revision") == "learning-20261115" or entry.get("reading_mode") == "longform":
        text = re.sub(r'(<div\b[^>]*class="reading-math"[^>]*>\s*\\\[)(.*?)(\\\]\s*</div>)',
                      reflow_formula, text, flags=re.S)
    def script(match):
        value = match[0]
        if re.search(r"MathJax|mathjax@|MathJax\.js|katex(?:\.min)?\.js", value, re.I):
            identifier = re.search(r'\bid=["\']([^"\']+)["\']', value.split(">", 1)[0])
            return (f'<script type="application/json" id="{identifier[1]}">{{}}</script>'
                    if identifier else "")
        return value
    text = re.sub(r"<script\b[^>]*>.*?</script>", script, text, flags=re.S | re.I)
    text = re.sub(r'<div\b[^>]*id=["\']math-loading["\'][^>]*>\s*'
                  r'<div\b[^>]*class=["\']spinner["\'][^>]*>\s*</div>[^<]*</div>',
                  '<span id="math-loading" class="reading-anchor"></span>', text, flags=re.S)
    # Older prerequisite pages use a one-line loading label.
    text = re.sub(r'<div\b[^>]*class=["\']math-loading["\'][^>]*>.*?</div>', "", text, flags=re.S)
    path = entry["url"]
    root = ctx.rel(path, "/assets/site/vendor/mathjax/")
    # rel(directory) resolves index.html; the loader needs the directory itself.
    root = root.removesuffix("index.html")
    tags = (f'<script defer src="{ctx.asset(path, "/assets/site/math-config.js")}" '
            f'data-mathjax-root="{root}"></script>'
            f'<script defer src="{ctx.asset(path, "/assets/site/math.js")}"></script>')
    return text.replace("</head>", tags + "</head>", 1)
