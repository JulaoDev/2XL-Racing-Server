# 🤝Contributing to JulaoDev 2XL Racing Server

First off, thank you for taking the time to contribute! this open-source preservation framework aims to revive the propietarty 2XL Games engine and safeguard digital software history.

## 🚀 How to Contribute

### 1. Reverese Engineering & Binary Analysis
* All analysis regarding `libndkwrapper.so` must be documented using static decompilation offsets (Ghidra/IDA Pro) or live runtime memory breakpoint offsets.
* If you identify key validation structs, sub-routine address, or network packet signatures, please open a detailed issue or append your findings directly to **Issue #3**.

### 2. Backend Development (FastAPI)
* Keep your code modular within `server_2xl.py`.
* Ensure any new endpoint routes match the original game's HTTP routing specifications.
* Run tests locally usinmg our automated client script `test_server.py` before submitting a pull request to ensure regressions do not occur.

### 📝 Pull Request Guideline 
* **Branch Strategy:** Create a descriptive feature branch (e.g., `feature/token-validation-fix`).
* **Documentation:** Provide clean, standalone Python comment explaining why a specific JSON key or header parameter was introduced.
* ****Licensing:** By contributing, you agree that your code will be distributed under the open-source architecture of this preservation project.

*Let's work together to bypass Error 6 and unlock the garage once again!*
