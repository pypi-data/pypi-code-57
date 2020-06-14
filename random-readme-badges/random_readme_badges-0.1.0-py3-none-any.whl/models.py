# -----------------------------------------------------------------------------
# Created: Sun 14 Jun 2020 17:03:38 IST
# Last-Updated: Sun 14 Jun 2020 17:06:06 IST
#
# models.py is part of random-readme-badges
# URL: https://gitlab.com/justinekizhak/random-readme-badges
# Description:
#
# Copyright (c) 2020, Justine Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "software"), to deal in the software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the software, and to permit
# persons to whom the software is furnished to do so, subject to the
# following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
# in no event shall the authors or copyright holders be liable for any claim,
# damages or other liability, whether in an action of contract, tort or
# otherwise, arising from, out of or in connection with the software or the
# use or other dealings in the software.
# -----------------------------------------------------------------------------


"""Models required for the app"""


badge_list = [
    "[![forthebadge](https://forthebadge.com/images/badges/60-percent-of-the-time-works-every-time.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/ages-12.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/ages-18.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/ages-20-30.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/approved-by-george-costanza.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/approved-by-veridian-dynamics.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/as-seen-on-tv.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-by-codebabes.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-by-crips.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-by-hipsters.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-by-neckbeards.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-with-grammas-recipe.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-with-grav.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-with-resentment.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/certified-cousin-terio.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/certified-elijah-wood.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/certified-snoop-lion.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/certified-steve-bruhle.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/certified-yourboyserge.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/compatibility-betamax.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/compatibility-club-penguin.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/compatibility-emacs.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/contains-technical-debt.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/designed-in-etch-a-sketch.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/designed-in-ms-paint.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/does-not-contain-msg.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/does-not-contain-treenuts.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/fo-real.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/fo-shizzle.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/fo-sho.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/for-sharks.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/fuck-it-ship-it.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/gluten-free.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/its-not-a-lie-if-you-believe-it.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/just-plain-nasty.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/kinda-sfw.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/mom-made-pizza-rolls.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/no-ragrets.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/not-an-issue.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/oooo-kill-em.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-case-western-reserve.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-comcast.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-electricity.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-jeffs-keyboard.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-netflix.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-oxygen.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-responsibility.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-water.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/powered-by-watergate.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/pretty-risque.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/reading-6th-grade-level.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/thats-how-they-get-you.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/uses-git.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/uses-h9rbs.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/winter-is-coming.svg)](https://forthebadge.com)",
    "[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)",
]
