import re
from datetime import datetime
from tkinter import Tk, filedialog

def srt_to_textgrid(srt_content, srt_filename):
    # Function to convert SRT time format to seconds
    def srt_time_to_seconds(time_str):
        time_obj = datetime.strptime(time_str, "%H:%M:%S,%f")
        seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6
        return seconds

    # Split text by speakers and return a list of (speaker, text) tuples
    def split_speakers(text, last_speaker):
        parts = re.split(r'(\b[A-Z]{2,}:)', text)
        if parts and parts[0] == '':
            parts.pop(0)
        segments = []
        speaker = last_speaker
        for part in parts:
            if re.match(r'\b[A-Z]{2,}:', part):
                speaker = part
            else:
                if speaker:
                    segments.append((speaker.strip(), part.strip()))
                    speaker = None
                else:
                    segments.append((last_speaker.strip(), part.strip()))
        return segments

    # Parse the SRT content
    pattern = re.compile(r"(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n", re.DOTALL)
    matches = pattern.findall(srt_content)

    intervals = []
    last_end_time = 0.0
    last_speaker = "ML:"  # Default speaker if none is found

    for i, match in enumerate(matches):
        start_time = srt_time_to_seconds(match[1])
        end_time = srt_time_to_seconds(match[2])
        text = match[3].replace('\n', ' ').strip()

        # Ensure the first interval starts at 0
        if i == 0:
            start_time = 0.0

        # Ensure the end time of the previous interval matches the start time of the current one
        if intervals:
            intervals[-1] = (intervals[-1][0], start_time, intervals[-1][2])

        # Split the text by speakers
        segments = split_speakers(text, last_speaker)

        # If there are no segments, continue to the next interval
        if not segments:
            last_end_time = end_time
            continue

        # Calculate the duration of each segment
        total_duration = end_time - start_time
        segment_duration = total_duration / len(segments)

        # Create intervals for each segment
        for j, (speaker, segment_text) in enumerate(segments):
            segment_start_time = start_time + j * segment_duration
            segment_end_time = segment_start_time + segment_duration
            speaker = re.sub(r'\bFOMATPLAY:', 'ML:', speaker)
            speaker = re.sub(r'\b([A-Z]{2,}):', lambda m: m.group(1)[0] + ":", speaker)
            if segment_text:  # Only add interval if there's actual speech content
                intervals.append((segment_start_time, segment_end_time, f"{speaker} {segment_text}".strip()))
        
        last_end_time = end_time
        last_speaker = segments[-1][0] if segments else last_speaker

    # Prepare the TextGrid content
    textgrid_content = (
        'File type = "ooTextFile"\n'
        'Object class = "TextGrid"\n\n'
        f'xmin = 0\n'
        f'xmax = {intervals[-1][1]:.15f}\n'
        'tiers? <exists>\n'
        'size = 2\n'
        'item []:\n'
        '    item [1]:\n'
        '        class = "IntervalTier"\n'
        f'        name = "{srt_filename}"\n'
        f'        xmin = 0\n'
        f'        xmax = {intervals[-1][1]:.15f}\n'
        f'        intervals: size = {len(intervals)}\n'
    )

    for i, (xmin, xmax, text) in enumerate(intervals, start=1):
        textgrid_content += (
            f'        intervals [{i}]:\n'
            f'            xmin = {xmin:.15f}\n'
            f'            xmax = {xmax:.15f}\n'
            f'            text = "{text}"\n'
        )

    textgrid_content += (
        '    item [2]:\n'
        '        class = "IntervalTier"\n'
        '        name = "1"\n'
        f'        xmin = 0\n'
        f'        xmax = {intervals[-1][1]:.15f}\n'
        '        intervals: size = 1\n'
        '        intervals [1]:\n'
        f'            xmin = 0\n'
        f'            xmax = {intervals[-1][1]:.15f}\n'
        '            text = ""\n'
    )

    return textgrid_content

def main():
    # Open file dialog to select multiple .srt files
    Tk().withdraw()  # Hide the root window
    srt_file_paths = filedialog.askopenfilenames(title="Select SRT files", filetypes=[("SRT files", "*.srt")])

    if not srt_file_paths:
        print("No files selected.")
        return

    for srt_file_path in srt_file_paths:
        srt_filename = srt_file_path.rsplit('/', 1)[-1].rsplit('.', 1)[0]

        with open(srt_file_path, 'r', encoding='utf-8') as file:
            srt_content = file.read()

        textgrid_content = srt_to_textgrid(srt_content, srt_filename)

        # Save the TextGrid file
        textgrid_file_path = srt_file_path.rsplit('.', 1)[0] + '.TextGrid'
        with open(textgrid_file_path, 'w', encoding='utf-8') as file:
            file.write(textgrid_content)

        print(f"TextGrid file saved as {textgrid_file_path}")

if __name__ == "__main__":
    main()
