# SRT to TextGrid Converter

## Overview

This project converts SRT subtitle files into Praat TextGrid files. It allows users to select multiple SRT files, processes them one by one, and generates corresponding TextGrid files with intervals and speaker names accurately maintained.

## How It Works

The script reads the contents of SRT files, processes the subtitle text and timing, and creates corresponding TextGrid files with linked intervals. The resulting TextGrid files can be used for speech analysis in Praat.

## Features

- Select multiple SRT files for processing.
- Converts each SRT file into a corresponding TextGrid file.
- Maintains speaker names and links intervals together seamlessly.
- Ensures the first interval starts at 0 and adjusts interval timings accordingly.
- Splits intervals into equal parts if multiple speakers are detected within a single interval.

## Steps the Script Takes

1. **File Selection**: Uses `tkinter` to open a file dialog allowing users to select multiple SRT files.
2. **Reading SRT Content**: Reads the contents of each selected SRT file.
3. **Parsing SRT**: Extracts timing and text information from the SRT file.
4. **Processing Text**:
   - Splits text by speaker identifiers.
   - Ensures accurate linking of intervals.
   - Maintains speaker names, converting "FOMATPLAY:" to "ML:" and abbreviating other names.
5. **Creating TextGrid**:
   - Generates intervals with accurate timing.
   - Ensures each interval's end time matches the start time of the next.
6. **Saving TextGrid**: Saves the generated TextGrid file in the same directory as the original SRT file with a `.TextGrid` extension.

## File Selection System

The file selection system uses `tkinter`'s `filedialog.askopenfilenames` to allow users to select multiple SRT files at once. This method returns a tuple containing the paths to all selected files. The script then processes each file individually, converting it to a TextGrid file and saving it in the same directory.

## Linking Intervals Together

The script ensures that the end time of each interval matches the start time of the next interval. If multiple speakers are detected within a single interval, it splits the interval into equal parts, each assigned to the respective speaker.

## Maintaining Speaker Names

The script maintains speaker names by:
- Replacing "FOMATPLAY:" with "ML:".
- Abbreviating other speaker names to their first letter followed by a colon (e.g., "RICARDO:" becomes "R:").
- Ensuring that if an interval starts without a speaker identifier, it uses the previous speaker's name.

## How the Executable Works

The executable, created using `PyInstaller`, runs the Python script as a standalone application. When executed, it opens a file dialog for selecting multiple SRT files, processes each selected file, and saves the resulting TextGrid files in the same directory.

## Usage

1. **Running the Executable**:
   - Double-click the executable file (e.g., `srt_to_textgrid.exe`).
   - A file dialog will open, allowing you to select multiple SRT files.
   - After selecting the files, the script processes each file and saves the corresponding TextGrid files in the same directory.

2. **Python Script**:
   - Ensure you have the required dependencies (`tkinter` and `re`).
   - Run the script using Python 3.x:
     ```sh
     python srt_to_textgrid.py
     ```
   - A file dialog will open, allowing you to select multiple SRT files.
   - The script will process each file and save the corresponding TextGrid files in the same directory.

## MIT License

```
MIT License

Made by Kim Garrick

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgements

This project was created by Kim Garrick. Special thanks to the open-source community for providing tools like `PyInstaller` and `tkinter` that made this project possible.
