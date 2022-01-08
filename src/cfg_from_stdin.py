from antlr4 import CommonTokenStream, StdinStream, FileStream

from src.antlr.gen.CPP14_v2Lexer import CPP14_v2Lexer
from src.antlr.gen.CPP14_v2Parser import CPP14_v2Parser
from src.cfg_extractor.cfg_extractor_visitor import CFGExtractorVisitor
from src.code_coverage.prime_path_coverage import prime_path_coverage_bruteforce, prime_path_coverage_superset
from src.code_coverage.path_finder import prime_paths, simple_paths
from src.graph.utils import last_node, head_node
from src.graph.visual import draw_CFG


def prompt():
    is_read_file = input("Read from file/stream (f/s)? ").startswith(("f", "F"))
    is_verbose = input("Verbose graph draw (y/n)? ").startswith(("y", "Y"))
    file_path = None
    if is_read_file:
        default_path = "../test_source/c.cpp"
        file_path = input("Enter file path: ")
        file_path = file_path if file_path else default_path

    return is_read_file, is_verbose, file_path


def extract(stream):
    lexer = CPP14_v2Lexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = CPP14_v2Parser(token_stream)
    parse_tree = parser.translationunit()
    cfg_extractor = CFGExtractorVisitor()
    cfg_extractor.visit(parse_tree)
    funcs = cfg_extractor.functions
    return funcs, token_stream


def print_coverage_paths(g):
    def stringify_paths(paths):
        delimiter = "\n\t"
        s = delimiter.join([" -> ".join(str(node + 1) for node in path[:-1]) for path in paths])
        return delimiter + s

    def stringify_paths_organized(paths):
        delimiter = "\n\t"
        ps = {}

        for path in paths:
            s = " -> ".join(str(node + 1) for node in path[:-1])
            if path[0] in ps.keys():
                ps[path[0]] += [s]
            else:
                ps[path[0]] = [s]

        s = delimiter.join(", ".join(paths) for paths in ps.values())
        return delimiter + s

    paths = simple_paths(g)
    print(f"simple paths:{stringify_paths_organized(paths)}")

    paths = prime_paths(g, head_node(g), head_node(g))
    print(f"prime paths:{stringify_paths_organized(paths)}")

    paths, _ = prime_path_coverage_bruteforce(g, head_node(g), last_node(g))
    print(f"bruteforce prime-paths coverage:{stringify_paths(paths)}")

    paths, _ = prime_path_coverage_superset(g, head_node(g), last_node(g))
    print(f"superset prime-paths coverage:{stringify_paths(paths)}")


def main():
    is_read_file, is_verbose, file_path = prompt()
    stream = (FileStream(file_path, encoding="utf8") if is_read_file else StdinStream())
    funcs, token_stream = extract(stream)
    for i, g in enumerate(funcs.values()):
        print_coverage_paths(g)
        draw_CFG(g, f"../test_output/temp{i}", token_stream, verbose=is_verbose)


if __name__ == '__main__':
    main()
