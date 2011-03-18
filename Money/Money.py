from Currency import Currency, getInstance

class Money(object):
    """Money objects represent money in various currency.

    They support methods for testing a money's currency, formating
    them for display, converting them to and from different currencies
    as well as provide methods to preform mathmatical operations on
    them such as edistribute money between multiple partners without
    rounding errors.

    Creating Money obects
    
    You can instantiate a money with a string
    >>> Money('$1.00 USD')
    Money('$1.00', 'USD')

    >>> Money(-100)
    Money('($100.00)', 'USD')

    Or a unicode object
    >>> Money(u'$200,000.00 USD')
    Money('$200,000.00', 'USD')

    Or you can specify a float and a currency
    >>> Money(3.0, 'USD')
    Money('$3.00', 'USD')
    
    Or a string and a currency
    >>> Money('3.00', 'USD')
    Money('$3.00', 'USD')

    However specifing a string with the currency code in the ammount
    as well as the ammount will raise a ValueError

    >>> Money('$1.50 USD', 'USD')
    Traceback (most recent call last):
    ...
    ValueError: Currency specified twice.

    If you don't specify the currency, Money should default to the
    currency of the region that the computer is using. We haven't
    implemented this yet so for now currency defaults to USD
    >>> Money('.45')
    Money('$0.45', 'USD')

    >>> Money(.3)
    Money('$0.30', 'USD')

    >>> Money(-1)
    Money('$-1.00', 'USD')

    Instantiating a money object from another Money object
    >>> Money(Money(300))
    Money('$300.00', 'USD')
    
    Money objects also implement the Null object pattern. Which is
    useful if you want to represent that the Value is unkown.

    >>> Money(None)
    Money(None)

    >>> Money('')
    Money(None)

    >> Money('       ')
    Money(None)

    Money Operations
    
    Money objects support the basic math operations:

    >>> m1 = Money('$1 USD')
    >>> m2 = Money('$2 USD')
    >>> noneMoney = Money(None)

    Addition between two money values
    >>> m1 + m2
    Money('$3.00', 'USD')

    >>> m2 - m1
    Money('$1.00', 'USD')

    Money objecs can be compared to primitive numbers, it's assumed
    that their currencies are the same.

    >>> Money(1) + 1
    Money('$2.00', 'USD')
    >>> 1 + Money(1) 
    Money('$2.00', 'USD')

    >>> Money("$100") + 0
    Money("$100.00", "USD")

    >>> 0 + Money("$100")
    Money("$100.00", "USD")

    >>> Money("$100") - 0
    Money("$100.00", "USD")

    >>> 0 - Money("$100")
    Money("($100.00)", "USD")
    



    >>> Money(1) == 1
    True

    >>> 1 == Money(1)
    True

    >>> l = map(Money, [1, '2.0', 3])
    >>> sum(l)
    Money('$6.00', 'USD')


    """

    
    cents = [1, 10, 100, 1000]
    # Money's are imutable objects, we cache a few 
    NoneMoney=None

    def __new__(cls, amount=None, currency=None):
        
        if isinstance(amount, basestring):
            amount = amount.strip()
            if amount != '':
                parts = amount.split()
                amount = parts[0]
                if len(parts) == 2:
                    if currency is not None:
                        raise ValueError("Currency specified twice.")
                    currency = parts[1]

        if amount is None or amount == '':
            # asking for the null object
            if cls.NoneMoney is None:
                cls.NoneMoney = object.__new__(cls)
                cls.NoneMoney._amount = None
                cls.NoneMoney._currency = None
                cls.NoneMoney._isNone = True
            return cls.NoneMoney
        
        # Try several different ways to parse the data that we got.
        if currency is not None and currency != '':
            # We got a currency passed into us.
            if isinstance(currency, basestring):
                currency = getInstance(currency)
            elif type(currency) != Currency:
                raise TypeError, "Invalid Currency type."
        else:
            # Default to USD
            currency = getInstance('USD')

        # Now that we have the currency we can remove the currency
        # symbol such as the $ form the begining if ammount is a string

        if isinstance(amount, basestring):
            amount = amount.split(currency.getSymbol())[-1]
            amount = float(amount.replace(',',''))        


        # now we can make a new money object
        obj = object.__new__(cls)
        obj._currency = currency
        obj._amount = long(round(amount * obj._centFactor()))
        obj._isNone = False
        return obj
        
##    def __init__(self, amount=None, currency=None):
##        """
##        Both arguments are actually required. An instance should
##        never be created without passing both.  They are only
##        optional so internal functions can create instances
##        and then call _setState.

##        amount: a numeric value
##        currency: an instance of Currency.Currency
##        """

