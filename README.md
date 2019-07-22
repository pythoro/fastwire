# fastwire

Fastwire is a simple package to facilitate communication between objects. It provides similar functionality to Blinker, but uses some newer Python features. It uses an Inversion-of-Control and Dependency injection to help keep code simple.

## Basic usage

It's recommended to use the decorator to connect signals, like this.

```python

import fastwire

sc = fastwire.SignalContainer()
signal = sc.signal()

class A():
	@fastwire.connect_to(signal)
	def connected(self, a):
		print(a)

a = A()		
signal.emit(a=5.7) # Prints 5.7

```

Alternatively, connect manually:


```python

import fastwire

sc = fastwire.SignalContainer()
signal = sc.signal()

class B():
	def connected(self, a):
		print(a)

a = B()
signal.connect(a.connected)	
signal.emit(a=5.7) # Prints 5.7

```