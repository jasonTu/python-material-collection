
## Do This, Then That: else Blocks Beyond if
This is no secret, but it is an underappreciated language feature: the else clause can be used not only in if statements but also in for, while, and try statements.

The semantics of for/else, while/else, and try/else are closely related, but very different from if/else. Initially the word else actually hindered my understanding of these features, but eventually I got used to it.

Here are the rules:
* for

The else block will run only if and when the for loop runs to completion (i.e., not if the for is aborted with a break).

* while

The else block will run only if and when the while loop exits because the condition became falsy (i.e., not when the while is aborted with a break).
* try

The else block will only run if no exception is raised in the try block. The official docs also state: “Exceptions in the else clause are not handled by the preceding except clauses.”

In all cases, the else clause is also skipped if an exception or a return, break, or continue statement causes control to jump out of the main block of the compound statement.

```python
for item in my_list:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('No banana flavor found!')
```

In the case of try/except blocks, else may seem redundant at first. After all, the after_call() in the following snippet will run only if the dangerous_call() does not raise an exception, correct?

```python
try:
    dangerous_call()
    after_call()
except OSError:
    log('OSError...')
```

However, doing so puts the after_call() inside the try block for no good reason. For clarity and correctness, the body of a try block should only have the statements that may generate the expected exceptions. This is much better:

```python
try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()
```

## Context Managers and with Blocks
Context manager objects exist to control a with statement, just like iterators exist to control a for statement.

The with statement was designed to simplify the try/finally pattern, which guarantees that some operation is performed after a block of code, even if the block is aborted because of an exception, a return or sys.exit() call. The code in the finally clause usually releases a critical resource or restores some previous state that was temporarily changed.

The context manager protocol consists of the \__enter__ and \__exit__ methods. At the start of the with, \__enter__ is invoked on the context manager object. The role of the finally clause is played by a call to \__exit__ on the context manager object at the end of the with block.

The most common example is making sure a file object is closed. See Example 15-1 for a detailed demonstration of using with to close a file.


```python
# Example 15-1: Demonstration of a file object as a context manager
with open('chapter15/mirror.py') as fp:
    src = fp.read(60)
```


```python
len(src)
```




    3




```python
fp
```




    <_io.TextIOWrapper name='chapter15/mirror.py' mode='r' encoding='UTF-8'>




```python
fp.closed, fp.encoding
```




    (True, 'UTF-8')




```python
fp.read()
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-5-5b707e20d623> in <module>()
    ----> 1 fp.read()
    

    ValueError: I/O operation on closed file.


The as clause of the with statement is optional. In the case of open, you’ll always need it to get a reference to the file, but some context managers return None because they have no useful object to give back to the user.


```python
# Example 15-3: code for the LookingGlass context manager class
class LookingGlass:
    
    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JASONTU'
    
    def reverse_write(self, text):
        self.original_write(text[::-1])
    
    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True
```

The interpreter calls the \__enter__ method with no arguments—beyond the implicit self. The three arguments passed to \__exit__ are:
* exc_type

The exception class (e.g., ZeroDivisionError).

* exc_value

The exception instance. Sometimes, parameters passed to the exception construc‐ tor—such as the error message—can be found in exc_value.args.

* traceback

A traceback object.


```python
# Example 15-2: Test driving the LookingGlass context manager class
with LookingGlass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)
```

    pordwonS dna yttiK ,ecilA
    UTNOSAJ



```python
what
```




    'JASONTU'




```python
print('Back to normal')
```

    Back to normal



```python
with LookingGlass() as what:
    1/0
```

    Please DO NOT divide by zero!



```python
what
```




    'JASONTU'



## The contextlib Utilities
Before rolling your own context manager classes, take a look at “29.6 contextlib — Utilities for with-statement contexts” in The Python Standard Library. Besides the al‐ ready mentioned redirect_stdout, the contextlib module includes classes and other functions that are more widely applicable:

* closing

A function to build context managers out of objects that provide a close() method but don’t implement the \__enter__/\__exit__ protocol.

* suppress

A context manager to temporarily ignore specified exceptions.

* @contextmanager

A decorator that lets you build a context manager from a simple generator function, instead of creating a class and implementing the protocol.

* ContextDecorator

A base class for defining class-based context managers that can also be used as function decorators, running the entire function within a managed context.

* ExitStack

A context manager that lets you enter a variable number of context managers. When the with block ends, ExitStack calls the stacked context managers’ \__exit__ methods in LIFO order (last entered, first exited). Use this class when you don’t know beforehand how many context managers you need to enter in your with block; for example, when opening all files from an arbitrary list of files at the same time.

The most widely used of these utilities is surely the @contextmanager decorator, so it deserves more attention. That decorator is also intriguing because it shows a use for the yield statement unrelated to iteration. This paves the way to the concept of a coroutine, the theme of the next chapter.

## Using @contextmanager
The @contextmanager decorator reduces the boilerplate of creating a context manager: instead of writing a whole class with \__enter__/\__exit__ methods, you just implement a generator with a single yield that should produce whatever you want the \__enter__ method to return.

In a generator decorated with @contextmanager, yield is used to split the body of the function in two parts: everything before the yield will be executed at the beginning of the while block when the interpreter calls \__enter__; the code after yield will run when \__exit__ is called at the end of the block.


```python
# Example 15-5: a context manager implemented with a generator
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    
    def reverse_write(text):
        original_write(text[::-1])
    
    original_write, sys.stdout.write = sys.stdout.write, reverse_write
    yield 'JASONTU'
    sys.stdout.write = original_write
```


```python
with LookingGlass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)
```

    pordwonS dna yttiK ,ecilA
    UTNOSAJ



```python
what
```




    'JASONTU'




```python
print('Back to normal')
```

    Back to normal



```python
# Example 15-7: generator-base context manager
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    
    def reverse_write(text):
        original_write(text[::-1])
    
    original_write, sys.stdout.write = sys.stdout.write, reverse_write
    
    msg = ''
    try:
        yield 'JASONTU'
    except ZeroDivisionError:
        msg = 'Please DO NOT divide by zero'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
```
