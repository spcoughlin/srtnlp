def transform_pos_data(input_data):
    # Split the input data into lines
    lines = input_data.strip().split("\n")

    output_lines = []
    current_sentence = []

    for line in lines:
        # Remove any surrounding whitespace
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Handle sentences
        if line == "./.":
            if current_sentence:
                output_lines.extend(current_sentence)
                output_lines.append("BREAK BREAK")
                current_sentence = []
            continue

        # Handle tagged phrases and words
        if line.startswith("[") and line.endswith("]"):
            # Remove square brackets and split into tokens
            tokens = line[1:-1].split()
            for token in tokens:
                word, tag = token.rsplit("/", 1)
                current_sentence.append(f"{word} {tag}")
        elif line.startswith(",") or line.startswith("."):
            # Ignore standalone punctuation lines
            continue
        else:
            if "/" in line:
                tags = line.split()
                for tag in tags:
                    if "." in tag:
                        continue
                    word, tag = tag.rsplit("/", 1)
                    current_sentence.append(f"{word} {tag}")
            else:
                word, tag = line.rsplit("/", 1)
                current_sentence.append(f"{word} {tag}")

    # Add any remaining sentence
    if current_sentence:
        output_lines.extend(current_sentence)
        output_lines.append("BREAK BREAK")

    return "\n".join(output_lines)

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    return parser.parse_args()

def main(args):
    with open(args.input_file, "r") as f:
        input_data = f.read()

    output_data = transform_pos_data(input_data)

    with open(args.output_file, "w") as f:
        f.write(output_data)

if __name__ == "__main__":
    args = parse_args()
    main(args)


