use std::env;

mod solutions;
use crate::solutions::*;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        panic!("Expected a argument like 'day1'");
    }
    match args[1].as_str() {
        "day1" => day1::solution(),
        "day2" => day2::solution(),
        "day3" => day3::solution(),
        "day4" => day4::solution(),
        "day5" => day5::solution(),
        "day6" => day6::solution(),
        "day7" => day7::solution(),
        "day8" => day8::solution(),
        "day9" => day9::solution(),
        "day10" => day10::solution(),
        "day11" => day11::solution(),
        "day12" => day12::solution(),
        // "day13" => day13::solution(),
        "day14" => day14::solution(),
        "day15" => day15::solution(),
        "day16" => day16::solution(),
        "day17" => day17::solution(),
        "day18" => day18::solution(),
        "day19" => day19::solution(),
        "day20" => day20::solution(),
        "day21" => day21::solution(),
        "day22" => day22::solution(),
        "day23" => day23::solution(),
        "day24" => day24::solution(),
        "day25" => day25::solution(),
        _ => panic!("Argument not supported"),
    }
}
