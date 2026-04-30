"""Pygments lexer for STARLIMS Scripting Language (SSL v11)."""

__all__ = ["SSLLexer"]

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import (
    Comment, Keyword, Literal, Name, Number, Operator, Punctuation,
    String, Text, Token,
)


class SSLLexer(RegexLexer):
    name = "SSL"
    aliases = ["ssl"]
    filenames = ["*.ssl"]

    # Colon-prefixed control-flow and declaration keywords
    _keywords = (
        ":BEGINCASE", ":CASE", ":OTHERWISE", ":EXITCASE", ":ENDCASE",
        ":CLASS", ":ENDCLASS",
        ":CONSTRUCTOR",
        ":DECLARE",
        ":DEFAULT",
        ":ELSE", ":ELSEIF",
        ":ERROR",
        ":EXITFOR", ":EXITWHILE",
        ":FINALLY",
        ":FOR", ":TO", ":STEP", ":NEXT",
        ":IF", ":ENDIF",
        ":INCLUDE",
        ":LABEL",
        ":LOOP",
        ":PARAMETERS",
        ":PRIVATE", ":PROTECTED",
        ":PROCEDURE", ":ENDPROC",
        ":PUBLIC",
        ":REGION", ":ENDREGION",
        ":BEGININLINECODE", ":ENDINLINECODE",
        ":RESUME",
        ":RETURN",
        ":TRY", ":CATCH", ":ENDTRY",
        ":WHILE", ":ENDWHILE",
    )

    tokens = {
        "root": [
            # Whitespace
            (r"\s+", Text.Whitespace),

            # Comments: /* text ; (semicolon terminates)
            (r"/\*[^;]*;", Comment.Single),

            # Boolean / NIL literals (case-insensitive handled by IGNORECASE flag)
            (r"(?i)\.T\.", Keyword.Constant),
            (r"(?i)\.F\.", Keyword.Constant),
            (r"(?i)\bNIL\b", Keyword.Constant),

            # Colon-prefixed keywords (case-sensitive, uppercase)
            (words(_keywords, suffix=r"\b"), Keyword),

            # Class-context identifiers
            (r"(?i)\b(Me|Base|Constructor)\b", Name.Builtin.Pseudo),

            # Strings
            (r'"[^"]*"', String.Double),

            # Numbers
            (r"\b\d+\.\d+\b", Number.Float),
            (r"\b\d+\b", Number.Integer),

            # Logical word operators (case-insensitive)
            (r"(?i)\.(AND|OR|NOT|XOR)\.", Operator.Word),

            # Compound assignment operators
            (r"\*\*=|\+=|-=|\*=|/=|%=", Operator),

            # Comparison / arithmetic operators
            (r"==|!=|<>|<=|>=|:=|[+\-*/%<>=]|\*\*|\$|#", Operator),

            # Member-access colon (standalone, not part of keyword)
            (r":", Punctuation),

            # Punctuation
            (r"[(){}\[\],;]", Punctuation),

            # Identifiers — function calls and variables
            (r"[A-Za-z_][A-Za-z0-9_]*(?=\s*\()", Name.Function),
            (r"[A-Za-z_][A-Za-z0-9_]*", Name),
        ],
    }
