open Types
open Str

(* loads the srt file and returns a list of lines *)
let load_srt_file filename =
    let ic = open_in filename in
    let rec read_lines acc =
        try
            let line = input_line ic in
            read_lines (line :: acc)
        with End_of_file -> List.rev acc
    in
    read_lines [] in

(* takes a string and returns if it is a valid srt time *)
let match_time s =
    let time_re = Str.regexp "^[0-9]\\{2\\}:[0-9]\\{2\\}:[0-9]\\{2\\},[0-9]\\{3\\}$" in
    Str.string_match time_re s 0 in

(* takes a string and returns the time in milliseconds *)
let time_to_int time =
  try
    (* Split the timestamp into hours, minutes, seconds, and milliseconds *)
    let time_parts = Str.split (Str.regexp "[:,]") time in
    match time_parts with
    | [hours; minutes; seconds; milliseconds] ->
        let hours_ms = int_of_string hours * 60 * 60 * 1000 in
        let minutes_ms = int_of_string minutes * 60 * 1000 in
        let seconds_ms = int_of_string seconds * 1000 in
        let milliseconds = int_of_string milliseconds in
        hours_ms + minutes_ms + seconds_ms + milliseconds
    | _ -> failwith "Invalid timestamp format"
  with
  | Failure _ -> failwith "Failed to parse timestamp"

(* flattens lines into a single string list *)
let flatten_lines lines =
    let rec flatten_lines' acc = function
        | [] -> acc
        | line :: lines -> flatten_lines' (acc @ (String.split_on_char ' ' line)) lines
    in
    flatten_lines' [] lines in

(* takes a list of strings and returns a list of srt tokens *)
let tokenize_srt lst =
    let rec tokenize_srt' acc = function
        | [] -> acc
        | line :: lines ->
            if match_time line then
                let time = time_to_int line in
                tokenize_srt' (time :: acc) lines
            else
                let text = Text line in
                tokenize_srt' (text :: acc) lines
    in
    List.rev (tokenize_srt' [] lst) in
