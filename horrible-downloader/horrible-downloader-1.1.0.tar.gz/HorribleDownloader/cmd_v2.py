def fetch_episodes(show, last_watched, shared_data, global_args, lock):
    # default values for
    new = []
    shared_data[show] = []
    # print info if not quiet mode
    with lock:
        titles = shared_data.keys()
        clear()
        for title in titles:
            print(f"{fg(3)}FETCHING:{fg.rs} {title}")

    if global_args.batch:
        new = parser.get_batches(show)
        shared_data[show] = new[0]
    else:
        episodes = parser.get_episodes(show)
        if global_args.episodes:
            ep_filter = generate_episode_filter(global_args.episodes)
            new = list(filter(lambda s: ep_filter(s["episode"]), episodes))
        else:
            new = list(filter(lambda s: float(s["episode"]) > float(last_watched), episodes))

        shared_data[show] = new if new else None

    # print the dots...
    with lock:
        titles = shared_data.keys()
        clear()
        for title in titles:
            dots = "." * (50 - len(str(title)))
            if shared_data[title]:
                print(f"{fg(3)}FETCHING:{fg.rs} {title}{dots} {fg(10)}FOUND ({str(len(shared_data[title]))}){fg.rs}")
            else:
                if shared_data[title] is None:
                    print(f"{fg(3)}FETCHING:{fg.rs} {title}{dots} {fg(8)}NONE{fg.rs}")
                else:
                    print(f"{fg(3)}FETCHING:{fg.rs} {title}")
