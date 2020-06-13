import logging
import os.path as osp
import time
from contextlib import contextmanager

from openai.finetune.load_dataset import load_dataset, Sampler
import openai
from openai.finetune import data_streams, util

logger = logging.getLogger(__name__)


@contextmanager
def scoped_log(message):
    tstart = time.time()
    logger.info(f"▕▔ {message}")
    yield
    logger.info(f"▕▁ Done in {time.time()-tstart:.2f} seconds")


# SCHED_FNS = dict(
#     none=lambda x: 1, cos=lambda x: np.cos(x * np.pi / 2), linear=lambda x: 1 - x
# )


def train(
    *,
    planner,
    update_scale,
    max_tokens,
    train_paths,
    val_paths,
    num_epochs,
    train_batch_size,
    val_batch_size,
):
    stream_kwargs = dict(tokens_per_example=max_tokens)
    # with scoped_log("Determining number of tokens"):
    #     train_ntok = data_streams.estimate_num_tokens(
    #         train_paths, enc=planner.make_encoding()
    #     )[0]
    #     logger.info(f"You training dataset is an estimated {train_ntok:,} tokens")

    # decayed_scale = 0
    # iepoch = -1
    # train_it = data_streams.stream_from_files(
    #     train_paths,
    #     **stream_kwargs,
    #     batch_size=train_batch_size,
    #     seed=iepoch,
    #     enc=planner.make_encoding(),
    #     pack=False,
    #     allow_partial_batch=True,
    # )
    # with scoped_log(f"Warmup"):
    #     train_epoch(
    #         planner=planner,
    #         data_iterator=train_it,
    #         toks_total=train_ntok,
    #         epnum=iepoch,
    #         update_scale=decayed_scale,
    #     )

    import itertools

    # enwik8
    # validation = [
    #     d.tolist()
    #     for d in load_dataset(
    #         enc=planner.make_encoding(), path=val_paths[0], combine=None
    #     )
    # ]
    # validation = [list(itertools.islice(v[:50000], 2049)) for v in validation]

    prompt = """You are Jon, a knight living in the kingdom of Larion. You have a steel longsword and a wooden shield. You are on a quest to defeat the evil dragon of Larion. You've heard he lives up at the north of the kingdom. You set on the path to defeat him and walk into a dark forest. As you enter the forest you see the dragon. He is surrounded by several men with crossbows and in their hands are three throwing knives.

"I didn't ask what you were doing here." a man says, "Did you come to free me from my torment?"
> You ask what's going on.
"What's going on? Why are you doing this?"
"I'm a knight, sir."
"Larion, Aethelwulf, let me go!"
"Sure, sure! Just keep your head down!"
> You attack the men.
You swing your blade"""

    for iepoch in range(num_epochs):
        decayed_scale = update_scale * (1 - iepoch / num_epochs)
        train_it = data_streams.stream_from_files(
            train_paths,
            **stream_kwargs,
            batch_size=train_batch_size,
            seed=iepoch,
            enc=planner.make_encoding(),
        )
        with scoped_log(f"Running epoch: {iepoch}"):
            for i, batch in enumerate(train_it):
                if i % 4 == 0:
                    ### Eval
                    # planner.add(
                    #     "POST /v1/completions",
                    #     prompt=validation,
                    #     logprobs=5,
                    #     max_tokens=0,
                    #     echo=True,
                    # )
                    ### Sampling eval
                    planner.add("POST /v1/completions", n=10, max_tokens=128, echo=True)

                    ### Sampling eval
                    planner.add(
                        "POST /v1/completions",
                        n=10,
                        max_tokens=128,
                        prompt=prompt,
                        temperature=0.4,
                        # presence_penalty=0.6,
                        # frequency_penalty=0.2,
                    )
                    if i > 0 and i % 100 == 0:
                        planner.add(
                            "POST /v1/snapshots",
                            description=f"Step {i} of openai-finetune",
                        )

                # TODO in-epoch update_scale planner, probably cosine
                planner.add(
                    "POST /v1/updates",
                    example=batch["tokens"],
                    mask=batch["mask"],
                    scale=decayed_scale,
                )


def save_snapshot(planner, epoch):
    planner.add("POST /v1/snapshots", description=f"Epoch {epoch} of openai-finetune")


def eval_step(planner, batch):
    planner.add(
        "POST /v1/completions",
        prompt=batch["tokens"],
        logprobs=0,
        max_tokens=0,
        echo=True,
    )


def train_epoch(planner, data_iterator, epnum, update_scale):
    toks_done = 0
    tokens = []

    last_update = None
    last_toks = None


def val_epoch(planner, data_iterator):
    for batch in data_iterator:
        eval_step(planner, batch)
