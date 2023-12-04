// use itertools::Itertools;
use std::{
    collections::{HashMap, HashSet, VecDeque},
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

type Point = (usize, usize);

type Graph = HashMap<Point, Vec<Point>>;

pub fn bfs(start: Point, end: Point, nodes: Graph) -> Option<usize> {
    let mut queue = VecDeque::new();
    let mut visited = HashSet::new();

    // Visit start
    queue.push_back((0, start));
    visited.insert(start);
    while let Some((distance, node)) = queue.pop_front() {
        let neighbors = nodes.get(&node).unwrap();
        // println!("n {:?} {:?}", node, distance);
        // println!("v {:?}", visited);
        // println!("nei {:?}", neighbors);
        for neighbor in neighbors {
            if visited.insert(*neighbor) {
                if neighbor == &end {
                    return Some(distance + 1);
                }
                queue.push_back((distance + 1, *neighbor))
            }
        }
    }
    Some(visited.len())
}

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day12.txt");
    let reader = BufReader::new(File::open(base).unwrap());

    let mut rows = Vec::new();
    let mut start = (0, 0);
    let mut end = (0, 0);

    let lines = reader.lines();
    for (y, line) in lines.enumerate() {
        let line_str = line.expect("Something went wrong reading lines");
        let mut row_chars = line_str.chars().collect::<Vec<char>>();
        if let Some(start_x) = row_chars.iter().position(|c| c == &'S') {
            start = (start_x, y);
            row_chars[start_x] = 'a'
        }
        if let Some(end_x) = row_chars.iter().position(|c| c == &'E') {
            end = (end_x, y);
            row_chars[end_x] = 'z'
        }
        rows.push(row_chars);
    }
    println!("start: {:?} end: {:?}", start, end);

    // build graph
    println!("Building graph..");
    let mut node_graph: Graph = HashMap::new();
    let n_rows = rows.len();
    let n_cols = rows[0].len();
    for x in 0..n_cols {
        for y in 0..n_rows {
            let node: Point = (x, y);
            let mut neighbors = Vec::new();
            if x != 0 && node_in_reach(rows[y][x - 1], rows[y][x]) {
                // left
                neighbors.push((x - 1, y))
            }
            if x != n_cols - 1 && node_in_reach(rows[y][x + 1], rows[y][x]) {
                // right
                neighbors.push((x + 1, y))
            }
            if y != 0 && node_in_reach(rows[y - 1][x], rows[y][x]) {
                // up
                neighbors.push((x, y - 1))
            }
            if y != n_rows - 1 && node_in_reach(rows[y + 1][x], rows[y][x]) {
                // down
                neighbors.push((x, y + 1))
            }
            if !neighbors.is_empty() {
                node_graph.insert(node, neighbors);
            }
        }
    }
    println!("Solving graph..");

    let distance = bfs(start, end, node_graph);
    println!("distance: {:?}", distance);
}

fn node_in_reach(c1: char, c2: char) -> bool {
    // c1.to_string().as_bytes()[0].abs_diff(c2.to_string().as_bytes()[0]) <= 1
    c1.to_string().as_bytes()[0] == c2.to_string().as_bytes()[0]
        || c1.to_string().as_bytes()[0] == c2.to_string().as_bytes()[0] + 1
}
