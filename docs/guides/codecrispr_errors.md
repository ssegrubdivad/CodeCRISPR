
# CodeCRISPR Toolkit — Error Message Reference and Interpretation Guide

This document provides a complete explanation of the error messages produced by CodeCRISPR Toolkit. It is intended to help both human users and AI assistants interpret errors clearly and take appropriate action in response.

---

## 1. Index Out of Bounds

**Message:**  
`Attempted to access line index 105, which is out of bounds for file 'filename.ext'.`

**Explanation:**  
The toolkit tried to read a line that does not exist in the file. This usually indicates that a block was expected to be longer than it actually is, possibly due to a missing closing bracket, brace, or keyword such as `end`.

**What to Do:**  
Review the file and ensure that all blocks are syntactically complete. Re-run the inspection to rebuild the reference map. If you're an AI assistant, notify the user that the file may be structurally malformed and recommend a manual check.

---

## 2. File Write Failure

**Message:**  
`Failed to write to 'filename.ext': [Errno 13] Permission denied.`

**Explanation:**  
The toolkit could not save changes to the specified file, likely due to permission issues, a read-only file, or restrictions on the current directory.

**What to Do:**  
Ensure that the target file is writable. Check the user or AI’s permissions and file system attributes. AI agents should avoid retrying until access is confirmed or alternate paths are suggested.

---

## 3. Method or Block Not Found

**Message:**  
`Function or block 'methodName' not found.`

**Explanation:**  
The named code block was not found in the toolkit’s internal reference map. This could be because it does not exist, has been renamed, or the file has changed since it was last inspected.

**What to Do:**  
Re-run the `--inspect` command on the file to refresh the reference map. AI assistants should revise their internal understanding of the file structure before attempting another replacement.

---

## 4. Undefined Block End

**Message:**  
`Could not determine closing boundary for block 'environmentName'.`

**Explanation:**  
A block or environment was opened but the toolkit could not find a proper end to it. For example, a LaTeX environment may have a `\begin{theorem}` but no matching `\end{theorem}`.

**What to Do:**  
Review the file to confirm that all structural pairs are complete. This may require human intervention to ensure syntax correctness.

---

## 5. No Identifiable Blocks

**Message:**  
`No matching patterns found for identifiable blocks in 'filename.ext'.`

**Explanation:**  
The toolkit could not find any functions, methods, or structural blocks in the file. This may be due to an unsupported language, empty file, or incorrect syntax.

**What to Do:**  
Ensure the file is non-empty and written in a supported language. If the language is not supported, consider writing a new language tool using one of the existing modules as a guide.

---

## 6. Replacement Target Unreachable

**Message (anticipated):**  
`Replacement range exceeds file length.`

**Explanation:**  
The range where a method is expected to exist lies outside the bounds of the current file, suggesting that the file has been truncated or modified unexpectedly.

**What to Do:**  
Perform a fresh `--inspect` to reset line ranges. AI agents should avoid using stale reference maps from previous file states.

---

## 7. Unknown or Unexpected Exception

**Message (general fallback):**  
`An unexpected error occurred: <error description>`

**Explanation:**  
The toolkit encountered an unhandled Python exception. This may indicate a bug in the language tool, an unanticipated syntax edge case, or a corrupted file.

**What to Do:**  
Report the error if reproducible. Human users may inspect the traceback for details. AI agents should avoid making assumptions about the result and instead alert the user.

---

## Summary

All errors produced by the toolkit are intended to be clear and actionable. AI assistants should treat these errors as signals to re-inspect, re-evaluate, or defer to the user. By interpreting these messages correctly, tool users and AI can safely manage and manipulate source files across many languages without encountering catastrophic failures.

This document is recommended as a reference for both developers and automated systems integrating with CodeCRISPR Toolkit.
