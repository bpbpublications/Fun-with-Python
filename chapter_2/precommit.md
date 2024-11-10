# Hooks

```bash
$ ~/work/fun-with-python/ ll .git
total 72
18B Nov 19 15:55 COMMIT_EDITMSG
96B Dec 9 23:01 FETCH_HEAD
21B Nov 19 15:55 HEAD
41B Nov 22 17:45 ORIG_HEAD
310B Oct 16 20:46 config
73B Oct 16 20:46 description
372B Oct 29 22:05 fork-settings
480B Oct 16 20:46 hooks
1.9K Nov 22 21:58 index
96B Oct 16 20:46 info
128B Oct 16 20:46 logs
1.6K Dec 9 23:01 objects
112B Oct 16 20:46 packed-refs
160B Oct 16 20:46 refs

$ ~/work/fun-with-python/ ll .git/hooks
total 120
478B Oct 16 20:46 applypatch-msg.sample
896B Oct 16 20:46 commit-msg.sample
4.6K Oct 16 20:46 fsmonitor-watchman.sample
189B Oct 16 20:46 post-update.sample
424B Oct 16 20:46 pre-applypatch.sample
1.6K Oct 16 20:46 pre-commit.sample
416B Oct 16 20:46 pre-merge-commit.sample
1.3K Oct 16 20:46 pre-push.sample
4.8K Oct 16 20:46 pre-rebase.sample
544B Oct 16 20:46 pre-receive.sample
1.5K Oct 16 20:46 prepare-commit-msg.sample
2.7K Oct 16 20:46 push-to-checkout.sample
3.6K Oct 16 20:46 update.sample
```

# pre-commit

simple pylint script

```bash
#!/bin/sh

set -e

pylint --rcfile=./config.rc 2>&1
```

improved version - only for changed files


```bash
#!/bin/sh

set -e

FILES_CHANGED=$(git diff --name-only --diff-filter=ACM origin/main  | grep "\.py" || true

if [ -n "$FILES_CHANGED" ]; then
    echo $FILES_CHANGED | xargs pylint --rcfile=./config.rc 2>&1
fi
```

With fixed grep version

```bash
#!/bin/sh

set -e

FILES_CHANGED=$(git diff --name-only --diff-filter=ACM origin/main  | grep -E ".py$" || true

if [ -n "$FILES_CHANGED" ]; then
    echo $FILES_CHANGED | xargs pylint --rcfile=./config.rc 2>&1
fi
```


# pre-commit

## install

```bash
$ pre-commit install
```

* config

```yaml
default_stages: [commit, push]
repos:

- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v4.3.0
  hooks:
  - id: trailing-whitespace
  - id: end-of-file-fixer
  - id: check-json
  - id: check-yaml
  - id: debug-statements
  - id: check-merge-conflict
  - id: detect-private-key
  - id: end-of-file-fixer
  - id: pretty-format-json
    args: [--autofix]
  - id: no-commit-to-branch
    args: [--branch, master]
- repo: https://github.com/ambv/black
  rev: 22.10.0
  hooks:
  - id: black
    args: [--line-length=120]
- repo: local
  hooks:
  - id: pylint
    name: Pylint
    stages: [push]
    description: Run pylint
    entry: ./config/pylint.sh
    language: script
    types: [python]
    pass_filenames: false
  - id: flake8
    name: Check flake8
    stages: [push]
    description: RUn flake8
    entry: ./config/flake8.sh
    language: script
    args: [local]
    types: [python]
    pass_filenames: false

```

execute pre-commit

```sh
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check json...........................................(no files to check)Skipped
check yaml...........................................(no files to check)Skipped
debug statements (python)................................................Passed
check for merge conflicts................................................Passed
detect private key.......................................................Passed
fix end of files.........................................................Passed
pretty format json...................................(no files to check)Skipped
don't commit to branch...................................................Passed
black....................................................................Passed
Run pylint...............................................................Passed
Check flake8.............................................................Passed
[bugfix/some-branch-name ee9cdc99] test commit
1 file changed, 1 insertion(+)
```
