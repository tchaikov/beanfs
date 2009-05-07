import logging

def exists_by_property(model, prop, value):
    records = model.all().filter('%s = ' % prop, value)
    logging.debug('%d entries found with %s = %r' % (records.count(), prop, value))
    return records.count() > 0


def get1_by_property(model, prop, value):
    records = model.all().filter('%s = ' % prop, value)

    if records.count() == 1:
        return records[0]
    elif records.count() == 0:
        return None
    else:
        assert 0, "%s has multiple records with %s=%s\n" % (model, prop, value)


def find(pred, seq, ret=None):
    """
    Return first item in sequence where pred(item) is True.
    """
    for item in seq:
        if pred(item):
            return item

    
