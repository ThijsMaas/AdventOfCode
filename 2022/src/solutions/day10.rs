use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

struct Clock {
    cycle: isize,
    x: isize,
    draw_position: usize,
}

impl Clock {
    fn new() -> Clock {
        Clock {
            cycle: 1,
            x: 1,
            draw_position: 0,
        }
    }

    fn tick(&mut self) {
        self.draw();
        self.cycle += 1;
    }

    fn add_x(&mut self, value: isize) {
        self.x += value;
    }

    fn draw(&mut self) {
        if self.sprite_overlap() {
            print!("#");
        } else {
            print!(".");
        }
        self.draw_position += 1;
        if self.draw_position == 40 {
            print!("\n");
            self.draw_position = 0;
        }
    }

    fn sprite_overlap(&self) -> bool {
        (self.x - self.draw_position as isize).abs() <= 1
    }
}

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day10.txt");
    let reader = BufReader::new(File::open(base).unwrap());
    let mut cycle = Clock::new();

    let lines = reader.lines();
    for line in lines {
        let line_str = line.expect("No line?");
        if line_str == "noop" {
            cycle.tick();
        } else {
            let value = line_str[5..].parse::<isize>().expect("Not a number?");
            cycle.tick();
            cycle.tick();
            cycle.add_x(value);
        }
    }
}
