import json
import sys

import openai


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def organization_info(obj):
    organization = getattr(obj, "organization", None)
    if organization is not None:
        return "[organization={}] ".format(organization)
    else:
        return ""


def display(obj):
    sys.stderr.write(organization_info(obj))
    sys.stderr.flush()
    print(obj)


def display_error(e):
    extra = (
        " (HTTP status code: {})".format(e.http_status)
        if e.http_status is not None
        else ""
    )
    sys.stderr.write(
        "{}{}Error:{} {}{}\n".format(
            organization_info(e), bcolors.FAIL, bcolors.ENDC, e, extra
        )
    )


class Engine:
    @classmethod
    def get(cls, args):
        service_account = openai.Engine.retrieve(id=args.id)
        display(service_account)

    @classmethod
    def generate(cls, args):
        if args.completions and args.completions > 1 and args.stream:
            raise ValueError("Can't stream multiple completions with openai CLI")

        kwargs = {}
        if args.model is not None:
            kwargs["model"] = args.model
        resp = openai.Engine(id=args.id).generate(
            completions=args.completions,
            context=args.context,
            length=args.length,
            stream=args.stream,
            temperature=args.temperature,
            top_p=args.top_p,
            logprobs=args.logprobs,
            **kwargs,
        )
        if not args.stream:
            resp = [resp]

        for part in resp:
            completions = len(part["data"])
            for c_idx, c in enumerate(part["data"]):
                if completions > 1:
                    sys.stdout.write("===== Completion {} =====\n".format(c_idx))
                sys.stdout.write("".join(c["text"]))
                if completions > 1:
                    sys.stdout.write("\n")
                sys.stdout.flush()

    @classmethod
    def search(cls, args):
        resp = openai.Engine(id=args.id).search(
            documents=args.documents, query=args.query
        )
        scores = [
            (search_result["score"], search_result["document"])
            for search_result in resp["data"]
        ]
        scores.sort(reverse=True)
        for score, document_idx in scores:
            print("=== score {:.3f} ===".format(score))
            print(args.documents[document_idx])

    @classmethod
    def list(cls, args):
        engines = openai.Engine.list()
        display(engines)


class Branch:
    @classmethod
    def create(cls, args):
        resp = openai.Branch.create(
            engine=args.engine, model=args.model, timeout=args.timeout
        )
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.Branch.retrieve(
            engine=args.engine, id=args.id, timeout=args.timeout
        )
        print(resp)

    def _block(self, engine, id):
        while resp["status"] == "pending":
            resp = openai.Branch.retrieve(engine=args.engine, id=id, timeout=10)


class Completion:
    @classmethod
    def create(cls, args):
        if args.n is not None and args.n > 1 and args.stream:
            raise ValueError("Can't stream completions with n>1 with the current CLI")

        resp = openai.Completion.create(
            engine=args.engine,
            n=args.n,
            max_tokens=args.max_tokens,
            logprobs=args.logprobs,
            prompt=args.prompt,
            model=args.model,
            stream=args.stream,
            temperature=args.temperature,
            top_p=args.top_p,
        )
        if not args.stream:
            resp = [resp]

        for part in resp:
            choices = part["choices"]
            for c_idx, c in enumerate(sorted(choices, key=lambda s: s["index"])):
                if len(choices) > 1:
                    sys.stdout.write("===== Completion {} =====\n".format(c_idx))
                sys.stdout.write(c["text"])
                if len(choices) > 1:
                    sys.stdout.write("\n")
                sys.stdout.flush()


class Event:
    @classmethod
    def list(cls, args):
        resp = openai.Event.list(
            run=args.run,
            offset=args.offset,
            limit=args.limit,
            timeout=args.timeout,
            stream=args.stream,
        )
        if args.stream:
            for res in resp:
                print(json.dumps(res))
        else:
            print(resp)


class File:
    @classmethod
    def create(cls, args):
        resp = self._create(path=args.path, purpose=args.purpose)
        print(resp)

    @classmethod
    def _create(cls, purpose, path):
        with open(path) as f:
            return openai.File.create(purpose=purpose, file=f)

    @classmethod
    def get(cls, args):
        resp = openai.File.retrieve(id=args.id)
        print(resp)

    @classmethod
    def list(cls, args):
        resp = openai.File.list()
        print(resp)


