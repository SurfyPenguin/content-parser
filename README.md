# Content Parser

## A CLI interface to make your string parsing functions accessible through command line conveniently.

## Setup
1. Import `cli.CLI` class and `argparse`
```python
import argparse
from argparse import ArgumentParser

from cli import CLI
```

2. Initialize your parser instance `parser.ArgumentParser` and setup `program name` and `description`.
```python
# from example.py
parser = argparse.ArgumentParser(
    prog="String Parser",
    description="Parses strings using simple but essential operations.",
)

cli = CLI(parser)
```
3. Add flags

Use either `CLI.parser.add_argument` or `CLI.init` to setup flags.

```python
cli.parser.add_argument("file", help="file path")
cli.parser.add_argument("-o", nargs="*", help=f"parse options: {list(cli.registry.keys())}")
```
Alternatively,
Here is an example from `example.py`
```python
@cli.init
def cli_init(p: ArgumentParser) -> None:
    p.add_argument("file", help="file path")
    p.add_argument("-o", nargs="*", help=f"parse options: {list(cli.registry.keys())}")
```
Here we have used `@cli.init` decorator which adds argument using parser instance stored in `CLI` instance.

## Creating custom parsing functions
Once the setup part is complete, we can add any parsing function following the signature: `(function) def parse_func(content: str) -> str: ...`

After implementing custom parsing logic, decorate it with `@CLI.register` decorator.

```python
# example.py

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
```

Finally, your own logic to handle flags
```python
def main() -> None:
    args = cli.parser.parse_args()

    content = get_file(args.file)
    pipeline = cli.pipeline(*args.o)

    print(pipeline(content))

if __name__ == "__main__":
    main()
```

## Pipeline
Once our functions are done, we can build pipelines which apply on texts or strings sequentially.

Here's how to use it.

```python
# custom function
@cli.register("strip_lines")
def strip_lines(content: str) -> str:
    return "\n".join([line.strip() for line in content.split("\n")])

@cli.register("excited")
def quote(content: str) -> str:
    return content.upper() + "!!!"

content = "   Guess who's back "

pipeline = cli.pipeline("strip_lines", "upper", "excited") # this returns a closure

# call the closure
pipeline(content) # outputs: GUESS WHO'S BACK!!!
```

## Usage
`example.py`
```sh
$ python example.py -h
usage: String Parser [-h] [-o [O ...]] file

Parses strings using simple but essential operations.

positional arguments:
  file        file path

options:
  -h, --help  show this help message and exit
  -o [O ...]  parse options: ['strip', 'remove_blanks', 'upper']
```

## Create executable script
Put this shebang at the top of your script `#!/usr/bin/env python3`
and make your script executable using this command.

```sh
$ chmod +x example # renamed example.py -> example
```
Execution:
```sh
$ ./example -h
usage: String Parser [-h] [-o [O ...]] file

Parses strings using simple but essential operations.

positional arguments:
  file        file path

options:
  -h, --help  show this help message and exit
  -o [O ...]  parse options: ['strip', 'remove_blanks', 'upper']
```

---
This project is a simple implementation of [strategy pattern](https://en.wikipedia.org/wiki/Strategy_pattern).