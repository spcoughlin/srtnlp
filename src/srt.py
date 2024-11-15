# aggregate all text fields from srt file into a single string
def srt_text_to_string(srtfile):
    with open(srtfile, 'r') as f:
        lines = f.readlines()
    text = ""
    for line in lines:
        if line.strip().isnumeric():
            continue
        if "-->" in line.strip():
            continue
        if line.strip() == '':
            continue
        text += line.strip() + ' '
    return text

