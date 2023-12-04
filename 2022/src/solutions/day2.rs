use std::{
    fs::File,
    io::{BufRead, BufReader},
};

enum Outcome {
    Lose, // X  0
    Draw, // Y  3
    Win,  // Z  6
}
impl Outcome {
    fn from_char(char: &str) -> Option<Outcome> {
        match char {
            "X" => Some(Outcome::Lose),
            "Y" => Some(Outcome::Draw),
            "Z" => Some(Outcome::Win),
            _ => None,
        }
    }
}

#[derive(PartialEq, Eq, Debug)]
enum Hand {
    Rock,    // 1
    Paper,   // 2
    Scissor, // 3
}

impl Hand {
    fn from_char(char: &str) -> Option<Hand> {
        match char {
            "A" => Some(Hand::Rock),
            "B" => Some(Hand::Paper),
            "C" => Some(Hand::Scissor),
            _ => None,
        }
    }

    /// Returns the points given for choosing this hand, 1, 2 or 3
    fn choice_point(&self) -> usize {
        *self as usize + 1
    }

    fn get_points_from_outcome(&self, outcome: &Outcome) -> usize {
        match outcome {
            Outcome::Win => {
                match self {
                    Hand::Paper => &Hand::Scissor,
                    Hand::Rock => &Hand::Paper,
                    Hand::Scissor => &Hand::Rock,
                }
                .choice_point()
                    + 6
            }
            Outcome::Lose => {
                match self {
                    Hand::Scissor => &Hand::Paper,
                    Hand::Paper => &Hand::Rock,
                    Hand::Rock => &Hand::Scissor,
                }
                .choice_point() // + 0
            }
            Outcome::Draw => self.choice_point() + 3,
        }
    }
}

pub fn solution() {
    let path = File::open("data/day2.txt").unwrap();
    let reader = BufReader::new(path);
    let mut total: usize = 0;
    for line in reader.lines() {
        let hand_str = line.expect("Something went wrong reading lines");
        let (their_hand_str, outcome_str) = hand_str
            .split_once(' ')
            .expect("Failed splitting hand string");
        let their_hand = Hand::from_char(their_hand_str).expect("Failed parsing their hand");
        let outcome = Outcome::from_char(outcome_str).expect("Failed parsing outcome");
        let points = their_hand.get_points_from_outcome(&outcome);
        total += points;
    }
    println!("1: {:?}", total)
}
