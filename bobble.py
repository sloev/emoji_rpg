# https://github.com/sindresorhus/cli-spinners/blob/master/spinners.json
# """div.small {
#   line-height: 0.7;
#   white-space: pre-wrap;
#   font-family: monospace;
# }"""

import textwrap


def bubble(text, max_width=30):
    wrapper = textwrap.TextWrapper(width=max_width)

    lines = wrapper.wrap(text=text)
    width = min(max_width, max([len(x) for x in lines]))
    data = ["⠴" + ("⠉" * width) + "⠦"]
    for line in lines:
        data.append("⠇" + line.ljust(width) + "⠸")
    data.append("⠲" + ("⠤" * width) + "⠋")
    data.append(" ⡏")
    return "\n".join(data)


print(bubble("lol her er en kattehistorie. Jeg fandt på den i bussen!"))
#     ⠲⠤⠤⠤⠤⠤⠤⠤⠤⠋
#  ⡏
# ⠴⠉⠉⠉⠉⠉⠉⠉⠉⠦
# ⠇    lol  ⠸
# ⠲⠤⠤⠤⠤⠤⠤⠤⠤⠋
#  ⡏

bubble = "\n".join(["◢■■■■■■◣", "▉■ lol ▉", "▉■■■■■■◤", "◤       "])

print(bubble)
