user_db: dict = {
    'text': {}
}

users: dict[int, dict] = {}   # {message.from_user.id: {'utc': int, 'text': list}}