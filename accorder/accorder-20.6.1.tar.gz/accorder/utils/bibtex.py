import pathlib
import subprocess
import itertools
import hashlib
import click
import base64
import json
from accorder.utils.cover import G_JPG
from pybtex.database import parse_file
from pybtex.database import BibliographyData
import pybtex.errors

pybtex.errors.set_strict_mode(False)


def no_calibre():
    click.echo("Please, check if you have Calibre installed and it is possible to run it as simple as `calibre` from your command line. Also, make sure it doesn't run while you run accorder against your Bibtex file. Once ready, please try this again.")
    exit(1)

def sanitize(o):
    return o.replace("}", "").replace("{", "").replace("""\\""", "")

def process_bibtex(bibtex_path):
    click.echo()
    click.echo(f">>>> IMPORT FROM BIBTEX:")
    click.echo(f">>>> {bibtex_path}")
    bib_data = parse_file(bibtex_path)
    entries = []
    fields = ['title', 'isbn', 'abstract', 'language', 'publisher',
              'edition', 'year', 'series', 'journal', 'issn', 'doi',
              'volume', 'number', 'pmid', 'pmcid']

    book_extensions = ['azw', 'azw3', 'cbz', 'chm', 'djvu', 'doc',
                       'docx', 'fb2', 'htmlz', 'mbp', 'md',
                       'txt', 'zip', 'mobi', 'epub', 'pdf']

    for bb in bib_data.entries.items():
        b = bb[1]
        entry = {}

        if 'file' in b.fields:
            sep = ":"
            if b.fields['file'].startswith('files/'):
                sep = ";"

            entry['file'] = {}
            for l in b.fields['file'].split(sep):
                if l.startswith("files/") and l.split(".")[-1] in book_extensions:
                    if pathlib.Path(bibtex_path).parent.joinpath(l).exists():
                        entry['file'][l.split(".")[-1]] = l

        if 'file' not in entry or not entry['file']:
            continue

        for field in [f for f in fields if f in b.fields]:
            entry[field] = sanitize(b.fields[field])

        entry['title'] = entry['title'].replace("#", "")

        if 'author' not in b.persons and 'editor' not in b.persons:
            continue

        authors = []
        authors_sort = []
        for role in ['author', 'editor']:
            if role in b.persons:
                for author in b.persons[role]:
                    first_names = sanitize(" ".join(author.bibtex_first_names))
                    prelast_names = sanitize(" ".join(author.prelast_names))
                    last_names = sanitize(" ".join(author.last_names))
                    author = f"{first_names} {prelast_names} {last_names}".replace("  ", " ").strip()
                    author_sort = f"{last_names}, {first_names} {prelast_names}".replace("  ", " ").strip()
                    authors_sort.append(author_sort)
                    authors.append(author)

        entry['authors'] = " & ".join(authors)
        entry['author_sort'] = " & ".join(authors_sort)

        if 'keywords' in b.fields:
            keywords = set(list(itertools.chain.from_iterable(
                [[sanitize(t).lower().strip().replace(",","") for t in k.split("/")]
                for k in b.fields['keywords'].split(",")])))
            entry['keywords'] = ",".join(keywords)


        bibhash = base64.b64encode(hashlib.md5(BibliographyData({bb[0]: b}).to_string('bibtex').encode()).digest()).decode()[:6]
        bibkey = base64.b64encode(hashlib.md5(bb[0].encode()).digest()).decode()[:6]
        entry['bibhash'] = f"{bibkey}{bibhash}"
        entry['bibtex_key'] = bb[0]
        entries.append(entry)
    return entries

def set_metadata(entry, cid, calibre_directory, bibtex_path):
    cl = ["calibredb", "set_metadata", f"--with-library={calibre_directory}"]

    if 'authors' in entry:
        cl.append("-f")
        cl.append(f"authors:{entry['authors']}")

    if 'author_sort' in entry:
        cl.append("-f")
        cl.append(f"author_sort:{entry['author_sort']}")


    if 'title' in entry:
        cl.append("-f")
        cl.append(f"title:{entry['title']}")
        cl.append("-f")
        cl.append(f"sort:{entry['title']}")

    for f in ['isbn', 'issn', 'doi', 'pmid', 'pmcid', 'bibhash']:
        if f in entry:
            cl.append("-f")
            cl.append(f"identifiers:{f}:{entry[f]}")

    if 'keywords' in entry:
        cl.append("-f")
        cl.append(f"tags:{entry['keywords']}")

    if 'language' in entry:
        cl.append("-f")
        cl.append(f"languages:{entry['language']}")

    if "abstract" in entry:
        cl.append("-f")
        cl.append(f"comments:{entry['abstract']}")

    if "publisher" in entry:
        cl.append("-f")
        cl.append(f"publisher:{entry['publisher']}")

    for f in ["series", "journal"]:
        if f in entry:
            cl.append("-f")
            cl.append(f"series:{entry[f]}")

    if "volume" in entry and entry['volume'].isdigit():
        if "number" in entry and entry['number'].isdigit():
            if int(entry["number"]) in range(10, 100):
                entry["volume"] += f".{entry['number']}"
            elif int(entry["number"]) in range(1, 10):
                entry["volume"] += f".0{entry['number']}"

        cl.append("-f")
        cl.append(f"series_index:{entry['volume']}")

    if "year" in entry:
        if "month" in entry:
            entry["year"] += f"/{entry['month']}"
        cl.append("-f")
        cl.append(f"pubdate:{entry['year']}")

    cl.append(cid)
    rp = subprocess.run(cl, capture_output=True)

    if rp.returncode != 0:
        click.echo(f"[bibhash: {entry['bibhash']}: '{entry['title']}' by ['authors']]. FAILED to set metadata for {cid} in Calibre")
        exit(1)
    else:
        for fline in entry['file'].values():
            cl = ["calibredb", "add_format", f"--with-library={calibre_directory}", cid]
            cl.append(pathlib.Path(bibtex_path).parent.joinpath(fline).as_posix())
            fp = subprocess.run(cl, capture_output=True)
            if fp.returncode != 0:
                click.echo(f"[bibhash: {entry['bibhash']}: '{entry['title']}' by ['authors']]. FAILED to add_format for {cid} in Calibre")
                exit(1)
        else:
            return "SUCCESS"

