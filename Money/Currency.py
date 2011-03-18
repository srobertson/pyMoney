registry = {}
instances = {}

# TODO: Need to get rid of all these getInstance calls, we can use
# __new__ to achieve the same imutable cached effect

# TODO: Include an iso database of currencies

def getInstance(currencyCode):
    currencyCode = currencyCode.upper()
    if instances.has_key(currencyCode):
        return instances[currencyCode]

    if registry.has_key(currencyCode):
        args = registry[currencyCode]
        inst = Currency(currencyCode, *args)
        instances[currencyCode] = inst
        return inst

    raise ValueError, "Invalid Currency Code: '%s'." % currencyCode


def register(code, fractionDigits, defaultSymbol=None, localeSymbols={}):
    info = (fractionDigits, defaultSymbol, localeSymbols)
    registry[code] = info


class Currency(object):
    def __init__(self, code, fractionDigits, defaultSymbol=None, localeSymbols={}):
        self._code = code
        self._fractionDigits = fractionDigits
        self._defaultSymbol = defaultSymbol or code
        self._localeSymbols = localeSymbols

    def getCurrencyCode(self):
        return self._code

    def getSymbol(self, locale=None):
        if locale and self._localeSymbols.has_key(locale):
            return self._localeSymbols[locale]
        return self._defaultSymbol

    def getDefaultFractionDigits(self):
        return self._fractionDigits

    def __str__(self):
        return self._code

    def __eq__(self, other):
        if type(other) == type(self) and other.getCurrencyCode() == self._code:
            return True
        return False

    def __ne__(self, other):
	# not sure why this is neccary.. but my unpickle tests fail without it
	return not self.__eq__(other)


CurrencyType = type(Currency(None, None))

# Currency definitions
# Add new currency definitions as a tuple with
# the following elements:
# -String: The ISO 4217 Currency Code: http://www.bsi-global.com/Technical+Information/Publications/_Publications/tig90.xalter
# -Integer: Number of fractional digits
# -String(optional): The default Symbol
# -Dictionary(optional): A dictionary of locale to symbol mappings.
register('USD', 2, '$')      # United States
register('MXN', 2, '$')      # Mexico
