import os
from pathlib import Path

import m3u8
import requests
from dotenv import load_dotenv
from tqdm import tqdm


def download_m3u8_video(m3u8_url, output_filename):
    # Fetch the m3u8 playlist
    playlist_response = requests.get(m3u8_url)
    playlist_response.raise_for_status()
    playlist = m3u8.loads(playlist_response.text)

    # Get base URL for segments
    base_url = m3u8_url.rsplit("/", 1)[0] + "/"

    # Download all segments
    with Path.open(output_filename, "xb") as f:
        for segment in tqdm(
            playlist.segments, desc="Downloading segments", unit="segment"
        ):
            segment_url = segment.uri
            if segment_url is None:
                print("No segments found in the playlist.")
                return
            if not segment_url.startswith("http"):
                segment_url = base_url + segment_url
            seg_resp = requests.get(segment_url)
            seg_resp.raise_for_status()
            f.write(seg_resp.content)

    print(f"Video saved as {output_filename}")


def main():  # noqa C901
    load_dotenv()

    output_path = Path(os.getenv("OUTPUT_PATH", "./downloads"))
    api_url = os.getenv("API_URL")
    delimiter = os.getenv("DELIMITER")
    input_file = Path(os.getenv("INPUT_FILE", "./data/inputs.txt"))
    prefix = os.getenv("M3U8_PREFIX", "sd")

    while True:

        try:
            with Path.open(input_file) as file:
                names = []
                for line in file:
                    name = line.strip()
                    if delimiter:
                        parts = name.split(delimiter)
                        if len(parts) > 1:
                            name = parts[1].strip()
                    names.append(name)
        except FileNotFoundError:
            names = []
            name = input("Please enter the unique video name or URL: ").strip()
            if delimiter:
                name = name.split(delimiter)[1].strip()
            names.append(name)

        if not api_url:
            print("API_URL not set in environment variables.")
            return

        for i, n in enumerate(names):
            print(f"Downloading video {i + 1} of {len(names)}")

            m3u8_url = api_url + n + "/" + prefix + ".m3u8"

            filename = n + ".mp4"

            file_path = output_path / filename

            try:
                download_m3u8_video(m3u8_url, file_path)
            except requests.RequestException as e:
                print(f"Error downloading video {n}: {e}")
                print("Could it be an .mp4? Skipping to next video...")
                continue

            print()

        rerun = (
            input("\nDo you want to download another video? (y/any): ").strip().lower()
        )

        if rerun != "y":
            break


if __name__ == "__main__":
    main()
