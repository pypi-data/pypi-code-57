from __future__ import absolute_import, unicode_literals

import pytest

from virtualenv.activation import FishActivator
from virtualenv.info import IS_WIN


@pytest.mark.skipif(IS_WIN, reason="we have not setup fish in CI yet")
def test_fish(activation_tester_class, activation_tester, monkeypatch, tmp_path):
    monkeypatch.setenv(str("HOME"), str(tmp_path))
    fish_conf_dir = tmp_path / ".config" / "fish"
    fish_conf_dir.mkdir(parents=True)
    (fish_conf_dir / "config.fish").write_text("")

    class Fish(activation_tester_class):
        def __init__(self, session):
            super(Fish, self).__init__(FishActivator, session, "fish", "activate.fish", "fish")

    activation_tester(Fish)
