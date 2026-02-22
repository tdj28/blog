import re

with open("content/en/blog/post/math_science/datasci/vector-search-math/index.md", "r") as f:
    text = f.read()

# 1. Remove all <a id="cite-..."></a> tags from the text
text = re.sub(r'<a id="cite-[^"]+"></a>', '', text)

# 2. Remove all [↩](#cite-...) backlinks from the references list
text = re.sub(r'\s*\[↩\]\(#cite-[^)]+\)', '', text)

with open("content/en/blog/post/math_science/datasci/vector-search-math/index.md", "w") as f:
    f.write(text)

print("Policy A applied.")
