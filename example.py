import argparse
from argparse import ArgumentParser

from cli import CLI

parser = argparse.ArgumentParser(
    prog="String Parser",
    description="Parses strings using simple but essential operations.",
)

cli = CLI(parser)

def get_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

@cli.register("strip")
def strip_comments(content: str) -> str:
    lines = [line for line in content.split("\n") if not line.startswith("#")]
    return "\n".join(lines)

@cli.register("remove_blanks")
def remove_blanks(content: str) -> str:
    lines = [line for line in content.split("\n") if line.strip() != ""]
    return "\n".join(lines)

@cli.register("upper")
def uppercase(content: str) -> str:
    return content.upper()

# initialize cli flags
@cli.init
def cli_init(p: ArgumentParser) -> None:
    p.add_argument("file", help="file path")
    p.add_argument("-o", nargs="*", help=f"parse options: {list(cli.registry.keys())}")

def main() -> None:
    args = cli.parser.parse_args()

    content = get_file(args.file)
    pipeline = cli.pipeline(*args.o)

    print(pipeline(content))

if __name__ == "__main__":
    main()