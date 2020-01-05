# A Scheme Interpreter in Python

A simple Scheme interpreter, getting some inspiration from Peter Norvig
(https://norvig.com/lispy.html) but involving quite an extensive revision to
match Scheme behavior as seen in Racket. The tokenizer and the parser are
written from scratch, assuming correct Scheme code.

As you can see, this interpreter can handle recursion, among other things:

```
scm.py> (+ 1 2)
3
scm.py> (- 1 -1)
2
scm.py> (define x 10)
scm.py> (+ x 20)
30
scm.py> (define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
scm.py> (fact 10)
3628800
scm.py> x
10
scm.py> (set! x 20)
scm.py> (+ x x x)
60
```
