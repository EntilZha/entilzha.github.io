Title: Debugging Machine Learning Code
Date: 2019-12-15
Tags: code
Slug: debug-ml-code
Author: Pedro Rodriguez

Developing new machine learning code is often error prone and takes many iterations of the write-run-debug loop.
In this context, I specifically refer to saving time fixing errors that crash the program--not than those that cause models to be incorrect in subtle ways (for that, see [Andrej Karpathy's blog post](https://karpathy.github.io/2019/04/25/recipe/)).
Here are a few tricks I use to preserve my sanity while developing new model code written in python.

### Use Debuggers

Modern machine learning code often contains several abstraction levels---a good thing!---which unfortunately makes it more difficult to dig deep into plumbing to fix data loading or tensor shape errors.
Debuggers are exceptionally useful in these cases.
I use them in one of two ways.

If I know that the program fails then you can start a debugger on failure by using one of:

1. `import pdb;pdb.set_trace()`, `breakpoint()` on the line that fails
2. If it fails for only some iterations (e.g., one data point is bad), then `python -m pdb mytrainingscript.py` to start a session and press `c` to start the program. The interpreter will drop you into a debug session when the failure occurs.
3. For `allennlp` specifically, this command works well: `ipython -m ipdb (which allennlp) -- train config.jsonnet`

Sidenote: I use `ipdb` instead of `pdb` since its more similar to the `ipython` terminal.

### Document Tensor Shapes

Its extremely helpful to know tensor shapes during development and helps reduce time when looking at code again.
Here are is a sample forward pass of a pytorch model with shape annotations:

```python
def forward(self, text, length):
    output = {}
    # (batch_size, seq_length)
    text = text['tokens'].cuda()

    # (batch_size, 1)
    length = length.cuda()

    # (batch_size, seq_length, word_dim)
    text_embed = self._word_embeddings(text)

    # (batch_size, word_dim)
    text_embed = self._word_dropout(text_embed.sum(1) / length)

    # (batch_size, hidden_dim)
    hidden = self._encoder(text_embed)

    # (batch_size, n_classes)
    output['logits'] = self._classifier(hidden)
```

### Verbose Logging to Terminal and Files

I often see print statements, but not much usage of the python `logging` module in model code.
Although it takes some setup, there are several benefits to using `logging.info` over `print`.

1. Timestamps are logged "for free" which is helpful to understanding where most of the execution time is spent.
2. Logging can be configured to output the module a statement is from which makes debugging faster.
3. Logging can also be configured to write to a file. This has saved me a few times when I didn't expect to need `print` output when I ran the model, but later needed it.
4. This leads me to: be verbose in what you log. I love that the logging in [allennlp](https://allennlp.org) includes things like model parameters.

I typically include this code in my package for logging to the standard error and a file

```python
# In a file like util.py
import logging


def get(name):
    log = logging.getLogger(name)

    if len(log.handlers) < 2:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler('mylogfile.log')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)

        log.addHandler(fh)
        log.addHandler(sh)
        log.setLevel(logging.INFO)
    return log

# In my model file
from mypackage import util

log = util.get(__name__)
log.info("hello world")
```

### Small Debug Dataset

Another common issue is debugging an error when dataset loading takes a long time.
Its very annoying to debug shape issues when your dataset takes twenty minutes to load.
One trick---aside from using `pdb`---is to make a small debug dataset and testing with this before using the full dataset.
If your dataset is in a line delimited format like [jsonlines](https://jsonlines.org), then it may be as easy as `$ cat mydata.jsonl | head -n 100 > debug_dataset.jsonl`

### Unit Tests

Last but not least, writing a few unit tests is often helpful.
Specifically, I like writing unit tests for data or metric code that is not obviously correct by inspection.
[PyTest](https://docs.pytest.org/en/latest/) has worked very well for this purpose since its easy to use and configure.

Here is a simple example of my configuration (`pytest.ini`)

```ini
[pytest]
testpaths = awesomemodel/tests/
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

A sample test in `awesomemodel/tests/test_zero.py`:

```python
from numpy.testing import assert_almost_equal
import pytest

from awesomemodel.numbers import AlmostZero


def test_zero():
    zero = AlmostZero()
    assert_almost_equal(0.0, zero())

```

And running the test

```bash
$ pytest
======================================================================================= test session starts ========================================================================================
platform linux -- Python 3.8.0, pytest-5.3.1, py-1.8.0, pluggy-0.13.1
rootdir: /tmp/src, inifile: pytest.ini, testpaths: awesomemodel/tests/
collected 1 item                                                                                                                                                                                   

awesomemodel/tests/test_zero.py .                                                                                                                                                            [100%]

======================================================================================== 1 passed in 0.13s =========================================================================================
```

For reference, the directory structure
```bash
$ tree
.
├── awesomemodel
│   ├── __init__.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_zero.py
│   └── zero.py
└── pytest.ini

2 directories, 5 files
```

That's all I got, hope its helpful!