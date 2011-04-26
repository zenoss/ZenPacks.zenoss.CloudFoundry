class CollectedOrModeledMixin:
    def getFloatForValue(self, value):
        # Get the recent collected value if possible.
        r = self.cacheRRDValue(value, None)

        # Fall back to a modeled value if it exists.
        if r is None:
            r = getattr(self, 'modeled_{0}'.format(value), None)

        try:
            return float(r) if r is not None else None
        except TypeError, ex:
            import pdb; pdb.set_trace()
            raise ex

    def getIntForValue(self, value):
        r = self.getFloatForValue(value)
        try:
            return int(r) if r is not None else None
        except TypeError, ex:
            import pdb; pdb.set_trace()
            raise ex
        
    def getStringForValue(self, value, format='{0}'):
        r = self.getFloatForValue(value)
        if r is None:
            return ''

        return format.format(r)

def CollectedOrModeledProperty(propertyName):
    """
    This uses a closure to make using CollectedOrModeledMixin easier to use in
    infos.
    """
    def getter(self):
        return self._object.getIntForValue(propertyName)

    return property(getter)

