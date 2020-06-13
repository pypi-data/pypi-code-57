#!/usr/bin/env python
import argparse
from openai.finetune import data_streams
import data_gym
import time
from termcolor import colored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("train_url")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    streamer = data_streams.stream_from_files(
        files=[args.train_url], n_ctx=100, seed=args.seed, overlap=0
    )
    enc = data_gym.text.get_encoding("reversible_50000")
    for x in streamer:
        tokens = x["tokens"][0].tolist()
        weights = x["weights"][0].tolist()
        assert len(tokens) == len(weights)
        for (t, w) in zip(tokens, weights):
            color = "white" if w > 0.1 else "blue"
            s = enc.decode([t])
            if s == "<|endoftext|>":
                print(colored("□", color="magenta"))
            else:
                print(colored(s, color=color), end="", flush=True)
            time.sleep(0.1)


if __name__ == "__main__":
    main()
