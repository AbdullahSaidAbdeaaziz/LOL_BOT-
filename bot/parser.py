from dataclasses import dataclass

from .constants import SUPPORTED_REGIONS


@dataclass(frozen=True)
class SummonerRecord:
    region: str
    name: str
    tag: str


def parse_summoners_lines(lines):
    summoners = []
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) != 3:
            raise ValueError(
                f"Invalid format on line {line_number}. Expected: <region> <name> <tag>"
            )

        region, name, tag = parts
        region = region.lower()
        if region not in SUPPORTED_REGIONS:
            raise ValueError(
                f"Unsupported region '{region}' on line {line_number}. "
                f"Allowed regions: {', '.join(sorted(SUPPORTED_REGIONS))}"
            )

        if not name or not tag:
            raise ValueError(f"Missing name or tag on line {line_number}")

        summoners.append(SummonerRecord(region=region, name=name, tag=str(tag)))

    return summoners
