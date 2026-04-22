[README.md](https://github.com/user-attachments/files/26989665/README.md)
CoinShell — A Numismatic Query Engine
-------------------------------------

CoinShell is a Python-based command-line application that allows users to query a coin database using both structured commands and natural-language-style input.

### Features

*   Dual parsing system:
    
    *   Explicit command parser (monarch george v and silver)
        
    *   Natural language parser (george v silver)
        
*   Alias normalization using external CSV files (e.g. “william rufus” → “William II”)
    
*   SQL-backed query engine with:
    
    *   Filtering
        
    *   Sorting
        
    *   Aggregation (count)
        
    *   Random selection (random)
        
    *   Result limiting (limit)
        
*   Modular architecture:
    
    *   parser.py – query parsing
        
    *   db.py – database execution
        
    *   helpers.py – reusable utilities
        
    *   config.py – project configuration
        
*   Interactive shell:
    
    *   Command history (↑ key)
        
    *   Tab completion
        
    *   Built-in help system
        
*   User-friendly output formatting
    

### Example Usage

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   > victoria pennyShowing 3 results.> silver sort year limit 5Showing 5 results (out of 23 matching).> monarch george v count12 matching coins.> randomShowing 1 result.   `

### Getting Started

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   git clone https://github.com/YOURNAME/coinshell.gitcd coinshellpython3 coinshell.py   `

### Project Structure

Explain briefly (just like above tree).

### Why this project?

This project was designed to explore:

*   building a domain-specific query language
    
*   parsing structured and semi-natural input
    
*   separating data, logic, and configuration
    
*   creating a reusable backend for future applications (e.g. GUI tools or games)
