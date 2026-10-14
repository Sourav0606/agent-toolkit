from formatter import TextFormatter


def test_format_title_capitalized():
    fmt = TextFormatter(prefix="[Article] ")
    # Expected title-cased words
    res = fmt.format_title("hello world of agents")
    assert res == "[Article] Hello World Of Agents"
