import os
import sys
from fnmatch import fnmatch

# Supported languages and their extensions for tree-sitter-language-pack.
# See: https://github.com/Goldziher/tree-sitter-language-pack
lang_extensions = {
    "actionscript": ["as"],
    "ada": ["ada", "adb", "ads"],
    "agda": ["agda"],
    "apex": ["cls", "trigger"],
    "arduino": ["ino"],
    "asm": ["asm", "s", "S"],
    "astro": ["astro"],
    "bash": ["sh"],
    "beancount": ["beancount", "bean"],
    "bibtex": ["bib"],
    "bicep": ["bicep"],
    "bitbake": ["bb", "bbclass", "bbappend", "inc"],
    "c_sharp": ["cs", "csx"],
    "cairo": ["cairo"],
    "capnp": ["capnp"],
    "chatito": ["chatito"],
    "clarity": ["clar"],
    "clojure": ["clj", "cljs", "cljc"],
    "cmake": ["cmake"],
    "comment": [],
    "commonlisp": ["lisp", "lsp"],
    "cpon": [],
    "cpp": ["c", "h", "c++", "cpp", "cxx", "cc", "cp", "C", "h++", "hpp", "hxx"],
    "css": ["css"],
    "csv": ["csv"],
    "cuda": ["cu", "cuh"],
    "d": ["d", "di"],
    "dart": ["dart"],
    "dockerfile": [],
    # "dot": ["dot"],
    "doxygen": [],
    "elisp": ["el"],
    "elixir": ["ex", "exs"],
    "elm": ["elm"],
    "embedded_template": ["erb", "ejs"],
    "erlang": ["erl", "hrl"],
    "fennel": ["fnl"],
    "firrtl": ["fir"],
    "fish": ["fish"],
    "fortran": ["f90", "f95", "f03", "f08", "for"],
    "func": ["fun"],
    # "formula": ["f", "frm"],
    "gdscript": ["gd"],
    "gitattributes": ["gitattributes"],
    "gitcommit": [],
    "gitignore": ["gitignore"],
    "gleam": ["gleam"],
    "glsl": ["glsl", "vert", "frag", "comp"],
    "gn": ["gn", "gni"],
    "go": ["go"],
    "gomod": [],
    "gosum": [],
    "groovy": ["groovy", "gvy", "gy", "gsh"],
    "gstlaunch": ["gst"],
    # "graphql": ["graphql"],
    "hack": ["hack", "hh", "hhi"],
    "hare": ["ha"],
    "haskell": ["hs", "lhs"],
    "haxe": ["hx"],
    "hcl": ["hcl"],
    "heex": ["heex"],
    "hlsl": ["hlsl"],
    "html": ["html", "xhtml", "htm"],
    "hyprlang": [],
    "ispc": ["ispc"],
    "janet": ["janet"],
    "java": ["java"],
    "javascript": ["js", "cjs", "mjs", "njs", "jsx"],
    "jsdoc": [],
    "json": ["json"],
    "jsonnet": ["jsonnet", "libsonnet"],
    # "json5": ["json5"],
    # "jq": ["jq"],
    "julia": ["jl"],
    # "just": ["just"],
    "kconfig": [],
    "kdl": ["kdl"],
    "kotlin": ["kotlin", "kt", "kts"],
    # "lalrpop": ["lalrpop"],
    # "latex": ["tex", "sty"],
    # "lean": ["lean"],
    # "less": ["less"],
    "linkerscript": ["ld"],
    "llvm": ["ll", "bc"],
    "lua": ["lua"],
    "luadoc": [],
    "luap": ["luap"],
    "luau": ["luau"],
    # "m68k": ["m68k"],
    "magik": ["magik"],
    "make": ["mak"],
    "markdown": ["md"],
    "matlab": ["m", "mat"],
    "mermaid": ["mmd", "mermaid"],
    "meson": ["meson"],
    "ninja": ["ninja"],
    # "nim": ["nim"],
    "nix": ["nix"],
    # "noir": ["noir"],
    "nqc": ["nqc"],
    "objc": ["objc"],
    # "ocaml": ["ml", "mli"],
    "odin": ["odin"],
    "org": ["org"],
    # "p4": ["p4"],
    "pascal": ["pas"],
    "pem": ["pem"],
    "perl": ["pl"],
    "pgn": ["pgn"],
    "php": ["php", "phtml"],
    "po": ["po", "pot"],
    "pony": ["pony"],
    "powershell": ["ps1", "psd1", "psm1"],
    "printf": [],
    "prisma": ["prisma"],
    "properties": ["properties"],
    "proto": ["proto"],
    "psv": ["psv"],
    "puppet": ["pp"],
    "purescript": ["purs"],
    "pymanifest": [],
    "python": ["py", "pyi", "pyx", "pxd"],
    "qmldir": ["qmldir"],
    # "qmljs": ["qmljs"],
    # "quakec": ["qc"],
    "query": ["qry", "rq"],
    "r": ["r", "R"],
    "racket": ["rkt"],
    # "rasi": ["rasi"],
    "rbs": ["rbs"],
    "re2c": ["re2c"],
    "readline": ["inputrc"],
    # "regex": ["regex"],
    # "rego": ["rego"],
    "requirements": [],
    # "robot": ["robot"],
    "ron": ["ron"],
    "rst": ["rst"],
    "ruby": ["rb", "rake", "gemspec"],
    "rust": ["rs"],
    "scala": ["scala"],
    "scheme": ["scm"],
    "scss": ["sass", "scss"],
    "slang": ["slang"],
    "smali": ["smali"],
    "smithy": ["smithy"],
    "solidity": ["sol"],
    # "sourcepawn": ["sp"],
    "sparql": ["sparql"],
    "sql": ["sql"],
    # "sqlite": ["sqlite"],
    "squirrel": ["nut"],
    "starlark": ["star", "bzl"],
    # "supercollider": ["sc"],
    "svelte": ["svelte"],
    "swift": ["swift"],
    "tablegen": ["td"],
    # "tact": ["tact"],
    "tcl": ["tcl", "tk"],
    "test": ["test"],
    "thrift": ["thrift"],
    "toml": ["toml"],
    # "tsx": ["tsx"],
    "tsv": ["tsv"],
    "twig": ["twig"],
    # "turtle": ["ttl"],
    "typescript": ["ts"],
    "typst": ["typ"],
    "udev": ["rules"],  # (in /etc/udev/rules.d/)
    "ungrammar": ["ungrammar"],
    # "usd": ["usd"],
    "uxntal": ["tal"],
    "v": ["vv"],
    "verilog": ["v", "vh", "sv", "svh"],
    "vhdl": ["vhdl"],
    "vim": ["vim", "vimrc"],
    "vue": ["vue"],
    # "wast": ["wasm", "wat", "wast"],
    # "wdl": ["wdl"],
    "wgsl": ["wgsl"],
    "xcompose": ["XCompose", "xcompose"],
    "xml": ["xml", "xsl", "xslt", "xsd", "xaml"],
    "yaml": ["yaml", "yml"],
    # "yang": ["yang"],
    "yuck": ["yuck"],
    "zig": ["zig", "zig_test"],
}

