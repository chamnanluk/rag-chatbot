from app.utils.token_utils import approximate_token_count


def test_approximate_token_count() -> None:
    text = "abcd" * 10
    assert approximate_token_count(text) == 10