##        self._currency = currency
##        if amount is not None:
##            self._amount = long(round(amount * self._centFactor()))
##        else:
##            self._amount = amount

    def isNone(self):
        return self._isNone

    def _centFactor(self):
        # Other functions should be sure to not call this function if
        # we are a "Null Money" placeholder.
        return self.cents[self._currency.getDefaultFractionDigits()]

    def getCurrency(self):
        return self._currency
    currency = property(getCurrency, None, None, "")

    def getCurrencyCode(self):
        if self.amount is not None:
            return self._currency.getCurrencyCode()
        else:
            return ''
            raise TypeError, "Can't get currency information for Null Money object."

    def getAmount(self):
        if self.amount is not None:
            return float(self._amount) / self._centFactor()
        else:
            return 0.0

    def getUnformattedAmount(self):
        """
        Returns the amount as a string with XX decimal places.
        Doesn't include commas or currency signs
        """
        if self.amount is not None:
            digits = self._currency.getDefaultFractionDigits()
            fmt = "%%.%sf" % digits
            return fmt % (float(self._amount) / self.cents[digits])
        else:
            return ''
        
    def _get_amount(self):
        return self._amount
    amount = property(_get_amount, None, None, "")

    def allocate(self, ratios):
        if self._amount is None:
            raise TypeError, "Can't call allocate on a Null Money object."
        
        if type(ratios) == list:
            total = 0
            for ratio in ratios:
                total += ratio

            # If all ratios are 0, return $0 for everyone.
            if not total:
                return [self.newMoney(x) for x in ratios]
                
            remainder = self._amount
            results = []
            for ratio in ratios:
                result = (self.newMoney(self._amount * ratio / total))
                remainder -= result.amount
                results.append(result)

            for i in range(remainder):
                results[i]._amount += 1

            return results
        elif type(ratios) == int:
            lowResult = self.newMoney(self._amount / ratios)
            highResult = self.newMoney(lowResult._amount + 1)
            results = []

            remainder = int(self.amount % ratios)
            for i in range(remainder):
                results.append(highResult)

            for i in range(ratios - remainder):
                results.append(lowResult)

            return results


    def __hash__(self):
        return hash((self.amount, self.currency))

    def __eq__(self, other):
	try:
	    other = self._compareTypes(other)
	except Exception, e:
	    print e
	    # couldn't coerce the other object
	    return False
        if other.currency == self._currency and \
		other.amount == self._amount:
            return True

        return False

    def __ne__(self, other):
        if isinstance(other, Money) and \
           other.currency == self._currency and \
           other.amount == self._amount:
            return False

        return True


    def _compareTypes(self, other):
	 # I suppose we should be able to use __coerce__ for this but, it doesn't want to work for me so...

        if not isinstance(other, Money):
	    # try to convert other to a money so we can compare apples to apples
            other = Money(other)

        # OK, we're both money types.  Let's see if either one of us
        # is a None Money type (ie. a placeholder type for a money
        # with no set value.)
        if self.amount is None or other.amount is None:
            # Yup...so don't bother checking currency.  The calling
            # function should do the right thing.
            return other
        
        if other.currency != self._currency:
            raise TypeError, "Can't use currency: %s with currency: %s" % (other.currency.getCurrencyCode(), self._currency.getCurrencyCode())
	return other


    def isEmpty(self):
        if self._amount is None:
            return True
        else:
            return False
            
    def newMoney(self, amount):
        return self.__copy(amount, self._currency)
        
        #m._setState(amount, self._currency)
        return m

    def __add__(self, other):
        other = self._compareTypes(other)

        if other.amount is None and self.amount is None:
            return Money(None, None)
        elif other.amount is None:
            return self.newMoney(self.amount)
        elif self.amount is None:
            return other.newMoney(other.amount)
            
        return self.newMoney(other.amount + self._amount)

    __radd__ = __add__

    def __sub__(self, other):
        other = self._compareTypes(other)

        if other.amount is None and self.amount is None:
            return Money(None, None)
        elif other.amount is None:
            return self.newMoney(self._amount)
        elif self.amount is None:
            return other.newMoney(- other.amount)
        
        return self.newMoney(self._amount - other.amount)
    __rsub__ = __sub__
    
    def __mul__(self, amount):
        if self.amount is None:
            raise TypeError, "Cannot multiply placeholder Money value of None."
        amt = self.getAmount() * amount
        return Money(amt, self._currency)

    __rmul__ = __mul__
    
    def __div__(self, amount):
	#other = self._compareTypes(other)

        if self.amount is None:
            raise TypeError, "Cannot divide placeholder Money value of None."
        amt = self.getAmount() / amount
        return Money(amt, self._currency)

    __rdiv__ = __div__

    def __cmp__(self, other):
        other = self._compareTypes(other)
        if self._amount < other.amount:
            return -1
        if self._amount == other.amount:
            return 0
        return 1

    def __str__(self):
        if self.isNone():
            return ''
        
        #import pdb; pdb.set_trace()
        amt = float(self._amount) / self._centFactor()
        digits = self._currency.getDefaultFractionDigits()
        fmt = "%%.%sf" % digits
        amt = fmt % amt
        # Add commas
        wholeNumbers, fractional = amt[:- (digits +1)], amt[-(digits+1):]
        commas = (len(wholeNumbers)-1)/3
        wholeNumbers = list(wholeNumbers)
        for i in range(0, commas):
            wholeNumbers.insert(len(wholeNumbers) - (3 * (i+1)) - i, ',')
        ret = "%s%s%s" % (self._currency.getSymbol(), ''.join(wholeNumbers), fractional)
            
        #ret = "%s%.2f" % (self._currency.getSymbol(), amt)
        return ret
    def __repr__(self):
        if self.isNone():
            return "Money(None)"
        else:
            return "Money(%s, %s)" % (repr(str(self)), repr(str(self.getCurrency()))) 

    
    def __float__(self):
        return self.getAmount()
    


    def lower(self):
        # Nasty hack to make our lives easier when sorting trees.  Get rid of
        # this at some point!
        return self

    def __copy(self, amount, currency):
        if amount is None and currency is None:
            # Bypass this copy method to return the None money object
            return Money(amount, currency)
        
        class Empty(self.__class__):
            def __new__(cls):return object.__new__(cls)
            def __init__(self): pass
        newcopy = Empty( )
        newcopy.__class__ = self.__class__
        newcopy._amount = amount
        newcopy._currency = currency
        newcopy._isNone = False
        return newcopy

