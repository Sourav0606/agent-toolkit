from strings import slugify

def test_slugify_basic():
    assert slugify("Hello World") == "hello-world"

def test_slugify_punctuation_and_spacing():
    assert slugify("  Special @# Characters!!  ") == "special-characters"

def test_slugify_multiple_hyphens():
    assert slugify("one---two   three") == "one-two-three"
