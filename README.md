# fastwire

Fastwire is a simple package to facilitate communication between objects. It
provides similar functionality to several other packages, such as:
 
* blinker
* wires
* wired
* observable
* pyDispatcher
* pymitter
* py-notify
* zope-event

Fastwire is intended to be elegant to use, fast to implement, and more
flexible, while maintianing high performance.

## Basic usage

Create a signal container:


```python

import fastwire as fw

sc = fw.SignalContainer()
```

Then create a signal...

```python
signal = sc.signal('your_name')
```

Note that we always get the same object for the same name from the container:


```python
same_signal = sc.signal('your_name')
signal is same_signal
# True
```


We can connect to that signal like this:

```python
class A():
    def __init__(self):
        signal.connect(self.connected)

    def connected(self, a):
        print('Class A instance received a: ' + str(a))

a = A()
connection_id1 = signal.connect(a.connected)	
signal.emit(a=5.7)
# Class A instance received a 5.7
```

The emit method doesn't return anything. 
We can connect other signals if we want to:

```python
signal_b = sc.signal('new_sig')
signal_b.connect(a.connected)
signal_b.emit(a=3)
# Class A instance received a 3
```

Connecting also works with functions. We can connect a function to the same
signal.

```python
def test_fun(a):
    print('test_fun got a ' + str(a))
    
connection_id2 = signal.connect(test_fun)
signal.emit(a=5.7)
# Class A instance received a 5.7
# test_fun got a 5.7
```

Only keyword arguments are accepted to ensure the data is passed cleanly.

We can remove connections based on the ID that gets passed back from the
connect function.

```python
signal.disconnect(connection_id1)
signal.emit(a=5.7)
# test_fun got a 5.7

signal.receivers()
[<function __main__.test_fun(a)>]
```

We can reset signals like this:

```python
signal.reset()
signal.receivers_present
# False
```

## Signal properties

### signal.n
Number of recievers.

### signal.receivers_present
True if receivers are present.

### name
The name of the signal.

## Decorators

It can be convenient to use decorators to automatically connect. Do do this,
the class needs to inherit fw.Wired.

```python
signal_c = sc.signal('C')

class B(fw.Wired):
	@fw.receive(signal_c)
	def connected(self, a):
		print('Class B instance got ' + str(a))

b = B()
signal_c.emit(a=7)
# Class B instance got 7
```

Functions need to use a different decorator.

```python
@fw.fn_receive(signal_c)
def test_fun_2(a):
    print('test_fun_2 got ' + str(a))
signal_c.emit(a=88)
# Class B instance got 88
# test_fun_2 got 88
```

## Fetching data

The signal.emit method does not return anything, but the signal.fetch method
does. The required functions or methods are assumed to 'supply' return
values, rather than simply recieve data. 

The return values are collected into a list.

```python
supply_signal = sc.signal('D')
def test_fun_3():
    return 'return value from test_fun_3'
    
def test_fun_4():
    return 'return value from test_fun_4'
    
supply_signal.connect(test_fun_3)
supply_signal.connect(test_fun_4)
supply_signal.fetch_all()
# ['return value from test_fun_3', 'return value from test_fun_4']
```

Decorators can also be used to supply data.
Use the @fastwire.supply decorator for methods that supply data,
and the @fastwire.fn_supply decorator for functions that supply data.
These methods or functions can take arguments passed using the fetch_all 
method.

```python
supply_signal2 = sc.signal('D2')
def test_fun_6(a):
    return a / 2
    
def test_fun_7(a):
    return a * 2
    
supply_signal2.connect(test_fun_6)
supply_signal2.connect(test_fun_7)
supply_signal2.fetch_all(a=5)
# [2.5, 10]
```

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

To remove:

```python
signal.remove_condition(My_Condition.name)
signal.emit(a=15)
# Class A instance received a 15
# test_fun got a 15
```

Condition classes are completely open - they can be as simple as the above
example or as complex as a state machine.

## Muting

No receivers get a muted signal. You can mute and unmute a signal easily...

```python
signal.mute()
signal.emit(a=3)
# Nothing mappens

signal.unmute()
signal.emit(a=3)
# Class A instance received a 3
# test_fun got a 3
```

## Wires

Wires work like signals, except they are designed to have only one supplier.
Unlike signals, they are designed to be used with a 'fetch' method.

```python
wc = fw.WireContainer()
wire_a = wc.wire('A')
def test_fun_5():
    return 'return value from test_fun_5'

wire_a.connect(test_fun_5)
wire_a.fetch()
# 'return value from test_fun_5'
```

Under the hood, fetch does the same thing as emit, but it passes on the 
return value from the connected method or function.

```python
wire_a.emit()
# 'return value from test_fun_5'
```

Like signals, decorators can be used.


```python
wire_b = wc.wire('B')

class D(fw.Wired):
	@fw.supply(wire_b)
	def supply_fun(self):
		return "supplied data from class D instance"

d = D()
wire_b.fetch()
# "supplied data from class D instance"
```

Functions need to use a different decorator.

```python
wire_c = wc.wire('C')

@fw.fn_supply(wire_c)
def test_fun_2():
    return 67
wire_c.fetch()
# 67
```

Note that wires cannot have more than one supplier.


## Documentation

Documentation is hosted at ReadTheDocs.org.

https://fastwire.readthedocs.io/en/latest/