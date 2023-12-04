use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

fn to_priority(byte: u8) -> u8 {
    if byte < 97 {
        byte - 65 + 1 + 26
    } else {
        byte - 97 + 1
    }
}

pub fn solution() {
    // let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day3.txt");
    // let reader = BufReader::new(File::open(base).unwrap());
    // let mut priority_sum: usize = 0;
    // for line in reader.lines() {
    //     let items_str = line.expect("Something went wrong reading lines");
    //     let items = items_str.as_bytes();

    //     let items_comp1 = &items[..((items.len() - 1) / 2) + 1];
    //     let items_comp2 = &items[((items.len() - 1) / 2) + 1..];
    //     let shared = items_comp1.iter().filter(|i| items_comp2.contains(i)).next().expect("No shared item found");
    //     let shared_item_priority = to_priority(*shared);
    //     priority_sum += shared_item_priority as usize;
    //     // println!("{:?} {:?}", shared, shared_item_priority);
    // }
    // println!("{:?}", priority_sum)

    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day3.txt");
    let reader = BufReader::new(File::open(base).unwrap());
    let mut priority_sum: usize = 0;
    let mut lines = reader.lines();

    loop {
        let line = lines.next();
        if let Some(elf1_line) = line {
            let elf1 = elf1_line.unwrap();
            let elf2 = lines
                .next()
                .expect("Something went wrong reading lines")
                .unwrap();
            let elf3 = lines
                .next()
                .expect("Something went wrong reading lines")
                .unwrap();

            let elf1_items = elf1.as_bytes();
            let elf2_items = elf2.as_bytes();
            let elf3_items = elf3.as_bytes();

            let shared = elf1_items
                .iter()
                .find(|i| elf2_items.contains(i) && elf3_items.contains(i))
                .expect("No shared item found");
            let shared_item_priority = to_priority(*shared);
            priority_sum += shared_item_priority as usize;
        } else {
            break;
        }
    }

    println!("{:?}", priority_sum)
}
