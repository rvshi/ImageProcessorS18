from database import(
    add_user, get_user, delete_user, login_user
)

users = [
    ('me@harveyshi.com', 'bme590'),
    ('ed.l.1324@gmail.com', 'bme590'),
    ('mpalmeri00@gmail.com', 'bme590'),
    ('suyash@suyashkumar.com', 'bme590'),
    ('michellewei12345@gmail.com', 'bme590'),
]

for u in users:
    add_user(u[0], u[1])
