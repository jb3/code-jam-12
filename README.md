# Monumental Monsteras CJ25 Project
Monumental Monsteras CJ25 Project is a typing speed test,
but with a twist: You cannot type with a normal keyboard.
You can only use the **wrong tool for the job**.

Try different wrong methods of writing text, with a score at
the end if you would like to flex on your friends.

Input methods:

# Running the project
## Using `uv` (recommended)

The recommended way to run the project is using `uv`.

If you do not have `uv` installed, see https://docs.astral.sh/uv/getting-started/installation/

```
$ git clone https://github.com/Mannyvv/cj25-monumental-monsteras-team-repo.git
$ cd cj25-monumental-monsteras-team-repo.git
$ uv run src/main.py
```

## Without `uv`

```
$ git clone https://github.com/Mannyvv/cj25-monumental-monsteras-team-repo.git
$ cd cj25-monumental-monsteras-team-repo.git
$ py -3.12 -m venv .venv
$ py -m pip install .
$ py src/main.py
```

# Contributing
## Setting up the project for development
If you do not have `pre-commit` installed, see https://pre-commit.com/#installation

You can also use `uvx pre-commit` to run `pre-commit` commands without permanently installing it.

Once you have `pre-commit` installed, run this command to set up the commit hooks.
```
$ pre-commit install
```

## Development process
If the change you are making is large, open a new
issue and self-assign to make sure no duplicate work is done.

When making a change:
1. Make a new branch on the main repository
2. Make commits to the branch
3. Open a PR from that branch to main

You can run the pre-commit checks locally with:
```
$ pre-commit run -a
```
If you installed the commit hook in the previous step, they should also be run locally on commits.
