# coding: utf-8


class DatabaseRouter(object):
    def db_for_read(self, model, **hints):
        database = getattr(model, "_database", None)
        if database:
            return database
        else:
            return "default"

    def db_for_write(self, model, **hints):
        database = getattr(model, "_database", None)
        if database:
            return database
        else:
            return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the master/slave pool.
        """
        return True

    def allow_migrate(self, db, model):
        """
        All non-auth models end up in this pool.
        """
        return True