class Plan:
    @classmethod
    def create(cls, args):
        if args.path is not None:
            file = File._create(purpose="plan", path=args.path).id
        else:
            file = args.file

        resp = openai.Plan.create(description=args.description, file=file)
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.Plan.retrieve(id=args.id)
        print(resp)

    @classmethod
    def delete(cls, args):
        plan = openai.Plan(id=args.id).delete()
        print(plan)

    @classmethod
    def list(cls, args):
        plans = openai.Plan.list()
        print(plans)


class Run:
    @classmethod
    def create(cls, args):
        resp = openai.Run.create(model=args.model, plan=args.plan)
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.Run.retrieve(id=args.id)
        print(resp)

    @classmethod
    def list(cls, args):
        resp = openai.Run.list()
        print(resp)


class Snapshot:
    @classmethod
    def create(cls, args):
        resp = openai.Snapshot.create(
            engine=args.engine,
            branch=args.branch,
            description=args.description,
            timeout=args.timeout,
        )
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.Snapshot.retrieve(
            engine=args.engine, id=args.id, timeout=args.timeout
        )
        print(resp)

    @classmethod
    def delete(cls, args):
        snapshot = openai.Snapshot(id=args.id).delete()
        print(snapshot)

    @classmethod
    def list(cls, args):
        snapshots = openai.Snapshot.list()
        print(snapshots)


class Tag:
    @classmethod
    def create(cls, args):
        resp = openai.Tag.create(id=args.id, model=args.model, force=args.force)
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.Tag.retrieve(id=args.id)
        print(resp)

    @classmethod
    def delete(cls, args):
        tag = openai.Tag(id=args.id).delete()
        print(tag)

    @classmethod
    def list(cls, args):
        tags = openai.Tag.list()
        print(tags)


class Update:
    @classmethod
    def create(cls, args):
        context = args.context
        try:
            parsed = json.loads(context)
        except json.decoder.JSONDecodeError:
            pass
        else:
            if isinstance(parsed, list):
                context = parsed

        mask = args.mask
        if args.mask is not None:
            mask = json.loads(mask)

        resp = openai.Update.create(
            engine=args.engine,
            branch=args.branch,
            scale=args.scale,
            context=context,
            mask=mask,
            timeout=args.timeout,
        )
        print(resp)

    @classmethod
    def get(cls, args):
        resp = openai.Update.retrieve(
            engine=args.engine, id=args.id, timeout=args.timeout
        )
        print(resp)


