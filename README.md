# python 3.9 / 3.10 asyncio race condition

the asyncio Semaphore in cpython has a race condition that can lead
to infinite blocking due to a corrupted state of the Semaphore.

You can use this code to reproduce the issue along with a possible
fix like this:

```
git checkout 52876860e43894b636b211643c232de44467dbef
# you are now using the bad implementation of 9d59381a5d
./main.py
# ^ will never finish
git checkout master
./main.py
# ^ will succeed
```

While this project is intended to highlight the blocking issue,
https://github.com/python/cpython/pull/93222 contains another, more
extensive solution.

`locks.py` is taken and modified from here: https://github.com/python/cpython/blob/9d59381a5d20157930bae34e5f5a7bc5ef09fa89/Lib/asyncio/locks.py
