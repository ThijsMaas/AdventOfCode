use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

fn accumulate(sizes: Vec<usize>) -> Vec<usize> {
    let mut accu = Vec::new();
    let mut iter = sizes.iter();
    let mut total = *iter.next().unwrap();
    for size in iter {
        total += size;
        accu.push(total)
    }
    accu
}

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day7.txt");
    let reader = BufReader::new(File::open(base).unwrap());
    let lines = reader.lines();

    let mut stack: Vec<usize> = Vec::new();
    let mut sizes: Vec<usize> = Vec::new();

    for line in lines {
        let line_str = line.expect("There is no line");
        if line_str.starts_with(&"$ cd ..".to_string()) {
            let size = stack.pop().unwrap();
            sizes.push(size);
            let stack_len = stack.len();
            stack[stack_len - 1] += size;
        } else if line_str.starts_with(&"$ cd ".to_string()) {
            stack.push(0);
        } else if let Ok(size) = line_str.split_once(' ').unwrap().0.parse::<usize>() {
            let stack_len = stack.len();
            stack[stack_len - 1] += size;
        }
    }
    // println!("{:?} {:?}", sizes, stack);
    stack.reverse();
    sizes.extend(accumulate(stack));

    // Part1
    // let size_limit: usize = 100_000;
    // println!("{:?}", sizes.iter().filter(|s|s <= &&size_limit).sum::<usize>())

    // Part2
    let space_needed: usize = 40_000_000;
    let x = sizes.iter().max().unwrap() - space_needed;
    println!("{:?}", sizes.iter().filter(|s| s >= &&x).min().unwrap())
}
