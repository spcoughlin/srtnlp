open Types
open Str
open Tokenize_srt

(* Takes a list of srt tokens and returns a list of strings up to the first time token *)
let strings_til_time tokens =
    let rec strings_til_time' tokens acc =
        match tokens with
        | [] -> acc
        | Time t -> acc
        | Text s -> strings_til_time' (List.tl tokens) (acc @ [s])
    in strings_til_time' tokens []

(* Takes a list of srt tokens and returns an srt = (int * string list ) list *)
let parse_srt tokens =
    let rec parse_srt' tokens acc =
        match tokens with
        | [] -> acc
        | Time t ->
            let next_strings = (* TODO *)
            
