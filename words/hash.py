import random
import hashlib

def gen_hash(user_id, length=None):

    hash = hashlib.sha1()
    hash.update("%s@@@%s" % (str(user_id), str(time.time())))
    if length is None:
        return hash.hexdigest()[-10:]
    else:
        return hash.hexdigest()[-length:]


def gen_unique_hash(model_class, length):
    id = model_class.objects.count()
    unique_hash = gen_hash(id, length)
    while model_class.objects.filter(hash=unique_hash).exists():
        id += random.randint(1, sys.maxint)
        unique_hash = gen_hash(id, length)
    return unique_hash
