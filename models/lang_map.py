class LangMap(dict):
    def __init__(self):
        super().__init__(
            {
                "java": "java",
                "py": "python",
                "js": "javascript",
                "cjs": "javascript",
                "njs": "javascript",
                "jsx": "javascript",
                "ts": "typescript",
                "tsx": "tsx",
                "go": "go",
                "c": "cpp",
                "h": "cpp",
                "c++": "cpp",
                "cpp": "cpp",
                "cxx": "cpp",
                "cc": "cpp",
                "cp": "cpp",
                "C": "cpp",
                "h++": "cpp",
                "hpp": "cpp",
                "hxx": "cpp",
                "xml": "xml",
                "xsl": "xml",
                "xslt": "xml",
                "xsd": "xml",
                "xaml": "xml",
                "html": "html",
                "xhtml": "html",
                "htm": "html",
                "sql": "sql",
                "sqlite": "sqlite",
                "php": "php",
                "phtml": "php",
                "kotlin": "kotlin",
                "kt": "kotlin",
                "kts": "kotlin",  # kotlin script
                "yaml": "yaml",
                "yml": "yaml",
                # # "properties": "properties",
                "cs": "c_sharp",
                "csx": "c_sharp",
                "css": "css",
                "scss": "scss",
                "less": "less",
                "vue": "vue",
                "mjs": "javascript",
                "ada": "ada",  # Ada source code file generic extension
                "adb": "ada",  # Ada main file extension, used to store program implementation part
                "ads": "ada",  # Ada specification file extension, used to store program interface part
                "agda": "agda",  # Agda is a programming language for dependent type programming
                "cls": "apex",  # File extension used to define Apex class files
                "sh": "bash",
                "beancount": "beancount",
                "capnp": "capnp",
                "clj": "clojure",
                "cljs": "clojure",
                "cljc": "clojure",
                "lisp": "commonlisp",
                "lsp": "commonlisp",
                "cu": "cuda",
                "cuh": "cuda",  # CUDA header file, similar to .h file
                "dart": "dart",
                "d": "d",
                "di": "d",  # D language interface file, usually used to define files that only contain declarations, not implementation
                "dot": "dot",
                "ex": "elixir",
                "exs": "elixir",  # This extension is used to write Elixir script files
                "elm": "elm",
                "el": "elisp",
                # "eno": "eno",
                "erb": "embedded_template",
                "ejs": "embedded_template",
                "erl": "erlang",
                "hrl": "erlang",  # File extension for header files, usually used to store macro definitions and shared data structures in Erlang
                "fnl": "fennel",
                "fish": "fish",
                "f": "formula",  # Traditional Fortran 77 source code file extension, used to include fixed format Fortran source code.
                "frm": "formula",
                "f90": "fortran",
                "f95": "fortran",
                "f03": "fortran",
                "f08": "fortran",
                "for": "fortran",
                "gitattributes": "gitattributes",
                "gitignore": "gitignore",
                "gleam": "gleam",
                "glsl": "glsl",
                "vert": "glsl",
                "frag": "glsl",
                "graphql": "graphql",
                "hack": "hack",
                "hh": "hack",
                "hhi": "hack",
                "hs": "haskell",
                "lhs": "haskell",
                "hcl": "hcl",
                "ispc": "ispc",
                "jq": "jq",
                "json": "json",
                "json5": "json5",
                "jl": "julia",
                "just": "just",
                "lalrpop": "lalrpop",
                "tex": "latex",
                "sty": "latex",
                "lean": "lean",
                "ll": "llvm",
                "bc": "llvm",
                "td": "tablegen",
                "lua": "lua",
                "magik": "magik",
                "make": "make",
                "md": "markdown",
                "meson": "meson",
                "m68k": "m68k",
                "nim": "nim",
                "nix": "nix",
                "noir": "noir",
                "objc": "objc",
                "ml": "ocaml",
                "mli": "ocaml",
                "odin": "odin",
                "org": "org",
                "p4": "p4",
                "pas": "pascal",
                "pl": "perl",
                "pgn": "pgn",
                "ps1": "powershell",
                "psm1": "powershell",  # PowerShell module file, usually used to package and organize PowerShell functions
                "proto": "proto",
                "qmljs": "qmljs",
                "qc": "quakec",
                "rkt": "racket",
                "rasi": "rasi",
                "re2c": "re2c",
                "regex": "regex",
                "rego": "rego",
                "rst": "rst",
                "r": "r",
                "R": "r",
                "rs": "rust",
                "robot": "robot",
                "scm": "scheme",
                # "sexp": "sexp",
                "smali": "smali",
                "sp": "sourcepawn",
                "sparql": "sparql",
                "sc": "supercollider",
                "tact": "tact",
                "thrift": "thrift",
                "toml": "toml",  # Cargo.toml: Cargo project configuration file
                "ttl": "turtle",
                "ungrammar": "ungrammar",
                "usd": "usd",
                "v": "verilog",
                "vh": "verilog",  # Verilog header file extension
                "sv": "verilog",  # SystemVerilog source code file extension
                "svh": "verilog",  # SystemVerilog source code file extension
                "vhdl": "vhdl",
                "wasm": "wast",
                "wat": "wast",
                "wast": "wast",
                "wdl": "wdl",
                "wgsl": "wgsl",
                "yang": "yang",
                "yuck": "yuck",
                "zig": "zig",
                "zig_test": "zig",  # Extension used to write Zig test files
                "svelte": "svelte",
            }
        )

    def __getitem__(self, key: str):
        if key.startswith("."):
            return super().__getitem__(key[1:])
        return super().__getitem__(key)

    def __contains__(self, key: str):
        if key.startswith("."):
            return super().__contains__(key[1:])
        return super().__contains__(key)

    def get(self, key: str):
        if key.startswith("."):
            return super().get(key[1:])
        return super().get(key)


lang_map = LangMap()
