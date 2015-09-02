Title: Functional Programming with Collections in Python
Date: 2015-3-14
Tags: python, scala, functional programming
Slug: functional-programming-collections-python
Author: Pedro Rodriguez
Description: Using ScalaFunctional to do functional programming in Python

In January I started working as a data scientist at [Trulia](https://trulia.com/) (which recently merged with [Zillow](https://zillow.com/)). Most of my data science work at Trulia involves writing Python with a smattering of SQL/Java for good measure. Prior to that and graduating from UC Berkeley, I worked in the UCB AMPLab on topic modeling research using [Apache Spark](http://spark.apache.org/). That meant I ended up writing lots of [Scala](http://www.scala-lang.org/).


Now that I work mostly in Python, the feature I miss most from Scala is the rich support for functional programming on collections.

As a data scientist, a lot of what I do involves repeatedly transforming and merging data sets until I can do something useful with them (such as running machine learning algorithms). Its been said before that 90% of data "science" is really data wrangling. Perhaps the 90% is a little blown out of proportion, but the sentiment is certainly true. With that in mind, it is very important for data scientists to have great tools for wrangling data.

Like any smart, but ultimately lazy programming does, I looked around to see if someone had already solved my problem. The first thing I looked at was [Pandas](http://pandas.pydata.org/). My overall impression is that it is a very powerful library with support for many of the data wrangling operations I was hoping for. That being said, [Pandas](http://pandas.pydata.org/) has a very opinionated way of manipulating data. Consequently, this makes it powerful and expressive when it works, but sometimes frustratingly difficult, especially at first, to figure out the "Panda way" of accomplishing what you want. Nonetheless, I use Pandas every day in conjunction with the library described farther down.

I still missed the powerful *simplicity* and *intuitiveness* of working with Scala collections. Here are a couple examples of code using Scala to do some number twiddling.

### Number Twiddling
```
:::scala
scala> val numbers = List(-3, -2, -1, 1, 2, 3)
// Double each value in the list
scala> numbers.map(x => x * 2)
res0: List[Int] = List(-6, -4, -2, 2, 4, 6)
// Filter out negative values
scala> numbers.filter(x => x > 0)
res1: List[Int] = List(1, 2, 3)
// Get the sum of double each positive element
scala> numbers.filter(x => x > 0).map(x => x * 2).reduce((x, y) => x + y)
res2: Int = 12

// Calculate the factorials from 9 down
scala> val range = List(1, 2, 3, 4, 5, 6, 7, 8, 9)
scala> range.inits.map(l => l.product).toList
res9: List[Int] = List(362880, 40320, 5040, 720, 120, 24, 6, 2, 1, 1)
```

Perhaps its just me, but this is quite beutiful to write and read. The best part, is that **each operation sequentially describes how the data is transformed**. If we wanted to accomplish the same in Python, we might write something like this:


### Python Solution
```
:::python
In [16]: numbers = [-3, -2, -1, 1, 2, 3]

In [17]: map(lambda x: x * 2, numbers)
Out[17]: [-6, -4, -2, 2, 4, 6]

In [18]: filter(lambda x: x > 0, numbers)
Out[18]: [1, 2, 3]

In [19]: reduce(lambda x, y: x + y, map(lambda x: x * 2, filter(lambda x: x > 0, numbers)))
Out[19]: 12

# Factorials from 9 and down
In [15]: map(lambda l: reduce(lambda x, y: x * y, l), [range(1, i) for i in range(2,11)])
Out[15]: [1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
```

Even this fairly trivial set of examples shows some of Python's readability weakness in transforming data. Instead of allowing for functional operations on data to be chained one after another, Python forces embedded calls which rapidly become difficult to read and write. Do you see how this could be a problem when your day job in data science is 90% transforming and wrangling data?

Perhaps the entire goal is non-pythonic, but in practice I find Scala's style of functional programming on collections powerful, flexible and most importantly very effective.

So, as espoused by the first of 7 habits in [The 7 Habits of Highly Effective People](http://www.amazon.com/Habits-Highly-Effective-People-Powerful/dp/1451639619/ref=sr_1_1?ie=UTF8&qid=1426303029&sr=8-1&keywords=7+habits+of+highly+effective+people), I did something *proactive* about it. I authored [ScalaFunctional](https://github.com/EntilZha/ScalaFunctional). I certainly am not advocating always reinventing the wheel, but [sometimes](http://blog.codinghorror.com/programming-is-hard-lets-go-shopping/) it makes sense to do so if the wheel doesn't exist or is the wrong shape.

The goal of [ScalaFunctional](https://github.com/EntilZha/ScalaFunctional) is to bring all the collections goodies from Scala (and some from Spark) to Python. I first realized this was possible after googling around and finding that as is common in the age of the internet, [this question has been asked and answered](http://stackoverflow.com/questions/27222193/clean-code-for-sequence-of-map-filter-reduce-functions/27222611#comment45051488_27222611).

Before talking about how the library is designed, lets step back and see an example of [ScalaFunctional](https://github.com/EntilZha/ScalaFunctional) in action. Lets try implementing word count in Python. Below is the first solution I found on [Stack Overflow](http://stackoverflow.com/questions/21107505/python-word-count-from-a-txt-file-program) followed by the solution using ScalaFunctional.


### Python Solution
```
:::python
# Standard Python solution
text = "here is the text of text".split(" ")
wordcount={}
for word in text:
    if word not in wordcount:
        wordcount[word] = 1
    else:
        wordcount[word] += 1

# Using ScalaFunctional
from functional import seq
text = "here is the text of text".split(" ")
wordcount = seq(text)\
	.map(lambda w: (w, 1))\
	.reduce_by_key(lambda x, y: x + y).to_dict()
```

So what is going on? How was word count, which took six lines of Python plus a for loop, if else statement, and dictionary able to be compressed to a single line of Python (split across 3 lines for readability) with the ```functional``` package?

Lets review the approach in case its unclear. First we get an array of words. We map these onto tuples with the word as the first element and ```1``` as the second. This results in tuples that look like: ```("here", 1), ("is", 1)``` and so on. Finally, `reduce_by_key` will group elements by the first element of the tuple, and collect the second element using the function passed into ```reduce_by_key```. In this case, it will sum them together resulting in the count of each word.

Under the hood, `seq` isn't doing anything particularly magical. The approach is actually fairly straightforward. `seq` takes a list then wraps it in a custom object named `FunctionalSequence`. `FunctionalSequence` implements functions such as `map`, `filter`, `reduce`, `reduce_by_key` and many more. Each of those functions will return its result wrapped in a new `FunctionalSequence` object if its return value is list-like. Since the return value is of type `FunctionalSequence`, its possible to chain as many of these operations together as desired.

You can find the project at [github.com/EntilZha/ScalaFunctional](https://github.com/EntilZha/ScalaFunctional), install it from [pypi](https://pypi.python.org/pypi/ScalaFunctional/) using `pip install scalafunctional`, and/or read the docs at [scalafunctional.readthedocs.org](http://scalafunctional.readthedocs.org/en/latest/). Bug reports, contributions, or feedback are always welcome.
