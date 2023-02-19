import os

'''
Takes in seconds and outputs a proper timestamp.
Used for writing timestamps in the subtitles file.
'''
def format_timestamp(seconds: float, always_include_hours: bool = False):
    assert seconds >= 0, "Non-negative timestamp expected!"

    # Convert to milliseconds
    milliseconds = round(seconds * 1000.0)

    # Get hours from remaining milliseconds
    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    # Get minutes from remaining milliseconds
    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    # Get seconds from remaining milliseconds
    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    # Format
    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

'''
Retrieves the filename given a path.
Used for sanity.
'''
def filename(path):
    return os.path.splitext(os.path.basename(path))[0]