def register(parser):
    # Engine management
    subparsers = parser.add_subparsers(help="All API subcommands")

    def help(args):
        parser.print_help()

    parser.set_defaults(func=help)

    sub = subparsers.add_parser("engines.list")
    sub.set_defaults(func=Engine.list)

    sub = subparsers.add_parser("engines.get")
    sub.add_argument("-i", "--id", required=True)
    sub.set_defaults(func=Engine.get)

    sub = subparsers.add_parser("engines.generate")
    sub.add_argument("-i", "--id", required=True)
    sub.add_argument(
        "--stream", help="Stream tokens as they're ready.", action="store_true"
    )
    sub.add_argument("-c", "--context", help="An optional context to generate from")
    sub.add_argument("-l", "--length", help="How many tokens to generate", type=int)
    sub.add_argument(
        "-t",
        "--temperature",
        help="""What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.

Mutually exclusive with `top_p`.""",
        type=float,
    )
    sub.add_argument(
        "-p",
        "--top_p",
        help="""An alternative to sampling with temperature, called nucleus sampling, where the considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10%% probability mass are considered.

            Mutually exclusive with `temperature`.""",
        type=float,
    )
    sub.add_argument(
        "-n",
        "--completions",
        help="How many parallel completions to run on this context",
        type=int,
    )
    sub.add_argument(
        "--logprobs",
        help="Include the log probabilites on the `logprobs` most likely tokens. So for example, if `logprobs` is 10, the API will return a list of the 10 most likely tokens. If `logprobs` is supplied, the API will always return the logprob of the generated token, so there may be up to `logprobs+1` elements in the response.",
        type=int,
    )
    sub.add_argument(
        "--stop", help="A stop sequence at which to stop generating tokens."
    )
    sub.add_argument(
        "-m",
        "--model",
        required=False,
        help="A model (most commonly a snapshot ID) to generate from. Defaults to the engine's default snapshot.",
    )
    sub.set_defaults(func=Engine.generate)

    sub = subparsers.add_parser("engines.search")
    sub.add_argument("-i", "--id", required=True)
    sub.add_argument(
        "-d",
        "--documents",
        action="append",
        help="List of documents to search over",
        required=True,
    )
    sub.add_argument("-q", "--query", required=True, help="Search query")
    sub.set_defaults(func=Engine.search)

    ## Completions
    sub = subparsers.add_parser("completions.create")
    sub.add_argument(
        "-e",
        "--engine",
        required=False,
        help="An optional engine (dedicated capacity) to use",
    )
    sub.add_argument(
        "--stream", help="Stream tokens as they're ready.", action="store_true"
    )
    sub.add_argument("-p", "--prompt", help="An optional prompt to complete from")
    sub.add_argument(
        "-M", "--max-tokens", help="The maximum number of tokens to generate", type=int
    )
    sub.add_argument(
        "-t",
        "--temperature",
        help="""What sampling temperature to use. Higher values means the model will take more risks. Try 0.9 for more creative applications, and 0 (argmax sampling) for ones with a well-defined answer.

Mutually exclusive with `top_p`.""",
        type=float,
    )
    sub.add_argument(
        "-P",
        "--top_p",
        help="""An alternative to sampling with temperature, called nucleus sampling, where the considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10%% probability mass are considered.

            Mutually exclusive with `temperature`.""",
        type=float,
    )
    sub.add_argument(
        "-n",
        "--n",
        help="How many sub-completions to generate for each prompt.",
        type=int,
    )
    sub.add_argument(
        "--logprobs",
        help="Include the log probabilites on the `logprobs` most likely tokens, as well the chosen tokens. So for example, if `logprobs` is 10, the API will return a list of the 10 most likely tokens. If `logprobs` is 0, only the chosen tokens will have logprobs returned.",
        type=int,
    )
    sub.add_argument(
        "--stop", help="A stop sequence at which to stop generating tokens."
    )
    sub.add_argument(
        "-m",
        "--model",
        # required=True,
        help="The model (most commonly a snapshot ID) to use",
    )
    sub.set_defaults(func=Completion.create)

    # Events

    sub = subparsers.add_parser("events.list")
    sub.add_argument("-r", "--run", required=True, help="The run ID to filter by")
    sub.add_argument(
        "-s", "--stream", action="store_true", help="Stream events as they're ready"
    )
    sub.add_argument(
        "-o",
        "--offset",
        type=int,
        help="A cursor, allows you to offset into the stream. Negative indexes allow you to index from the current end of the stream.",
    )
    sub.add_argument("-l", "--limit", type=int, help="How many records to return.")
    sub.add_argument(
        "-t",
        "--timeout",
        help="An optional amount of time to block for new events. If the timeout expires, an empty list will be returned.",
        type=float,
    )
    sub.set_defaults(func=Event.list)

    # Files
    sub = subparsers.add_parser("files.create")
    sub.add_argument("--purpose", default="plan")
    sub.add_argument("-p", "--path", required=True)
    sub.set_defaults(func=File.create)

    sub = subparsers.add_parser("files.get")
    sub.add_argument("-i", "--id", required=True, help="The file ID")
    sub.set_defaults(func=File.get)

    sub = subparsers.add_parser("files.list")
    sub.set_defaults(func=File.list)

    # Plans
    sub = subparsers.add_parser("plans.create")
    sub.add_argument(
        "-d", "--description", help="A human-readable description of this plan"
    )
    sub.add_argument(
        "-f", "--file", help="An uploaded JSONL file corresponding to the plan"
    )
    sub.add_argument("-p", "--path")
    sub.set_defaults(func=Plan.create)

    sub = subparsers.add_parser("plans.get")
    sub.add_argument("-i", "--id", required=True, help="The plan ID")
    sub.set_defaults(func=Plan.get)

    sub = subparsers.add_parser("plans.delete")
    sub.add_argument("-i", "--id", required=True, help="The plan ID")
    sub.set_defaults(func=Plan.delete)

    sub = subparsers.add_parser("plans.list")
    sub.set_defaults(func=Plan.list)

    # Runs
    sub = subparsers.add_parser("runs.create")
    sub.add_argument(
        "-m",
        "--model",
        required=True,
        help="A model (most commonly a snapshot ID) to start the run from",
    )
    sub.add_argument("-p", "--plan", required=True, help="The plan to apply.")
    sub.set_defaults(func=Run.create)

    sub = subparsers.add_parser("runs.get")
    sub.add_argument("-i", "--id", required=True, help="The run ID")
    sub.set_defaults(func=Run.get)

    sub = subparsers.add_parser("runs.update")
    sub.add_argument("-i", "--id", required=True, help="The run ID")
    sub.set_defaults(func=Run.get)

    sub = subparsers.add_parser("runs.list")
    sub.set_defaults(func=Run.list)

    ## Snapshots
    sub = subparsers.add_parser("snapshots.list")
    sub.set_defaults(func=Snapshot.list)

    sub = subparsers.add_parser("snapshots.create")
    sub.add_argument(
        "-e", "--engine", required=True, help="The engine this snapshot is running on"
    )
    sub.add_argument(
        "-b", "--branch", required=True, help="The branch to turn into a snapshot"
    )
    sub.add_argument(
        "-d", "--description", help="A human-readable description of this snapshot"
    )
    sub.add_argument(
        "-t",
        "--timeout",
        help="An optional amount of time to block for the snapshot to transition from pending. If the timeout expires, a pending snapshot will be returned.",
        type=float,
    )
    sub.set_defaults(func=Snapshot.create)

    sub = subparsers.add_parser("snapshots.get")
    sub.add_argument("-e", "--engine", help="The engine this snapshot is running on")
    sub.add_argument("-i", "--id", required=True, help="The snapshot ID")
    sub.add_argument(
        "-t",
        "--timeout",
        help="An optional amount of time to block for the snapshot to transition from pending. If the timeout expires, a pending snapshot will be returned.",
        type=float,
    )
    sub.set_defaults(func=Snapshot.get)

    sub = subparsers.add_parser("snapshots.delete")
    sub.add_argument("-i", "--id", required=True, help="The snapshot ID")
    sub.set_defaults(func=Snapshot.delete)

    # Tags
    sub = subparsers.add_parser("tags.create")
    sub.add_argument("-i", "--id", help="The ID of the tag to create", required=True)
    sub.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Whether to overwrite an existing tag with this ID",
    )
    sub.add_argument(
        "-m",
        "--model",
        help="Which model (most commonly a snapshot ID) to tag",
        required=True,
    )
    sub.set_defaults(func=Tag.create)

    sub = subparsers.add_parser("tags.get")
    sub.add_argument("-i", "--id", required=True, help="The tag ID")
    sub.set_defaults(func=Tag.get)

    sub = subparsers.add_parser("tags.delete")
    sub.add_argument("-i", "--id", required=True, help="The tag ID")
    sub.set_defaults(func=Tag.delete)

    sub = subparsers.add_parser("tags.list")
    sub.set_defaults(func=Tag.list)

    ## Updates
    sub = subparsers.add_parser("updates.create")
    sub.add_argument(
        "-e", "--engine", required=True, help="The engine this update is running on"
    )
    sub.add_argument(
        "-b", "--branch", required=True, help="The branch to make a update on"
    )
    sub.add_argument(
        "-c",
        "--context",
        help="The data to train on: either a string, a list of strings, or a list of tokens (encoded as JSON)",
        required=True,
    )
    sub.add_argument(
        "--mask",
        help="An array of numbers specifying relative training weight for each token (encoded as JSON)",
    )
    sub.add_argument("-s", "--scale", help="How large of a update to take", type=float)
    sub.add_argument(
        "-t",
        "--timeout",
        help="An optional amount of time to block for the update to transition from pending. If the timeout expires, a pending update will be returned.",
        type=float,
    )
    sub.set_defaults(func=Update.create)

    sub = subparsers.add_parser("updates.get")
    sub.add_argument(
        "-e", "--engine", required=True, help="The engine this update is running on"
    )
    sub.add_argument("-i", "--id", required=True, help="The update ID")
    sub.add_argument(
        "-t",
        "--timeout",
        help="An optional amount of time to block for the update to transition from pending. If the timeout expires, a pending update will be returned.",
        type=float,
    )
    sub.set_defaults(func=Update.get)
