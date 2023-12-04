use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

type Stack = Vec<char>;

struct Stacks {
    stacks: Vec<Stack>,
}

impl Stacks {
    fn get_last_crates(&mut self) -> Vec<char> {
        self.stacks.iter_mut().map(|c| c.pop().unwrap()).collect()
    }

    // fn move_crate(&mut self, from_stack: usize, to_stack: usize) {
    //     let moved_crate = self.stacks[from_stack].pop().unwrap();
    //     self.stacks[to_stack].push(moved_crate);
    // }

    fn move_multiple_crates(&mut self, from_stack: usize, to_stack: usize, amount: usize) {
        let mut moved_crates = Vec::new();
        for _ in 0..amount {
            moved_crates.push(self.stacks[from_stack].pop().unwrap());
        }
        moved_crates.reverse();

        self.stacks[to_stack].extend(moved_crates.iter());
    }

    fn add_crate(&mut self, crate_char: char, to_stack: usize) {
        if self.stacks.len() <= to_stack {
            // if stack does not exist yet
            for i in 0..=to_stack {
                // create new stacks for each previous, if not existing
                if self.stacks.get(i) == None {
                    self.stacks.push(Vec::new())
                }
            }
        }
        self.stacks[to_stack].push(crate_char);
    }

    fn reverse_stacks(&mut self) {
        self.stacks.iter_mut().for_each(|stack| stack.reverse())
    }
}

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day5.txt");
    let reader = BufReader::new(File::open(base).unwrap());

    let mut stacks = Stacks { stacks: Vec::new() };
    let lines = reader.lines();

    for line in lines {
        let line_str = line.expect("Something went wrong reading lines");
        if line_str.starts_with("move") {
            //move 'move 1 from 2 to 1'
            let numbers: Vec<&str> = line_str.split_whitespace().skip(1).step_by(2).collect();
            let amount = numbers[0]
                .parse::<usize>()
                .expect("Problem parsing move number");
            let from = numbers[1]
                .parse::<usize>()
                .expect("Problem parsing move number");
            let to = numbers[2]
                .parse::<usize>()
                .expect("Problem parsing move number");
            // Part 1
            // for _ in 0..amount {
            //     stacks.move_crate(from - 1, to - 1)
            // }
            // Part 2
            stacks.move_multiple_crates(from - 1, to - 1, amount)
        } else if line_str.starts_with(" 1") {
            // Done with setup
            stacks.reverse_stacks()
        } else {
            let crate_chars_to_add: Vec<char> = line_str.chars().skip(1).step_by(4).collect();
            // println!("adding {:?}", crate_chars_to_add);
            crate_chars_to_add
                .iter()
                .enumerate()
                .filter(|(_, crate_)| crate_ != &&' ')
                .for_each(|(i, crate_)| stacks.add_crate(*crate_, i));
        }
    }
    println!("{:?}", stacks.stacks);

    println!(
        "crates: {:?}",
        stacks.get_last_crates().iter().collect::<String>()
    );
}
