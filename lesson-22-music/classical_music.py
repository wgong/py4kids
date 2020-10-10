# use full-name to lookup Wikiwand
name_map = {
    'Strauss I': 'Johann Strauss I',
    'Mozart': 'Wolfgang Amadeus Mozart',
    'Vivaldi': 'Antonio Vivaldi',
    'Mendelssohn': 'Felix Mendelssohn',
    'Tchaikovsky': 'Piotr Ilyich Tchaikovsky',
    'Tchaikovsy': 'Piotr Ilyich Tchaikovsky',
    'Tchaikowsky': 'Piotr Ilyich Tchaikovsky',
    'Strauss II': 'Johann Strauss II',
    'Bach': 'Johann Sebastian Bach',
    'Bizet': 'George Bizet',
    'Beethoven': 'Ludwig van Beethoven',
    'Grieg': 'Edvard Grieg',
    'Barber': 'Samuel Barber',
    'Haydn': 'Joseph Haydn',
    'Sibelius': 'Jean Sibelius',
    'Dvorak': 'Antonín Dvořák',
    'Brahms': 'Johannes Brahms',
    'Prokofiev': 'Sergei Prokofiev',
    'Schubert': 'Franz Schubert',
    'Puccini': 'Giacomo Puccini',
    'Rossini': 'Gioachino Rossini',
    'Verdi': 'Giuseppe Verdi',
    "Telemann": "Georg Philipp Telemann",
    "Corelli": "Arcangelo Corelli",
    "Afternova": "Fred Buscaglione",
    "Chopin": "Frédéric Chopin",
    "Debussy": "Claude Debussy",
    "Liszt": "Franz Liszt",
    "Schubert-Liszt": "Franz Liszt",
    "Litvinovsky": "Alexander Litvinovsky",
    "Morricone": "Ennio Morricone",
    "Piazzolla": "Astor Piazzolla",
    "Rachmaninoff": "Sergei Rachmaninoff",
    "Rosetti": "Antonio Rosetti",
    "Saint-Saëns": "Camille Saint-Saëns",
    "Satie": "Erik Satie",
    "Schumann": "Robert Schumann",
    "Scriabin": "Alexander Scriabin",
}

def ts2sec(ts):
    tmp = ts.split(":")
    if len(tmp) >= 3:
        sec = 60*60*int(tmp[0]) + 60*int(tmp[1]) + int(tmp[2])
    elif len(tmp) == 2:
        sec = 60*int(tmp[0]) + int(tmp[1])
    else:
        sec = int(tmp[0])
    return sec
        
def make_youtube_url_with_ts(vid, ts):
    sec = ts2sec(ts)
    # https://www.youtube.com/watch?v=i0b29lAuMlg&t=2501s
    return f"https://www.youtube.com/watch?v={vid}&t={sec}s"


def make_wikiwand_url(name):
    nm = "_".join([i.strip() for i in name.split(" ") if i.strip()])
    return f"https://www.wikiwand.com/en/{nm}"

def make_youtube_link(vid, ts):
    youtube_url = make_youtube_url_with_ts(vid, ts)
    ts = "00:"+ts if len(ts) < 8 else ts
    return f"""<a href={youtube_url}>{ts}</a>"""

def make_wikiwand_link(name):
    wiki_url = make_wikiwand_url(name)
    return f"""<a href={wiki_url}>{name}</a>"""


def parse_file_txt(file_txt, meta_marker="## YouTube metadata", desc_marker="## YouTube description"):
    with open(file_txt) as f:
        lines = f.read().split("\n")

    if lines[0].strip() != meta_marker:
        raise ValueError(f"{file_txt} missing YouTube metadata")

    b_has_data = False
    for n, line in enumerate(lines):
        if line.strip() == desc_marker:
            b_has_data = True
            break

    meta_map = {}
    metalines = lines[1:n]
    for m in metalines:
        if not m.strip():
            continue
        tmp = m.split(":")
        meta_map[tmp[0].strip()] = (":".join(tmp[1:])).strip()

    lines = lines[n+1:]
    if not b_has_data or len(lines) < 1:
        raise ValueError(f"{file_txt} missing YouTube description")
        
    return meta_map, lines