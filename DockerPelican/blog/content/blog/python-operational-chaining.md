Title: Python uses operational chaining for boolean comparisons
Date: 2017-01-20 18:23
Tags: Python
Category: Computer Science
Author: Tim Jones
Summary: It is important to understand Python's use of operational chaining to avoid programming errors

#### Problem

A colleague noticed this behavior:

```
>>> 'a' in 'b' == 0
False
>>> ('a' in 'b') == 0
True
>>> 'a' in ('b' == 0)
TypeError: argument of type 'bool' is not iterable
```

offering a bucket of doubloons to anyone who can explain it.

#### Explanation

Parenthesis force Python to do something first. I often use parenthesis out of habit even when not needed just to be 100% clear.

In the first instance above, Python is operator chaining. For `'a' in 'b' == 0`, it first loads a and b strings (STACK: b,a)
it then DUP_TOP duplicates 'b' so that it doesn’t have to waste time to load it again for the second evaluation (STACK: b, b, a).  
ROT_THREE lifts second and third stack item up and the top item down to third place, so now the stack is STACK: b, a, b. 
COMPARE_OP acts on b,a … since it is not true, it jumps and just returns False. What is interesting is if you do `'a' in 'a' == 1`, 
which after DUP_TOP has the stack (STACK: a,a,a); here `'a' in 'a'` is obviously true, but I think the first two 'a's are 
replaced with the result of that evaluation True which, being the top of the stack is popped off by JUMP_IF_FALSE_OR_POP 
leaving the duplicated 'a' on the top of the stack, where then 1 is loaded so the stack is [1, a] and the == comparison is 
applied which is indeed False. Thus `'a' in 'b' == 0` is effectively the same as `'a' in 'b' and 'b' == 0` which is false.

Using the dis module, we find:

```
>>> 'a' in 'a'
True
>>> 'a' in 'a' and 'a' == True
False
>>> 'a' in 'a' == True
False
```
```
  7           0 LOAD_CONST               1 ('a')
              3 LOAD_CONST               2 ('b')
              6 DUP_TOP
              7 ROT_THREE
              8 COMPARE_OP               6 (in)
             11 JUMP_IF_FALSE_OR_POP    21
             14 LOAD_CONST               3 (0)
             17 COMPARE_OP               2 (==)
             20 RETURN_VALUE
        >>   21 ROT_TWO
             22 POP_TOP
             23 RETURN_VALUE

'a' in 'b' and 'b' == 0
15           0 LOAD_CONST               1 ('a')
              3 LOAD_CONST               2 ('b')
              6 COMPARE_OP               6 (in)
              9 JUMP_IF_FALSE_OR_POP    21
             12 LOAD_CONST               2 ('b')
             15 LOAD_CONST               3 (0)
             18 COMPARE_OP               2 (==)
        >>   21 RETURN_VALUE

'a' in 'a' == 0
  9           0 LOAD_CONST               1 ('a')
              3 LOAD_CONST               1 ('a')
              6 DUP_TOP
              7 ROT_THREE
              8 COMPARE_OP               6 (in)
             11 JUMP_IF_FALSE_OR_POP    21
             14 LOAD_CONST               2 (0)
             17 COMPARE_OP               2 (==)
             20 RETURN_VALUE
        >>   21 ROT_TWO
             22 POP_TOP
             23 RETURN_VALUE
 ```

The final case is simply a typecasting problem.
