use itertools::Itertools;
use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day6.txt");
    let mut reader = BufReader::new(File::open(base).unwrap());
    let mut data = String::new();
    reader.read_line(&mut data).expect("");

    let data_slice = data.as_bytes();
    let window_size = 14;

    for i in window_size..data_slice.len() {
        let window = &mut data_slice[i - window_size..i].to_vec();
        window.sort();
        let unique_window_size = window.iter().dedup().count();
        if unique_window_size == window.len() {
            println!("{:?}", i);
            break;
        }
    }
}
