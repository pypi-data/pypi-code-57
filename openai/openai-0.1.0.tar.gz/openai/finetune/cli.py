import argparse
import json
import logging
import os
import sys
import tempfile
from datetime import datetime

import openai
from openai.finetune import train
from openai.finetune.planner import Planner, SyncPlanner
from openai import error

logger = logging.getLogger(__name__)


def verify_files_exist(urls):
    # TODO
    pass


def finetune(args):
    logging.getLogger("openai.finetune").setLevel(
        min(logging.INFO, logger.getEffectiveLevel())
    )

    if args.engine:
        finetune_sync(args)
    else:
        finetune_async(args)


def finetune_sync(args):
    logger.info(f"Preparing fine-tuning run on engine={args.engine} model={args.model}")
    planner = SyncPlanner(engine=args.engine, model=args.model, encoding=args.encoding)
    train_paths = args.train.split(",")
    val_paths = args.val.split(",") if args.val else []
    verify_files_exist(train_paths + val_paths)
    train.train(
        planner=planner,
        update_scale=args.scale,
        max_tokens=args.max_tokens,
        train_paths=train_paths,
        val_paths=val_paths,
        num_epochs=args.num_epochs,
        train_batch_size=args.batch_size,
        val_batch_size=args.val_batch_size,
    )


def finetune_async(args):
    from openai.finetune import train

    create_plan = args.plan
    create_run = create_plan and args.model
    do_stream = create_run and args.stream

    if not create_plan and args.output is None:
        logger.info(
            "Must save to a local path by passing -o <file> if you are not going to create a plan."
        )
        return

    if do_stream:
        logger.info(f"Will fine-tune on {args}")

    train_paths = args.train.split(",")
    val_paths = args.val.split(",") if args.val else []
    verify_files_exist(train_paths + val_paths)

    planner = Planner(encoding=args.encoding, output=args.output)
    if args.output is None:
        logger.info(
            f"Building plan in tempfile: {planner.file.name} (pass -o <file> to save to disk)."
        )
    else:
        logger.info(
            f"Building plan in {planner.file.name} and will output to {args.output}"
        )

    logger.info(
        f"Building fine-tuning plan. Each line will have at most {args.max_tokens} tokens, each training batch will have {args.batch_size} examples, and each validation batch will have at most {args.val_batch_size} examples"
    )
    train.train(
        planner=planner,
        update_scale=args.scale,
        max_tokens=args.max_tokens,
        train_paths=train_paths,
        val_paths=val_paths,
        num_epochs=args.num_epochs,
        train_batch_size=args.batch_size,
        val_batch_size=args.val_batch_size,
    )

    try:
        if create_plan:
            logger.info(f"Uploading file to create plan object...")
            planner.file.seek(0)
            file = openai.File.create(purpose="plan", file=planner.file)
            plan = openai.Plan.create(
                description=args.description or "Plan from openai fine-tune",
                file=file.id,
            )
            logger.info(f"Plan created: {plan}")
        else:
            plan = None
    finally:
        planner.close()
    if args.output:
        logger.info(f"Plan contents are available in {args.output}")

    if create_run:
        run = openai.Run.create(model=args.model, plan=plan.id)
        logger.info(f"Started run on {args.model}: {run}")
        if not do_stream:
            logger.info(
                f"You can monitor its progress: openai api events.list -r {run.id} -s"
            )
    elif create_plan:
        logger.info(
            f"You can now start any number of runs with your plan. For example, run this to fine-tune ada: openai api runs.create -p {plan.id} -s ada"
        )
    else:
        logger.info(
            f"You can now upload your file to create a plan, and then use that to create any number of runs. For example, run this to make a plan: openai api plans.create -f {args.output}"
        )

    if do_stream:
        logger.info(
            f"Waiting on progress. Resume any time: openai api events.list -r {run.id} -s"
        )
        for res in openai.Event.list(run=run.id, stream=True):
            print(json.dumps(res))

    return args.output


def register(subparsers):
    sub = subparsers.add_parser(
        "fine-tune",
        help="Produce a fine-tuned snapshot on your own dataset",
        description=""""
This subcommand lets you fine-tuned snapshot on your own dataset.

Data formats accepted are:

- txt: Just provide a text file with your data, and we'll treat it all as data to learn on.
- jsonl: Provide a
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    sub.add_argument(
        "-t", "--train", help="Comma-separated list of files to train on", required=True
    )
    sub.add_argument("-v", "--val", help="Comma-separated list of files to evaluate on")
    sub.add_argument("--log-path", help="Directory to write logs to")
    sub.add_argument(
        "--num-epochs",
        default=1,
        type=int,
        help="The number of epochs to run over training set.",
    )
    sub.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="How many examples to have in each step.",
    )
    sub.add_argument(
        "--val-batch-size",
        type=int,
        default=50,
        help="How many examples to have in each val step.",
    )
    sub.add_argument(
        "-s",
        "--scale",
        type=float,
        help="How much to scale the update size by",
        default=1,
    )
    sub.add_argument(
        "--max-tokens",
        type=int,
        help="Set the max number of tokens in each training example",
        default=2048,
    )
    sub.add_argument(
        "--encoding",
        help="Set the encoding used in this plan",
        default="byte-pair-encoding-v0",
    )

    # API options
    sub.add_argument("-o", "--output", help="Save fine-tuning file to a local path")
    sub.add_argument("-d", "--description", help="A description for the Plan")
    sub.add_argument(
        "-P",
        "--no-plan",
        dest="plan",
        default=True,
        action="store_false",
        help="Do not upload the file and create a Plan object",
    )
    sub.add_argument("-m", "--model", help="What model to run with")
    sub.add_argument(
        "-e", "--engine", help="What engine to run with (will run synchronously)"
    )
    sub.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        help="Whether to stream back results",
    )
    sub.set_defaults(func=finetune)


def main():
    parser = argparse.ArgumentParser()
    # API configuration
    parser.add_argument("-b", "--api-base", help="What API base url to use.")
    parser.add_argument("-k", "--api-key", help="What API key to use.")
    parser.add_argument(
        "-o",
        "--organization",
        help="Which organization to run as (will use your default organization if not specified)",
    )
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(help="sub-command help")
    register(subparsers)

    args = parser.parse_args()
    if args.func is None:
        parser.print_help()
        return

    logger.setLevel(logging.INFO)

    if args.api_key is not None:
        openai.api_key = args.api_key
    if args.api_base is not None:
        openai.api_base = args.api_base
    if args.organization is not None:
        openai.organization = args.organization
    openai.debug = True
    openai.max_network_retries = 5

    args.func(args)


if __name__ == "__main__":
    main()
