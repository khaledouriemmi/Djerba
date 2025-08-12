
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

* **Unique Syntax** — Custom operators and keywords (inspired by Tunisian creativity 🌊).
* **Simple Commands** — Variables, math, printing, and conditionals.
* **Beginner-Friendly** — Small enough to understand in one sitting.
* **Interpreter in Python** — Easy to extend or modify.

Example syntax:

```djerba
$greeting <- "Hello from Djerba!"
:> $greeting
? 5 > 3 :> "This condition is true!"
```

---

## 📂 Project Structure

```
Djerba/
│
├── djerba.py         # Interpreter
├── test.djerba       # Example program
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

## 🛠 Writing Your Own Djerba Code

Djerba syntax is **minimal & expressive**:

* **Variables** start with `$`:

  ```djerba
  $x <- 5
  ```
* **Print** with `:>`:

  ```djerba
  :> "Welcome to Djerba!"
  ```
* **Conditions** with `?`:

  ```djerba
  ? $x > 3 :> "x is greater than 3"
  ```

---

## 💡 How It Works

1. **Read** — The interpreter loads `.djerba` files.
2. **Parse** — Tokenizes the syntax into commands.
3. **Execute** — Runs the commands in Python logic.

This project is a great starting point for learning about **interpreters** and **domain-specific languages (DSLs)**.

---

## 📦 Roadmap

* [ ] Add functions
* [ ] Add loops
* [ ] Add file I/O
* [ ] Create VS Code syntax highlighter

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