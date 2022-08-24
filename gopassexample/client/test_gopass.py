from multipass import Multipass

from . import GoPass

gobo_secret = (
    "TMx64BCXZZmzBHeBeFsXkRbBokR5522Qj8RgtF2jodwgp2ZNjZwfwkykkJoSZVFg"
    "giGxyTwwLRnp2sXyp3fzuPVjSq34ZtE28NpCw7NNsHXtFgxqYoT6BGyTrWxxfFMm"
)
gopass = GoPass(gobo_secret)

user_id = "141fcdfe-dce9-4d54-b74c-88ea2730bc2d"
remote_ip = "127.0.0.1"
data = {
    "user_id": user_id,
    "remote_ip": remote_ip,
}


def test_gopass():
    token = gopass.generate_token(data)

    message = gopass.parse_token(token)
    assert user_id == message["user_id"]
    assert remote_ip == message["remote_ip"]


def test_gopass_third_party():
    multipass = Multipass(gobo_secret)
    token = multipass.generateToken(data)

    message = gopass.parse_token(token)
    assert user_id == message["user_id"]
    assert remote_ip == message["remote_ip"]
