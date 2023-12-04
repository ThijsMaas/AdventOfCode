use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day4.txt");
    let reader = BufReader::new(File::open(base).unwrap());

    let mut counts: usize = 0;

    for line in reader.lines() {
        let line_str = line.expect("Something went wrong reading lines");
        let (sections_1, sections_2) = line_str
            .split_once('-')
            .expect("Sections are not splitting");
        let range_1_str = sections_1
            .split_once('-')
            .expect("Sections are not splitting");
        let range_2_str = sections_2
            .split_once('-')
            .expect("Sections are not splitting");
        let set_1: HashSet<usize> = (range_1_str
            .0
            .parse::<usize>()
            .expect("Section can not be parsed")
            ..=range_1_str
                .1
                .parse::<usize>()
                .expect("Section can not be parsed"))
            .collect();
        let set_2: HashSet<usize> = (range_2_str
            .0
            .parse::<usize>()
            .expect("Section can not be parsed")
            ..=range_2_str
                .1
                .parse::<usize>()
                .expect("Section can not be parsed"))
            .collect();
        // let result: Vec<&usize> = set_1.intersection(&set_2).collect();
        if set_1.intersection(&set_2).next().is_none() {
            counts += 1;
        }
    }
    println!("counts: {}", counts);
}
