"""Remove private JPEG metadata without changing the compressed photo data."""
from pathlib import Path

source = Path(__file__).resolve().parents[2] / "KakaoTalk_20261020_204243534.jpg"
target = Path(__file__).resolve().parents[1] / "dist" / "images" / "profile.jpg"
data = source.read_bytes()
if data[:2] != b"\xff\xd8":
    raise ValueError("Source is not a JPEG")

result = bytearray(data[:2])
cursor = 2
removed = 0
while cursor < len(data):
    if data[cursor] != 0xFF:
        raise ValueError("Unexpected JPEG marker")
    marker_start = cursor
    while data[cursor] == 0xFF:
        cursor += 1
    marker = data[cursor]
    cursor += 1
    if marker == 0xDA:  # Start of scan: keep the compressed image verbatim.
        result.extend(data[marker_start:])
        break
    if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
        result.extend(data[marker_start:cursor])
        continue
    length = int.from_bytes(data[cursor:cursor + 2], "big")
    end = cursor + length
    if marker in (0xE1, 0xED, 0xFE):  # EXIF/XMP, IPTC, comments.
        removed += 1
    else:
        result.extend(data[marker_start:end])
    cursor = end
else:
    raise ValueError("JPEG start of scan not found")

target.parent.mkdir(parents=True, exist_ok=True)
target.write_bytes(result)
print(f"Wrote {target.name}: {len(result)} bytes; removed {removed} metadata segments")
