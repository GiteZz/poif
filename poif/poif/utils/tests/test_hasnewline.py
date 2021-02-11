from poif.utils import has_newline


def test_has_new_line():
    assert not has_newline("a")
    assert not has_newline("")
    assert not has_newline("Very long text")
    assert has_newline("\n")
    assert has_newline("qdsfkjqdfmklqdjf\n")
