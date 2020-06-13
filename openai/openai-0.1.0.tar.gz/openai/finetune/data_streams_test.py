import json
import tempfile
import os.path as osp
from openai.finetune import data_streams
import data_gym
import blobfile


def val_stream_from_files():
    text = ",".join(str(i) for i in range(1000))
    tmpdir = tempfile.mkdtemp()
    fname = osp.join(tmpdir, "a.jsonl")
    print(fname)
    enc = data_gym.text.get_encoding("reversible_50000")
    with open(fname, "w") as fh:
        fh.write(json.dumps({"data": text}))
        fh.write("\n")
    stream = data_streams.stream_from_files(
        [fname], n_ctx=17, seed=0, shuffle=False, overlap=0
    )
    roundtrip = "".join([enc.decode(chunk["tokens"][0].tolist()) for chunk in stream])
    # pylint: disable=bad-str-strip-call
    assert roundtrip.rstrip("<|endoftext|>") == text


def val_estimate():
    paths = blobfile.glob("gs://easyfinetune/reddit-cleanjokes-*.jsonl")
    for path in paths:
        size_sub, stderr_sub = data_streams.get_num_tokens([path], n_samples=100)
        size_all, stderr_all = data_streams.get_num_tokens([path], n_samples=int(1e6))
        assert stderr_all == 0
        z = (size_all - size_sub) / stderr_sub
        errpct = 100 * (size_all - size_sub) / size_all
        assert abs(z) < 3
        print(
            f"Est: {size_sub:.1f} ± {stderr_sub:.1f}. True: {size_all}.",
            f"%err={errpct:.1f}, z={z:.1f}",
        )
