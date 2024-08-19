This folder is intended to filter out most commits, retaining only those that meet two criteria:

    1, The commit includes one source file and one test file.
    2, Only a single function is changed within that source file.

Reasons:

>A, One source file and one test file: Based on our experience and survey hundreds standardized submission practices, we believe this pattern significantly helps in localizing bug fixes to their corresponding unit tests aimed specifically at these changes.

>B, Single function changes: According to findings from [1], large blocks of code can be challenging for LLMs in single-round conversation to handle effectively in program repair tasks. Therefore, our benchmark focuses on single function changes within the source file. However, our intermediate data and scripts do support multiple hunks and multiple functions; we plan to extend these in future work.