def run_calibre(entries, bibtex_path, calibre_directory):
    total = len(entries)
    total_s = 0
    total_d = 0
    total_u = 0

    check_calibre = subprocess.run(["calibre", "-s"])

    if check_calibre.returncode != 0:
        no_calibre()

    click.echo()
    for i, entry in enumerate(entries):
        status = "NEW"
        n = i + 1
        cid = None

        bibkey = entry["bibhash"][:6]
        cl = ["calibredb", "list", "-f", "id",  "-s", f'identifier:"bibhash:{bibkey}"', f"--with-library={calibre_directory}", "--for-machine"]
        cl2 = ["calibredb", "list", "-f", "id", "-s",  f"identifiers:bibhash:{entry['bibhash']}", f"--with-library={calibre_directory}", "--for-machine"]

        kp = subprocess.run(cl, capture_output=True)
        if kp.returncode != 0:
            click.echo(kp)
            no_calibre()
        else:
            #[k['id'] for k in json.loads(cop.stdout.decode()) if not 'cover' in k.keys()]
            bids = json.loads(kp.stdout.decode())
            if bids:
                bp = subprocess.run(cl2, capture_output=True)
                if bp.returncode !=0:
                    click.echo(bp)
                    no_calibre()
                else:
                    hids = json.loads(kp.stdout.decode())
                    if len(hids) > 1:
                        click.echo("This is very weird. Let's just skip this book.")
                        continue
                    elif hids[0] in bids:
                        click.echo(f"{n}/{total} DUPLICATE: {entry['title']} by {entry['authors']}")
                        total_d += 1
                        continue
                    elif not hids:
                        status = "UPDATE"
                        total_u += 1
                        cid = hids[0]

        if not cid:
            cl = ["calibredb", "add", f"--with-library={calibre_directory}"]
            cl.append("-t")
            cl.append(entry['title'])
            if 'pdf' in entry['file'].keys():
                fpath = entry['file']['pdf']
            else:
                fpath = [*entry['file'].values()][0]

            cl.append(pathlib.Path(bibtex_path).parent.joinpath(fpath).as_posix())
            p = subprocess.run(cl, capture_output=True)
            if p.stderr.decode().startswith("The following books were not added as they already exist in the database"):
                click.echo(f"{n}/{total} DUPLICATE: {entry['title']} by {entry['authors']} (via calibredb stderr)")
                total_d += 1
                continue
            elif p.returncode != 0:
                click.echo(f"Adding book failed....")
                no_calibre()
            else:
                cid = p.stdout.decode().split("ids: ")[1].strip()
                if not cid.isdigit():
                    click.echo(f"Reading ID of the empty book jus added failed: {p.stdout}")
                    exit(1)

        sm = set_metadata(entry, cid, calibre_directory, bibtex_path)
        if sm == "SUCCESS":
            total_s += 1
            click.echo(f"{n}/{total} {status}: {entry['title']} by {entry['authors']}")


    cl = ["calibredb", "list", "-f", "cover", f"--with-library={calibre_directory}", "--for-machine"]
    cop = subprocess.run(cl, capture_output=True)
    cover_path = f"{calibre_directory}g.jpg"
    if cop.returncode == 0:
        with open(cover_path, "wb") as img:
            img.write(base64.decodebytes(G_JPG))

        for kid in [k['id'] for k in json.loads(cop.stdout.decode()) if not 'cover' in k.keys()]:
            cl = ["calibredb", "set_metadata", f"--with-library={calibre_directory}"]
            cl.append("-f")
            cl.append(f'cover:{cover_path}')
            cl.append(str(kid))
            cop = subprocess.run(cl, capture_output=True)

        pathlib.Path(cover_path).unlink()

    total_n = abs(total_s - total_u)
    updated = ""
    duplicates = ""
    cand = ""
    band = ""
    if total_u > 0:
        updated = f"\n   * {total_u} updated"
    if total_d > 0:
        duplicates = f"\n   * {total_d} duplicates skipped"
    if updated and duplicates:
        cand = ", and"
    if not updated and duplicates:
        band = ", and"
    if total_n == 0:
        total_n = "\n   * NO NEW references found in bibtex file"
    else:
        total_n = f"\n   * {total_n} new references added"
    click.echo(f"\n>>>> Out of total {total} references in:\n>>>> {bibtex_path}:{total_n}{band}{updated}{cand}{duplicates}\n")

def add_books(bibtex_path, calibre_directory):
    entries = process_bibtex(bibtex_path)
    run_calibre(entries, bibtex_path, calibre_directory)
