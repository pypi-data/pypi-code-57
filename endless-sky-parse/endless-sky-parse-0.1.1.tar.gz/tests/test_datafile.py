import io
from endless_sky.datafile import DataFile


def test_filelike(caplog):
    datastream = io.StringIO(data)
    # caplog.set_level(logging.DEBUG)
    checknode(DataFile(datastream).root)


def test_listlike():
    checknode(DataFile(data.split("\n")).root)


def test_pathlike(tmp_path):
    f = tmp_path / "test-pathlike.txt"
    f.write_text(data)
    checknode(DataFile(f).root)


data = """
ship "Protector"
    sprite "ship/protector"
    thumbnail "thumbnail/protector"
    attributes
        category "Heavy Warship"
        "cost" 5500000
        "shields" 9500
        "hull" 6500
        "required crew" 30
        "bunks" 69
        "mass" 500
        "drag" 10.3
        "heat dissipation" .6
        "fuel capacity" 400
        "cargo space" 50
        "outfit space" 570
        "weapon capacity" 220
        "engine capacity" 100
        weapon
            "blast radius" 160
            "shield damage" 1600
            "hull damage" 800
            "hit force" 2400
    outfits
        "Sidewinder Missile Launcher" 2
        "Sidewinder Missile" 90
        "Quad Blaster Turret" 4
        "Heavy Anti-Missile Turret" 2
        
        "Fusion Reactor"
        "LP288a Battery Pack"
        "D67-TM Shield Generator"
        "Small Radar Jammer" 3
        "Liquid Nitrogen Cooler"
        "Laser Rifle" 6
        
        "X3700 Ion Thruster"
        "X3200 Ion Steering"
        "Hyperdrive"
        
    engine -11 125
    engine 11 125
    gun -15 -100 "Sidewinder Missile Launcher"
    gun 15 -100 "Sidewinder Missile Launcher"
    turret -54 -54 "Quad Blaster Turret"
    turret 54 -54 "Quad Blaster Turret"
    turret -73 0 "Heavy Anti-Missile Turret"
    turret 73 0 "Heavy Anti-Missile Turret"
    turret -54 54 "Quad Blaster Turret"
    turret 54 54 "Quad Blaster Turret"
    leak "leak" 60 50
    leak "flame" 20 80
    explode "tiny explosion" 18
    explode "small explosion" 36
    explode "medium explosion" 24
    explode "large explosion" 8
    "final explode" "final explosion large"
    description `Voted the "ugliest ship in the sky" by Stars and Starships Magazine, the Protector is a typical example of brutally efficient Syndicate engineering. It is basically nothing more than six turrets attached to a set of engines and crew's quarters, designed as a defense platform that can accompany merchant convoys.`



ship "Quicksilver"
    sprite "ship/quicksilver"
    thumbnail "thumbnail/quicksilver"
    attributes
        category "Light Warship"
        "cost" 1090000
        "shields" 3000
        "hull" 800
        "required crew" 3
        "bunks" 6
        "mass" 120
        "drag" 2.7
        "heat dissipation" .8
        "fuel capacity" 400
        "cargo space" 10
        "outfit space" 240
        "weapon capacity" 60
        "engine capacity" 70
        weapon
            "blast radius" 40
            "shield damage" 400
            "hull damage" 200
            "hit force" 600
    outfits
        "Particle Cannon" 2
        
        "RT-I Radiothermal"
        "LP036a Battery Pack"
        "D23-QP Shield Generator"
        "Cooling Ducts"
        
        "Greyhound Plasma Thruster"
        "Greyhound Plasma Steering"
        "Hyperdrive"
        
    engine -17 54
    engine 17 54
    gun -6 -38 "Particle Cannon"
    gun 6 -38 "Particle Cannon"
    leak "leak" 50 50
    explode "tiny explosion" 12
    explode "small explosion" 16
    "final explode" "final explosion small"
    description "The Megaparsec Quicksilver is a warship built around a single concept: to design the smallest and fastest ship capable of carrying two particle cannons. Because of its speed and long weapons range, the Quicksilver can keep a safe distance from most targets and bombard them with particle bursts until they are destroyed."
"""


def checknode(n):
    assert n.children[0].tokens == ["ship", "Protector"]
    assert n.children[0].children[2].children[0].tokens == ["category", "Heavy Warship"]
    assert (
        next(n.children[0].filter_first("description"))
        .tokens[1]
        .startswith('Voted the "ugliest ship in the sky" by')
    )
    assert len(list(n.children[0].filter_first("turret"))) == 6
    assert n.children[1].tokens == ["ship", "Quicksilver"]
