from passlib.hash import bcrypt

def hash_password(password):
    return bcrypt.hash(password)

def check_password(password_input, hash):
    """
    Checks if input hashes into the hash given
    :param password_input: password from user
    :param hash: the hash to be tested against
    :type password_input: str
    :type hash: str
    :rtype bool
    """
    return bcrypt.verify(password_input, hash)