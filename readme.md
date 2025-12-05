
# 🌴 Djerba — A Minimal Custom Programming Language

> **Djerba** is a tiny, personal programming language & interpreter written in Python.
> Named after the beautiful island of **Djerba** in Tunisia, where I grew up, this project reflects both my love for computer science and my roots.

This project demonstrates:

* Interpreter design
* Lexical parsing
* Custom syntax creation
* Command execution in a sandboxed environment

---

## ✨ Features

* **Unique Syntax** — Custom operators and keywords inspired by Tunisian creativity 🌊
* **Lists & Arrays** — First-class support for collections
* **For Loops** — Easy iteration over lists and ranges
* **Logical Operators** — Boolean logic with `and`, `or`, `not`
* **Rich Built-ins** — 20+ built-in functions for math, strings, and lists
* **Functions** — Define reusable functions with parameters
* **Control Flow** — If/else, while loops, break/continue
* **Beginner-Friendly** — Small enough to understand in one sitting
* **Interpreter in Python** — Easy to extend or modify

Example syntax:

```djerba
$greeting <- "Hello from Djerba!"
:> $greeting

$numbers <- [1, 2, 3, 4, 5]
@> $num in $numbers {
  :> "Number:", $num
}

? 5 > 3 and true {
  :> "Logical conditions work!"
}
```

---

## 📂 Project Structure

```
Djerba/
│
├── djerba.py         # Interpreter (enhanced)
├── test.djerba       # Comprehensive examples
└── README.md         # You are here
```

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/khaledouriemmi/djerba-lang.git
cd djerba-lang
```

### 2️⃣ Run your first Djerba program

Make sure you have Python 3 installed.

```bash
python djerba.py test.djerba
```

---

## 🛠 Language Reference

### Variables
Variables start with `$`:
```djerba
$x <- 5
$name <- "Khaled"
$isReady <- true
```

### Printing
Print with `:>`:
```djerba
:> "Welcome to Djerba!"
:> "Value:", $x
```

### Data Types
- **Numbers**: `42`, `3.14`
- **Strings**: `"hello"`, `"world"`
- **Booleans**: `true`, `false`
- **Lists**: `[1, 2, 3]`, `["a", "b", "c"]`

### Lists
```djerba
$fruits <- ["apple", "banana", "cherry"]
:> $fruits[0]           ;; "apple"
:> len($fruits)         ;; 3
append($fruits, "date")
```

### Conditionals
Use `?` for if, `else` for else:
```djerba
? $x > 3 {
  :> "x is greater than 3"
} else {
  :> "x is 3 or less"
}
```

### Logical Operators
```djerba
? $x > 5 and $y < 10 {
  :> "Both conditions are true"
}

? $a == 0 or $b == 0 {
  :> "At least one is zero"
}

? not $isDone {
  :> "Still working..."
}
```

### While Loops
Use `~` for while:
```djerba
$i <- 0
~ $i < 5 {
  :> $i
  $i <- $i + 1
}
```

### For Loops
Use `@>` for for-each loops:
```djerba
@> $item in [1, 2, 3, 4, 5] {
  :> "Item:", $item
}

@> $i in range(10) {
  :> $i
}
```

### Break & Continue
```djerba
@> $n in range(10) {
  ? $n == 5 {
    break      ;; Exit loop
  }
  ? $n % 2 == 0 {
    continue   ;; Skip even numbers
  }
  :> $n
}
```

### Functions
Use `@` to define functions, `!>` to return:
```djerba
@add(a, b) {
  !> a + b
}

:> add(5, 3)  ;; 8

@greet(name) {
  :> "Hello,", name
}

greet("Djerba")
```

---

## 📚 Built-in Functions

### Math Functions
- `sin(x)`, `cos(x)`, `tan(x)` — Trigonometric functions
- `sqrt(x)` — Square root
- `abs(x)` — Absolute value
- `floor(x)`, `ceil(x)`, `round(x)` — Rounding functions
- `min(...)`, `max(...)` — Minimum and maximum
- `pow(x, y)` — Power (also available as `x ^ y`)

### String Functions
- `len(s)` — Length of string or list
- `upper(s)` — Convert to uppercase
- `lower(s)` — Convert to lowercase
- `substr(s, start, end)` — Extract substring

### List Functions
- `append(list, item)` — Add item to list
- `push(list, item)` — Same as append
- `pop(list)` — Remove and return last item
- `len(list)` — Get list length

### Utility Functions
- `range(n)` — Generate list `[0, 1, ..., n-1]`
- `range(start, end)` — Generate list from start to end-1
- `range(start, end, step)` — Generate list with step
- `type(x)` — Get type: "number", "string", "bool", "list"
- `input(prompt)` — Read user input (optional prompt)

### Constants
- `PI` — 3.14159...
- `E` — 2.71828...

---

## 💡 Example Programs

### FizzBuzz
```djerba
@> $num in range(1, 16) {
  ? $num % 15 == 0 {
    :> "FizzBuzz"
  } else {
    ? $num % 3 == 0 {
      :> "Fizz"
    } else {
      ? $num % 5 == 0 {
        :> "Buzz"
      } else {
        :> $num
      }
    }
  }
}
```

### Fibonacci
```djerba
@fibonacci(n) {
  ? n <= 1 {
    !> n
  }
  !> fibonacci(n - 1) + fibonacci(n - 2)
}

@> $i in range(10) {
  :> "fib(", $i, ") =", fibonacci($i)
}
```

### Sum of List
```djerba
@sumList(lst) {
  $total <- 0
  @> $item in lst {
    $total <- $total + $item
  }
  !> $total
}

:> sumList([10, 20, 30, 40])  ;; 100
```

---

## 🏝 Inspiration

* My hometown **Djerba, Tunisia**
* Curiosity about how programming languages work under the hood

---

## 👨‍💻 Author

**Khaled Ouriemmi**
[GitHub](https://github.com/khaledouriemmi)

---

## 📜 License

This project is open-source under the MIT License.
Feel free to fork, modify, and build your own island of code 🏝.

---