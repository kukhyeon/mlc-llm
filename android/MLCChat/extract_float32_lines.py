import argparse
from pathlib import Path


def extract_float32_lines(input_path: Path, output_path: Path) -> int:
    matches = []
    with input_path.open("r", encoding="utf-8") as src:
        for line_no, line in enumerate(src, start=1):
            if "float32" in line:
                matches.append(f"{line_no}: {line.rstrip()}\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as dst:
        dst.writelines(matches)

    return len(matches)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Save all lines containing "float32" from a Python script to a text file.'
    )
    parser.add_argument("input_file", type=Path, help="Path to the source .py file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .txt path. Defaults to <input_stem>_float32_lines.txt next to input file.",
    )
    args = parser.parse_args()

    input_path = args.input_file.resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")
    if input_path.suffix.lower() != ".py":
        raise ValueError(f"Expected a .py file, got: {input_path}")

    output_path = args.output
    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}_float32_lines.txt")
    else:
        output_path = output_path.resolve()

    count = extract_float32_lines(input_path, output_path)
    print(f"Saved {count} matching lines to: {output_path}")


if __name__ == "__main__":
    main()
