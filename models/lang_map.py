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
                "ada": "ada",  # Ada源代码文件的通用扩展名
                "adb": "ada",  # Ada的主体文件扩展名，用于存放程序的实现部分
                "ads": "ada",  # Ada的规范文件扩展名，用于存放程序的接口部分
                "agda": "agda",  # Agda 是一种用于依赖类型编程的编程语言
                "cls": "apex",  # 用于定义 Apex 类的文件扩展名
                "sh": "bash",
                "beancount": "beancount",
                "capnp": "capnp",
                "clj": "clojure",
                "cljs": "clojure",
                "cljc": "clojure",
                "lisp": "commonlisp",
                "lsp": "commonlisp",
                "cu": "cuda",
                "cuh": "cuda",  # CUDA 头文件，类似于 .h 文件
                "dart": "dart",
                "d": "d",
                "di": "d",  # D 语言接口文件，通常用于定义只包含声明的文件，不包含实现
                "dot": "dot",
                "ex": "elixir",
                "exs": "elixir",  # 这个扩展名用于编写 Elixir 脚本文件
                "elm": "elm",
                "el": "elisp",
                # "eno": "eno",
                "erb": "embedded_template",
                "ejs": "embedded_template",
                "erl": "erlang",
                "hrl": "erlang",  # 头文件的扩展名，通常用于存放 Erlang 中的宏定义和共享的数据结构等
                "fnl": "fennel",
                "fish": "fish",
                "f": "formula",  # 传统的 Fortran 77 源代码文件扩展名，用于包含固定格式的 Fortran 源代码。
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
                "psm1": "powershell",  # PowerShell 模块文件，通常用于封装和组织 PowerShell 函数
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
                "toml": "toml",  # Cargo.toml: Cargo 项目配置文件
                "ttl": "turtle",
                "ungrammar": "ungrammar",
                "usd": "usd",
                "v": "verilog",
                "vh": "verilog",  # Verilog头文件的扩展名
                "sv": "verilog",  # SystemVerilog源代码文件的扩展名
                "svh": "verilog",  # SystemVerilog源代码文件的扩展名
                "vhdl": "vhdl",
                "wasm": "wast",
                "wat": "wast",
                "wast": "wast",
                "wdl": "wdl",
                "wgsl": "wgsl",
                "yang": "yang",
                "yuck": "yuck",
                "zig": "zig",
                "zig_test": "zig",  # 用于编写 Zig 测试文件的扩展名
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
