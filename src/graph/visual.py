import html

import graphviz as gv

from src.antlr.rule_utils import extract_exact_text
from src.graph.utils import head_node, last_node

FONT_SIZE = "22"


def draw_CFG(graph, filename, token_stream, format="png"):
    gr = gv.Digraph(comment=filename, format=format, node_attr={"shape": "none"})
    gr.node("start", style="filled", fillcolor="#aaffaa", shape="oval", fontsize=FONT_SIZE)

    for node, args in list(graph.nodes.data())[:-1]:
        block_contents = stringify_block(token_stream, args)
        gr.node(str(node), label=build_node_template(node, block_contents))
    gr.node(str(last_node(graph)), label="end", style="filled", fillcolor="#ffaaaa", shape="oval", fontsize=FONT_SIZE)

    for f, t, args in graph.edges.data():
        gr.edge(f"{str(f)}", f"{str(t)}", label=args.get("state"), fontsize=FONT_SIZE)
    gr.edge("start", str(head_node(graph)))

    gr.render(f"{filename}.gv", view=True)


def build_node_template(node_label, node_contents):
    b = node_content_to_html(node_contents)
    b_len = len(node_contents)
    line_height = 40
    s = f"""<<FONT POINT-SIZE="{FONT_SIZE}">  
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
            <tr>
                <td width="30" height="30" fixedsize="true">{node_label + 1}</td>
                <td width="9" height="9" fixedsize="true" style="invis"></td>
                <td width="9" height="9" fixedsize="true" style="invis"></td>
            </tr>
            <tr>
                <td width="30" height="{b_len * line_height}" fixedsize="true" sides="tlb"></td>
                <td width="50" height="{b_len * line_height}" fixedsize="false" sides="bt" PORT="here">{b}</td>
                <td width="30" height="{b_len * line_height}" fixedsize="true" sides="brt"></td>
            </tr>
        </TABLE>
    </FONT>>"""
    return strip_lines(s)


def strip_lines(x: str): return "\n".join(line.strip() for line in x.splitlines())


def node_content_to_html(node_contents):
    delimiter = '<br align="left"/>\n'
    content_list_string = delimiter.join([html.escape(f"{l}: {content}") for l, content in node_contents])
    return content_list_string + delimiter


def stringify_block(token_stream, node_args):
    return [(rule.start.line, extract_exact_text(token_stream, rule)) for rule in node_args["data"]]
