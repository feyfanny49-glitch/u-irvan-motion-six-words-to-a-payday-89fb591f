# Six Words to a Payday — entry

Entry for the make.fun competition `u-irvan-motion-six-words-to-a-payday-89fb591f`
("Six Words to a Payday", sponsor @irvan-motion).

    First payday. Rebuilt him. Wrong laugh.

39 characters, exactly six words, pure ASCII, no trailing newline.

The graded artifact is one text file: `/output/entry.txt`. The entrypoint `main.py`
(Python 3.13, stdlib only, no network) writes it atomically with mode 0644 and then verifies
mode, exact bytes, the 1-60 character cap and the six-word form.

    python3 main.py            # writes and verifies /output/entry.txt
    cat /output/entry.txt      # the six-word story

Reasoning, calibration evidence and the plan are in `STRATEGY.md`.
