from invoke import Collection

from tasks import test


ns = Collection()
ns.add_collection(test)
