from ao3tagblockgenerator.cli import parse_tags, create_css_block


def test_parse_tags_basic():
    assert parse_tags("a,b,c") == ["a", "b", "c"]


def test_parse_tags_none_and_whitespace():
    assert parse_tags(None) == []
    assert parse_tags("  a , b , , c ") == ["a", "b", "c"]


def test_percent_encoding_and_space():
    assert parse_tags("tag one,tag two") == ["tag%20one", "tag%20two"]


def test_slash_and_ampersand_substitutions():
    # '/' becomes '*s*'
    assert parse_tags("tag/with/slash") == ["tag*s*with*s*slash"]
    # '&' becomes '*a*' but surrounding spaces remain percent-encoded
    assert parse_tags("a & b") == ["a%20*a*%20b"]


def test_dot_question_hash():
    # '.' becomes '*d*'
    assert parse_tags("a.b") == ["a*d*b"]
    # '?' becomes '*q*'
    assert parse_tags("what?") == ["what*q*"]
    # '#' becomes '*h*'
    assert parse_tags("tag#hash") == ["tag*h*hash"]


def test_parentheses_colon_at_preserved():
    # Parentheses are restored to literal '(' and ')'
    assert parse_tags("?(#)") == ["*q*(*h*)"]
    # Colon and at-sign are restored to their literal characters
    assert parse_tags("foo:bar") == ["foo:bar"]
    assert parse_tags("user@host") == ["user@host"]


def test_non_ascii_percent_encoded():
    # Non-ASCII characters are percent-encoded (UTF-8)
    out = parse_tags("café, 你好")
    # café -> caf%C3%A9, 你好 -> percent-encoded UTF-8 bytes
    assert out[0].lower().startswith("caf%")
    assert all(ch in "0123456789abcdef%" for ch in out[1].lower() if ch != '%') or out[1].startswith('%')


def test_create_css_block():
    tags = ["tag%20one", "tag%20two"]
    expected = (
        '.blurb:has(a[href$="/tags/tag%20one/works"]),\n'
        '.blurb:has(a[href$="/tags/tag%20two/works"]) {\n'
        '    display: none;\n'
        '}'
    )
    assert create_css_block(tags) == expected