# Show exported languages in language menu
supported_languages = sorted(lang_extensions.keys())


class ExtToLangMap(dict):
    def __init__(self):
        for lang, extensions in lang_extensions.items():
            if not extensions:
                continue
            if not isinstance(extensions, (list, tuple)):
                extensions = [extensions]
            for ext in extensions:
                if ext not in self:
                    self[ext] = lang
                else:
                    print(
                        "Language '{}' and '{}' have duplicate extension '{}'".format(
                            self[ext], lang, ext
                        ),
                        file=sys.stderr,
                    )
                    continue

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


class FileToLangMap(dict):
    def __init__(self):
        super().__init__(
            {
                "cmakelists.txt": "cmake",
                "cmakelists": "cmake",
                "commit_editmsg": "gitcommit",
                "go.mod": "gomod",
                "go.sum": "gosum",
                "hyprland.conf": "hyprlang",
                "kconfig": "kconfig",
                "manifest.in": "pymanifest",
                "requirements.txt": "requirements",
                "makefile": "make",
                "readme": "markdown",
                "license": "markdown",
                "copying": "markdown",
                "changelog": "markdown",
                "dockerfile": "dockerfile",
            }
        )
        self.globs = {}
        for file, lang in self.items():
            if "*" in file:
                self.globs[file] = lang

    def __getitem__(self, key: str):
        """
        Implements [] operator.
        """
        key = key.lower()
        if super().__contains__(key):
            return super().__getitem__(key)
        if self.globs:
            for k, v in self.globs.items():
                if fnmatch.fnmatch(key, k):
                    return v

    def __contains__(self, key: str):
        """
        Implements in operator, such as: "if 'key' in map"
        """
        key = key.lower()
        if super().__contains__(key):
            return True
        if self.globs:
            for k, _v in self.globs.items():
                if fnmatch.fnmatch(key, k):
                    return True
        return False

    def get(self, key: str):
        """
        Implements get() method.
        """
        key = key.lower()
        if super().__contains__(key):
            return super().get(key)
        if self.globs:
            for k, v in self.globs.items():
                if fnmatch.fnmatch(key, k):
                    return v
        return None


ext_to_lang_map = ExtToLangMap()
file_to_lang_map = FileToLangMap()


def get_language(file_path: str) -> str:
    file_name = os.path.basename(file_path)
    lang = None
    if "." in file_name:
        ext = file_name.split(".")[-1]
        if ext and ext in ext_to_lang_map:
            lang = ext_to_lang_map.get(ext)
    if not lang and file_name in file_to_lang_map:
        lang = file_to_lang_map.get(file_name)
    print(f"lang: {lang}", file=sys.stderr)
    return lang
