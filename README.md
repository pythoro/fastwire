# fastwire

Fastwire is a simple package to facilitate communication between objects. It provides similar functionality to Blinker, but uses some newer Python features. It uses an Inversion-of-Control and Dependency injection to help keep code simple.

## Basic usage

Create a signal container:


```python

import fastwire

sc = fastwire.SignalContainer()
```

Then create a signal...

```python
signal = sc.signal('your_name')
```

We can connect to that signal like this:

```python
class A():
    def __init__(self):
    signal.connect(self.connected)

    def connected(self, a):
        print('Class A instance received a: ' + str(a))

a = B()
signal.connect(a.connected)	
signal.emit(a=5.7)
# Class A instance received a 5.7
```

And we can connect other signals if we want to:

```python
signal_b = sc.signal('new_sig')
signal_b.connect(a.connected)
signal_b.emit(a=3)
# Class A instance received a 5.7
```

Connecting also works with functions. We can connect a function to the same
signal.

```python
def test_fun(a):
    print('test_fun got a ' + str(a))
    
signal.connect(test_fun)
signal.emit(a=5.7)
# Class A instance received a 5.7
# test_fun got a 5.7
```

Only keyword arguments are accepted to ensure the required type of data is 
passed.


The emit method doesn't return anything. But the signal.fetch method does. It
requires there to be a single function or method that 'supplies' the return
value. The signal.fetch_all method returns a list of return values from
all receivers.

## Decorators

It can be convenient to use decorators to automatically connect. Do do this,
the class needs to inherit fastwire.Wired.

```python
signal_c = sc.signal('C')

class B(fastwire.Wired):
	@fastwire.receives(signal_c)
	def connected(self, a):
		print('Class B instance got ' + str(a))

b = B()
signal_c.emit(a=7)
# Class B instance got 7
```

Functions need to use a different decorator.

```python
@fastwire.fn_receives(signal_c)
def test_fun_2(a):
    print('test_fun_2 got ' + str(a))
signal_c.emit(a=88)
# Class B instance got 88
# test_fun_2 got 88
```

Use the @fastwire.supply decorator for methods that supply data,
and the @fastwire.fn_supply decorator for functions that supply data.


## Conditions

Conditions can be added. They need to have a method called 'check', which is
passed combined keyword arguments from the caller and receiver. It needs to
return a boolean. If it's true, the given receiver gets the signal, if not,
it doesn't. They also need a class attribute called 'name'.

Add a signal condition like this:

```python

class My_Condition():
    name = 'default'
    def check(self, a, **kwargs):
        ''' The main check call - must return a boolean '''
        if a < 10:
            return True
        else:
            return False
            
signal.add_condition(My_Condition())
```

Now, receivers only get the signal when a is less than 10:

```python
signal.emit(a=5.7)
# Class A instance received a 5.7
# test_fun got a 5.7

signal.emit(a=15)
# Nothing happens
```

Condition classes are completely open - they can be as simple as the above
example or as complex as a state machine.