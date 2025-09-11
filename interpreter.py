from __future__ import annotations

import sys
from collections import defaultdict


class Brainfuck:
    """A Brainf*** interpreter."""

    def __init__(self, source: str):
        self.source = source
        self.jump_map = self._jump_map(source)

    @staticmethod
    def compile(source: str) -> Brainfuck:
        """Preprocess Brainf*** source code."""
        return Brainfuck(source)

    @staticmethod
    def execute(source: str) -> None:
        """Compile and run Brainf*** source code."""
        Brainfuck(source).run()

    def run(self) -> None:
        """Run the interpreter."""
        tape: defaultdict[int, int] = defaultdict(int)
        cell = 0
        instruction_pointer = 0

        while instruction_pointer < len(self.source):
            op = self.source[instruction_pointer]

            if op == ">":
                cell += 1
            elif op == "<":
                cell -= 1
            elif op == "+":
                tape[cell] += 1
            elif op == "-":
                tape[cell] -= 1
            elif op == ",":
                tape[cell] = ord(sys.stdin.read(1))
            elif op == ".":
                sys.stdout.write(chr(tape[cell]))
            elif (op == "[" and not tape[cell]) or (op == "]" and tape[cell]):
                instruction_pointer = self.jump_map[instruction_pointer]

            instruction_pointer += 1

    def _jump_map(self, source: str) -> dict[int, int]:
        """Precalculate loop start and end indexes."""
        indexes: dict[int, int] = {}
        stack: list[int] = []

        for i, op in enumerate(source):
            if op == "[":
                stack.append(i)
            if op == "]":
                if not stack:
                    source = source[:i]
                    break
                index = stack.pop()
                indexes[i], indexes[index] = index, i

        if stack:
            raise SyntaxError("unclosed loops at {}".format(stack))

        return indexes


if __name__ == "__main__":
    import argparse

    # Pass `-` on the command line to read from the standard input stream.
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))
    args = parser.parse_args()
    Brainfuck.execute(args.infile.read())
