import argparse
import asyncio
import json
from pathlib import Path
from typing import Optional

from document_loader import load_text_from_source
from agent import run_comparison


async def _async_run(primary: str, secondary: str) -> dict:
    primary_text, secondary_text = await asyncio.gather(
        load_text_from_source(primary), load_text_from_source(secondary)
    )
    result = await run_comparison(primary_text, secondary_text)
    return result.model_dump()


def main():
    parser = argparse.ArgumentParser(
        description="Compare two policy documents (primary vs secondary) and output structured JSON."
    )
    parser.add_argument("primary", help="Primary document path or SAS URL")
    parser.add_argument("secondary", help="Secondary document path or SAS URL")
    parser.add_argument(
        "-o", "--output", type=Path, help="Optional path to write JSON result"
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print JSON (default if writing to file)"
    )
    args = parser.parse_args()

    try:
        payload = asyncio.run(_async_run(args.primary, args.secondary))
    except Exception as exc:  # pragma: no cover
        parser.exit(status=1, message=f"Error: {exc}\n")

    indent: Optional[int] = 2 if (args.pretty or args.output) else None
    text = json.dumps(payload, ensure_ascii=False, indent=indent)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text)


if __name__ == "__main__":  # pragma: no cover
    main()
