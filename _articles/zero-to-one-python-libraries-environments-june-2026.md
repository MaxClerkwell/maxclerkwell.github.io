---
title: "Zero to One: Python Libraries, Environments, and Working Like You Mean It"
date: 2026-06-16
tags: [python, education, zero-to-one]
description: "You do not have to write everything from scratch. Python has thousands of libraries. But the way you pull them in matters, and most introductions get that part wrong."
keywords: "python virtual environment, uv python, pyproject.toml, requirements.txt, python repl, standard library, pip alternatives, python beginners"
draft: true
---

![Python logo](/assets/posts/zero-to-one-python-libraries-environments-june-2026/python-logo.png)

*Python and the Python logo are trademarks of the Python Software Foundation.*

You have heard of Python. Maybe someone mentioned it in passing, maybe you saw a snippet online and thought it looked approachable. You are not sure where to start. This article is for you.

The goal is not to teach you the language. It is to show you the three things that matter before you write a single function: how to explore interactively, where to find code that already exists, and how to manage dependencies without making a mess of your machine. By the end, you will have a working Python script, a proper project structure, and an understanding of why each piece is there.

One thing before we start: this article assumes Linux. If you are serious about programming and you are not on Linux yet, fix that first. Debian is the best-documented distribution for development work, and everything here assumes it.

---

## The REPL: Exploration, Not Production

Open a terminal and type `python3`. You are now in the Read-Eval-Print Loop. Type an expression, press Enter, get a result.

```
>>> 2 ** 10
1024
>>> "hello" + " " + "world"
'hello world'
```

The REPL is useful for two things: quick numerical experiments and exploring an unfamiliar library before you commit to using it. It is not where you build anything that needs to work tomorrow. Code you type in the REPL disappears when you close it. Treat it as a scratchpad.

When you are done, type `exit()` and press Enter to leave the REPL and return to your normal shell prompt.

One specific use I find underrated: the REPL as a filesystem explorer. We will build our own file exploration tool in Python in a later article, and the REPL will be a great place to prototype it.

---

## The Standard Library: Use It First

Python ships with a standard library that covers an enormous amount of ground. Before reaching for a third-party package, check whether the stdlib already does what you need.

Let us look at `math` as a first example. You can import it directly in the REPL and start calling functions:

```
>>> import math
>>> math.sqrt(2)
1.4142135623730951
>>> math.cos(math.pi)
-1.0
>>> math.floor(3.7)
3
>>> exit()
```

The rule is simple: if there is a stdlib module for your problem, use it. Import it by its full name and keep the namespace, exactly as shown above.

> **Disclaimer:** If you have looked into other Python tutorials you will likely find things like `from math import cos` or `import math as m`. Even though these are perfectly valid Python, forget about them for a few days. If you want to use a function from `math` or any other library, write out the full namespace: `math.cos(...)`, not just `cos(...)`. The reason is readability. When you read code written by someone else, or by yourself six months later, `math.cos` tells you immediately where that function comes from. A bare `cos` tells you nothing. Namespace collisions in larger codebases are subtle and painful. The explicit prefix costs you a few extra characters and saves you an hour of debugging three months from now.

---

## Script Files and the `__main__` Guard

The REPL is temporary. Scripts are not. When you write Python that should run as a program, save it to a `.py` file.

Open a fresh file, for example with `vim my_script.py`, and write the following:

```python
import math

if __name__ == "__main__":
    angle = math.pi / 4
    result = math.cos(angle)
    print(result)
```

If you have ever used other programming languages you may already be familiar with the concept of a main function: a designated entry point that the runtime looks for when it starts your program. In C you write `int main()`, in Java `public static void main(String[] args)`. Python does not enforce this at the language level, but the `if __name__ == "__main__":` block serves the same purpose. When Python runs a file directly, it sets the special variable `__name__` to the string `"__main__"`. When a file is imported as a module by some other file, `__name__` is set to the module's name instead. The block only executes in the first case.

> **Please do not omit this.** You may have seen it missing in other tutorials and assumed it was optional noise. In these simple examples, it is technically not required. But in the general case, you want to make sure that your script only runs its logic when it is actually invoked as a program, not when it is imported by something else. The moment you start writing larger programs where one file imports from another, any module-level code that prints output, modifies state, or starts a process will fire on import. The `if __name__ == "__main__":` guard prevents that. Form the habit now, before it costs you something.

Run the script:

```bash
python3 my_script.py
```

You should see `0.7071067811865476` printed to your terminal.

---

## Dependencies: Why We Need More Than the Standard Library

The standard library is large, but it has intentional gaps. It does not include tools for plotting, machine learning, HTTP clients with advanced retry logic, colored terminal output, image processing, and thousands of other things. For these, you reach for third-party libraries: code that other people wrote, packaged up, and made available for you to install.

If you have worked in other programming languages, you may already know that pulling in extra libraries can get messy very quickly. In C or C++ you are often tracking down header files and linking flags by hand. In Java the situation is better with Maven or Gradle, but still complex. Python has a particularly clean approach to this problem, and understanding it well from the beginning will save you a lot of pain.

The question is: how do you install third-party libraries without eventually creating a conflict-ridden mess on your machine?

### A brief history, so you understand why things are the way they are

For years, the standard advice was: install packages with a tool called `pip`. This works until it does not. Pip installs packages into whichever Python environment is active. If you just run it without thinking, that is your system Python, the one your operating system may itself depend on. The moment you have two projects that need different versions of the same library, you have a conflict. On Debian-based systems, a carelessly pip-installed package can interfere with system tools that rely on Python. Things can become genuinely broken this way.

