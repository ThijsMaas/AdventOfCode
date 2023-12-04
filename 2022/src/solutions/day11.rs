use std::{
    collections::VecDeque,
    fs::{read_to_string, File},
    io::{BufRead, BufReader},
    path::Path,
};

use itertools::Itertools;
use regex::Regex;

struct Monkeys {
    monkeys: Vec<Monkey>,
}

impl Monkeys {}

#[derive(Debug)]
struct Monkey {
    items: VecDeque<usize>,
    op: char,
    op_value: Option<usize>,
    divisible_value: usize,
    true_throw: usize,
    false_throw: usize,
    total_throws: usize,
}

impl Monkey {
    fn new(
        items: VecDeque<usize>,
        op: char,
        op_value: Option<usize>,
        divisible_value: usize,
        true_throw: usize,
        false_throw: usize,
    ) -> Monkey {
        Monkey {
            items,
            op,
            op_value,
            divisible_value,
            true_throw,
            false_throw,
            total_throws: 0,
        }
    }

    fn pop_and_inspect(&mut self, modulo: usize) -> usize {
        let item = self.items.pop_front().expect("No items to pop");
        let other = match self.op_value {
            Some(value) => value,
            None => item.clone(),
        };
        let mod_item = match &self.op {
            '+' => item.wrapping_add(other),
            '*' => item.wrapping_mul(other),
            _ => panic!("Op not supported"),
        };
        mod_item % modulo
    }

    fn throw(&self, item: usize) -> usize {
        if item % self.divisible_value == 0 {
            self.true_throw
        } else {
            self.false_throw
        }
    }
}

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day11.txt");
    let pattern = Regex::new(r"  Starting items: (.*)\n  Operation: new = old ([\+\*]) (\d+|old)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)").unwrap();

    let mut monkeys: Vec<Monkey> = Vec::new();
    let rounds = 10000;

    let file_str = read_to_string(base).expect("Could not read file contents");
    for cap in pattern.captures_iter(&file_str) {
        let items: VecDeque<usize> = cap[1]
            .split(", ")
            .map(|i| i.parse::<usize>().expect("item not a number"))
            .collect();
        let op = cap[2].chars().next().unwrap();
        let op_value = cap[3].parse::<usize>().ok();
        let divisible_value = cap[4].parse::<usize>().expect("Cant parse divisible str");
        let true_throw = cap[5].parse::<usize>().expect("Cant parse true str");
        let false_throw = cap[6].parse::<usize>().expect("Cant parse false str");
        monkeys.push(Monkey::new(
            items,
            op,
            op_value,
            divisible_value,
            true_throw,
            false_throw,
        ))
    }

    println!("{:?}", monkeys);

    // let part1_modulo = 3;
    let part2_modulo = monkeys
        .iter()
        .map(|m| m.divisible_value)
        .reduce(|a, b| a * b)
        .unwrap();


    for round in 0..rounds {
        for i in 0..monkeys.len() {
            while monkeys[i].items.len() > 0 {
                let item = monkeys[i].pop_and_inspect(part2_modulo);
                let to_monkey = monkeys[i].throw(item);
                monkeys[to_monkey].items.push_back(item);
                monkeys[i].total_throws += 1;
                if round % 20 == 0 {}
            }
        }
    }
    println!(
        "{:?}",
        monkeys
            .iter()
            .map(|m| m.total_throws)
            .collect::<Vec<usize>>()
    );
    let monkey_business = monkeys
        .iter()
        .map(|m| m.total_throws)
        .sorted()
        .rev()
        .collect::<Vec<usize>>();

    println!("{:?}", monkey_business[0] * monkey_business[1]);
}
