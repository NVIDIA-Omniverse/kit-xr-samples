import pathlib


def test_clang_format_top_level_keys_no_trailing_space():
    repo = pathlib.Path(__file__).resolve().parent.parent
    clang_format = repo / '.clang-format'
    assert clang_format.exists()

    for line in clang_format.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        # Top-level keys are not indented; indented lines belong to lists like IncludeCategories.
        if not line.startswith(' '):
            key, _sep = line.split(':', 1)
            assert not key.endswith(' '), (
                f"Top-level option key has trailing space before colon: {key!r}"
            )
