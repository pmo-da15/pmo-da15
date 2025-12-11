from argparse import ArgumentParser
import asyncio
from contextlib import contextmanager
import sys

from tqdm import tqdm

from core.config import Config
from core.extraction import extract_fragments_from_document
from core.llm_store import LlmStore
from core.scraping import scrape_md
from core.summarization import (
    SUMMARIZATION_CRITERIONS_FULL_NAMES,
    SummarizationCriterions,
    SummarizationOutput,
    summarize_fragments,
)


async def run_pipeline(cfg: Config, url: str) -> SummarizationOutput:
    llm_store = LlmStore(cfg)

    tqdm.write(f"scraping {url}...")
    md = await scrape_md(url)

    tqdm.write(f"extracting fragments from {url}...")

    extractor = llm_store[cfg.extractor]
    fragments = await extract_fragments_from_document(extractor, md)

    tqdm.write("compiling the page report")

    summarizer = llm_store[cfg.summarizer]
    output = await summarize_fragments(summarizer, fragments)

    return output


def format_output_md(out: SummarizationOutput) -> str:
    r = "# Criterions\n\n"

    for criterion in SummarizationCriterions.model_fields:
        full_name = SUMMARIZATION_CRITERIONS_FULL_NAMES[criterion]
        data = getattr(out.criterions, criterion)

        r += f"## {full_name}\n"
        r += f"**Score**: {data.score}\n\n"
        r += f"**Comment**: {data.comment}\n\n"

    r += "\n# Recommendations\n\n"

    for recommendation in out.recommendations:
        r += recommendation + "\n\n"

    return r


parser = ArgumentParser()

parser.add_argument(
    "-c",
    "--config",
    type=str,
    required=True,
    help="path to config file",
)

parser.add_argument(
    "--output-json",
    type=str,
    action="append",
    nargs=1,
    metavar="FILE",
    help='write JSON output to file. pass "-" to write to stdout',
)

parser.add_argument(
    "--output-markdown",
    type=str,
    action="append",
    nargs=1,
    metavar="FILE",
    help='write Markdown output to file. pass "-" to write to stdout',
)

parser.add_argument(
    "url",
    type=str,
    help="URL to analyze",
)


def args_to_list(arg):
    if arg is None:
        return []
    return [a[0] for a in arg]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@contextmanager
def output_manager(path):
    if path == "-":
        yield sys.stdout
    else:
        with open(path, "w") as file:
            yield file


def main():
    args = parser.parse_args()

    output_json = args_to_list(args.output_json)
    output_markdown = args_to_list(args.output_markdown)

    if len(output_json) == 0 and len(output_markdown) == 0:
        eprint("Please, specify at least 1 --output-json or --output-markdown")
        exit(1)

    with open(args.config, "r") as file:
        cfg = Config.model_validate_json(file.read())

    result = asyncio.run(run_pipeline(cfg, args.url))

    for output in output_json:
        with output_manager(output) as file:
            file.write(result.model_dump_json(indent=4))

    for output in output_markdown:
        with output_manager(output) as file:
            file.write(format_output_md(result))
