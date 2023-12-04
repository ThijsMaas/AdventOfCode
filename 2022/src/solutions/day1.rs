use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day1.txt");
    let reader = BufReader::new(File::open(base).unwrap());

    let mut weights: Vec<usize> = Vec::new();
    let mut elf_weight: usize = 0;

    for line in reader.lines() {
        let calorie_str = line.expect("Something went wrong reading lines");
        if calorie_str == *"" {
            weights.push(elf_weight);
            elf_weight = 0;
        } else {
            elf_weight += calorie_str
                .parse::<usize>()
                .expect("Something went wrong parsing weight to int");
        }
    }

    println!("{:?}", weights.iter().max().expect("No weights were found"));

    weights.sort();
    weights.reverse();
    let total: usize = weights[..3].iter().sum();

    println!("{:?}", total)
}