The community's first answer was virtual environments, and the concept is important enough to understand clearly. A Python environment is the combination of a Python interpreter and a set of installed packages. When Python looks for a library you import, it searches inside the active environment. The system Python is one environment, but you can create as many additional ones as you like, each with their own interpreter copy and their own isolated set of installed packages.

A virtual environment, then, is an environment scoped to a single project. You create it, point your shell at it, and anything you install from that moment forward lands inside that project's isolated directory and nowhere else. You can have project A using version 1.2 of some library and project B using version 2.0 of the same library, in two separate environments, with no conflict between them. When you are done with a project, you can delete the environment directory and your system is exactly as clean as it was before.

This is the right idea. The problem was in the tooling around it. Pip and the original `venv` module gave you the isolation, but they did not give you a reliable way to reproduce an environment exactly. The convention was a `requirements.txt` file listing package names and optional version pins. But it did not capture transitive dependencies: the packages that your packages depend on. Someone else clones your repo, installs from your `requirements.txt`, gets slightly different transitive versions because the ecosystem has moved on, and your code breaks in subtle ways.

Forget about pip for the next few days or weeks. You now know it exists, and if you see it in older tutorials or projects you will recognize it. But we are going to use a better tool from the start.

### pyproject.toml

`pyproject.toml` is the modern standard for declaring what a Python project is and what it needs. It is a structured, machine-readable file that tools can parse, diff, and reason about. It is the right place to record your dependencies.

Here is what a minimal one looks like:

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "rich",
]
```

The `[project]` table holds your project's metadata. The `dependencies` list is where third-party packages go. The standard library never appears here because it is always available with no installation needed.

---

## uv: Install This Now

`uv` is a project and dependency manager for Python. It is not a narrow replacement for pip; it does considerably more. It manages Python interpreter versions, creates and manages virtual environments, resolves and locks dependencies, and gives you a single coherent workflow instead of several disconnected tools stitched together. It is what we will use for the rest of this article.

Install it once:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

> **Before you run that:** piping a script fetched from the internet directly into your shell for execution is a genuine security risk, and you should not make a habit of doing it just because some article tells you to. What that command does is download a shell script from astral.sh and hand it directly to `sh` without you ever seeing what is in it. If the server were compromised, or if you mistyped the URL and landed somewhere else, your machine would execute whatever it received. The correct habit is to inspect first: open `https://astral.sh/uv/install.sh` in your browser, read through it, and satisfy yourself that it does what it claims. In this case it downloads a prebuilt binary and puts it in `~/.local/bin`. It is not doing anything exotic. But the habit of checking is more important than this particular script, and I would rather you slow down here than learn to run things blindly.

Then close and reopen your terminal, or run `source ~/.bashrc`, so the shell picks up the new `uv` command.

---

## Putting It Together

Now we have all the concepts. Let us build an actual project.

Start by creating a directory and writing the `pyproject.toml` yourself:

```bash
mkdir my-project
cd my-project
```

Open a new file called `pyproject.toml` with your editor and write the following:

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "rich",
]
```

Now create `main.py`:

```python
import math
import rich.console
import rich.panel

console = rich.console.Console()

if __name__ == "__main__":
    angle = math.pi / 6
    result = math.sin(angle)
    message = f"sin(pi/6) = {result:.6f}"
    panel = rich.panel.Panel(message, title="Result", style="bold green")
    console.print(panel)
```

Your project directory now looks like this:

```
my-project/
├── pyproject.toml
└── main.py
```

Now let uv read the `pyproject.toml`, create a virtual environment, and install everything declared in `dependencies`:

```bash
uv sync
```

That is all. `uv sync` reads your `pyproject.toml`, creates a `.venv` directory in your project folder, installs `rich` and everything it depends on into that isolated environment, and writes a `uv.lock` file that records the exact version of every package that was installed.

Run the script:

```bash
uv run main.py
```

You should see a green bordered panel in your terminal with the result. The `math` module came from the standard library. The `rich` library came from PyPI (the Python Package Index, a public registry at pypi.org where anyone can publish Python packages and where `uv` fetches them from by default), installed into the project's isolated environment.

Your project directory now contains:

```
my-project/
├── .venv/
├── uv.lock
├── pyproject.toml
└── main.py
```

The lock file is the thing that `requirements.txt` was trying to be and never quite was. It records every transitive dependency at an exact version. Someone else gets a copy of your project, runs `uv sync`, and they get exactly the same environment you had. No drift, no surprises.

### The shortcut: uv init and uv add

Once you understand what the files are for, you do not have to write them by hand every time. `uv init` creates the project structure for you:

```bash
uv init my-project
cd my-project
```

This generates a `pyproject.toml`, a `main.py`, a `.python-version` file pinning the interpreter version, and a `.gitignore`. And instead of editing `pyproject.toml` by hand to add a dependency, you can run:

```bash
uv add rich
```

This updates `pyproject.toml`, resolves the new dependency, and runs the equivalent of `uv sync` automatically. The result is the same as what you built by hand; this is just faster once you know what it is doing.

---

## Where This Goes Next

Libraries exist for almost everything you will want to do. The skill is knowing when to reach for one, which one to trust, and how to isolate it from the rest of your system. You now have all three pieces in place.

I will write about another small Python project here soon. If you already have a specific problem you were trying to solve when you started reading this, feel free to tell me what it is and I will write something up around that.

One last thing: you may have noticed that `uv init` created a file called `.gitignore` without explanation. Git is a tool for tracking the history of your files and sharing projects with others. It is the standard way to manage code over time, and `.venv/` is the kind of directory you do not want it touching. I have not introduced git yet because it deserves its own article. There is a Zero-to-One for git coming. Until then, just leave those files where they are.
