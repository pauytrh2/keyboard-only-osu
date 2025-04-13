import os

def find_map(artist, song_name, difficulty, base_path="~/.local/share/osu/files"):
    """Find osu maps by artist, song name, and difficulty"""
    base_path = os.path.expanduser(base_path)
    matching_file = []

    for root, _, files in os.walk(base_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    if lines and lines[0].strip().lower() == "osu file format v14":
                        in_metadata = False
                        found_title = found_artist = found_version = False

                        for line in lines:
                            line = line.strip()
                            if line == "[Metadata]":
                                in_metadata = True
                                continue
                            if in_metadata:
                                if line.startswith("[") and line != "[Metadata]":
                                    break  # end of metadata sect

                                if line.lower().startswith("title:") and song_name.lower() == line[6:].strip().lower():
                                    found_title = True
                                elif line.lower().startswith("artist:") and artist.lower() == line[7:].strip().lower():
                                    found_artist = True
                                elif line.lower().startswith("version:") and difficulty.lower() == line[8:].strip().lower():
                                    found_version = True

                        if found_title and found_artist and found_version:
                            matching_file.append(file_path)

            except UnicodeDecodeError: # not an osu! file
                continue
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return matching_file

if __name__ == "__main__":
    results = find_map("Arctic Monkeys", "505", "Normal")
    for r in results:
        print(r)