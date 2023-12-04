// use itertools::Itertools;
use crossterm::{cursor, terminal, ExecutableCommand};
use std::io::{stdout, Write};
use std::{
    collections::HashSet,
    fs::File,
    io::{BufRead, BufReader},
    ops::Sub,
    path::Path,
};

#[derive(Eq, Hash, PartialEq, PartialOrd, Debug, Clone)]
struct Point {
    x: isize,
    y: isize,
}
impl Point {
    fn new() -> Point {
        Point { x: 0, y: 0 }
    }

    /// Return true if this point is touching (can be diagonal) or overlapping a point
    fn is_touching(&self, other: &Point) -> bool {
        self == other || ((self.x - other.x).abs() <= 1 && (self.y - other.y).abs() <= 1)
    }
}

impl Sub for Point {
    type Output = Self;

    fn sub(self, other: Self) -> Self::Output {
        Self {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

struct Rope {
    segments: Vec<Point>,
    tail_positions: HashSet<Point>,
}

impl Rope {
    fn new(length: usize) -> Rope {
        let body = vec![Point::new(); length + 1];
        Rope {
            segments: body,
            tail_positions: HashSet::new(),
        }
    }

    fn go_up(&mut self) {
        self.segments[0].y += 1;
        self.move_body()
    }

    fn go_down(&mut self) {
        self.segments[0].y -= 1;
        self.move_body()
    }

    fn go_left(&mut self) {
        self.segments[0].x -= 1;
        self.move_body()
    }

    fn go_right(&mut self) {
        self.segments[0].x += 1;
        self.move_body()
    }

    fn move_body(&mut self) {
        let mut previous_index = 0;
        for current_index in 1..self.segments.len() {
            if !self.segments[current_index].is_touching(&self.segments[previous_index]) {
                // H not touching S, move to touching position
                let x_diff = self.segments[previous_index].x - self.segments[current_index].x; // {-2, -1, 0, 1, 2}
                let y_diff = self.segments[previous_index].y - self.segments[current_index].y; // {-2, -1, 0, 1, 2}
                                                                                               // println!("{}: {:?} - {:?}", current_index, x_diff, y_diff);
                // if x_diff.abs() > 2 || y_diff.abs() > 2 {
                //     panic!(
                //         "Something went wrong moving segments!: {} {} {:?} {:?}",
                //         x_diff, y_diff, self.segments[previous_index], self.segments[current_index]
                //     )
                // }

                if x_diff.abs() == 2 {
                    self.segments[current_index].x += x_diff;
                    if y_diff != 0 {
                        self.segments[current_index].y += y_diff
                    }
                } else if y_diff.abs() == 2 {
                    self.segments[current_index].y += y_diff;
                    if x_diff != 0 {
                        self.segments[current_index].x += x_diff
                    }
                }
                self.draw()
            }
            previous_index = current_index;
        }
        self.tail_positions.insert(Point {
            x: self.segments.iter().last().expect("No tail found").x,
            y: self.segments.iter().last().expect("No tail found").y,
        });
    }
    fn draw(&self) {
        let rows = 20;
        let cols = 20;
       let mut stdout = stdout(); // lock stdout and use the same locked instance throughout
        stdout.execute(cursor::MoveUp((rows as u16) * 2)).unwrap();
        stdout
            .execute(terminal::Clear(terminal::ClearType::FromCursorDown))
            .unwrap();
        for i in -rows..rows {
            let mut row: Vec<char> = Vec::new();
            for j in (-cols..cols).rev() {
                if (i, j) == (0, 0) {
                    row.push('s')
                } else if self.segments[0] == (Point { x: i, y: j }) {
                    row.push('H')
                } else if self.segments[self.segments.len() - 1] == (Point { x: i, y: j }) {
                    row.push('#')
                } else if self.segments.contains(&Point { x: i, y: j }) {
                    row.push(
                        char::from_digit(
                            self.segments
                                .iter()
                                .position(|p| p == &Point { x: i, y: j })
                                .unwrap() as u32,
                            10,
                        )
                        .unwrap(),
                    )
                } else {
                    row.push('.')
                }
            }
            let row_str: String = row.into_iter().collect();
            writeln!(stdout, "{}", row_str).unwrap();
        }

        // wait 2 seconds before replacing lines
        std::thread::sleep(std::time::Duration::from_millis(100));
    }

    fn draw_tail(&self) {
        for y in (-20..20).rev() {
            for x in -20..20 {
                if self.tail_positions.contains(&(Point { x, y })) {
                    print!("#")
                } else {
                    print!(".")
                }
            }
            print!("\n")
        }
        print!("\n")
    }
}

// fn move_adjacent(tail: &Point, head: &Point) -> Option<Point> {
//     let dx = tail.x - head.x;
//     let dy = tail.y - head.y;

//     if (dx == 2 || dx == -2) && (dy == 2 || dy == -2) {
//         Some(Point {x: head.x + dx.clamp(-1, 1), y: head.y + dy.clamp(-1, 1)})
//     } else if dx == 2 || dx == -2 {
//         Some(Point {x: head.x + dx.clamp(-1, 1), head.y})
//     } else if dy == 2 || dy == -2 {
//         Some((head.x, Point {x:}ead.y + dy.clamp(-1, 1)})
//     } else {
//         None // already adjacent
//     }
// }

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day9.txt");
    let reader = BufReader::new(File::open(base).unwrap());
    let mut rope = Rope::new(9);
    rope.tail_positions.insert(Point { x: 0, y: 0 });

    let lines = reader.lines();
    for line in lines {
        let line_str = line.expect("");
        // println!("{:?}", line_str);
        let (direction, moves) = line_str.split_once(' ').expect("No split");
        if direction == "U" {
            for _ in 0..moves.parse::<usize>().expect("Moves not a number") {
                rope.go_up();
            }
        } else if direction == "D" {
            for _ in 0..moves.parse::<usize>().expect("Moves not a number") {
                rope.go_down();
            }
        } else if direction == "L" {
            for _ in 0..moves.parse::<usize>().expect("Moves not a number") {
                rope.go_left();
            }
        } else if direction == "R" {
            for _ in 0..moves.parse::<usize>().expect("Moves not a number") {
                rope.go_right();
            }
        }
    }
    rope.draw_tail();
    println!("positions: {:?}", rope.tail_positions.len())
}

#[cfg(test)]
mod tests {
    // use super::get_segment_direction;

    use crate::solutions::day9::Point;

    #[test]
    fn test_segment_mover() {
        // [0,0] - [0,2] -> [0,1]
        // assert_eq!(get_segment_direction(0, 0, 0, 2), (0,1);)
        // [0,0] - [-2,0] -> [-1,0]
        let p1 = Point { x: 5, y: 5 };
        let p2 = Point { x: 5, y: 7 };
        let d = p1 - p2;
        if d.x.abs() == 2 {}
        let move_x = d.x / 2;
        // let x1: isize = 0;
        // let x2: isize = -1;
        println!("{:?}", d);
    }
}
