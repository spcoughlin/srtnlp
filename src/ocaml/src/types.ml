(* CFG Basics *)
type terminal = string
type nonterminal = string
type symbol = 
    | T of terminal 
    | NT of nonterminal
type production_rule = {
    lhs: nonterminal;
    rhs: symbol list;
}
type grammar = {
    start: nonterminal;
    terminals: terminal list;
    nonterminals: nonterminal list;
    rules: production_rule list;
}
type lexicon = (terminal * nonterminal) list

(* srt file parsing *)
type srt_token =
    | Time of int
    | Text of string
type srt = (int * string list) list
type grammar_tokenized_srt = (int * terminal list) list

