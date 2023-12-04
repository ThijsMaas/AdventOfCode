// use itertools::Itertools;
use std::{
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
};

fn get_visible_trees(sight: Vec<u32>, tree: u32) -> usize {
    let mut visible = 0;
    for t in sight {
        if t < tree {
            visible += 1;
        } else if t >= tree {
            visible += 1;
            break;
        }
    }
    visible
}

pub fn solution() {
    let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/day8.txt");
    let reader = BufReader::new(File::open(base).unwrap());
    let lines = reader.lines();

    let mut forest = Vec::new();
    let mut visible_trees: usize = 0;
    let mut scenic_scores = Vec::new();

    // Store the trees in a matrix
    for line in lines {
        let row: Vec<u32> = line
            .expect("No line")
            .chars()
            .map(|c| c.to_digit(10).expect("Not a digit"))
            .collect();
        forest.push(row);
    }
    let forest_length = forest.len();
    let forest_width = forest[0].len();

    // Iterate over every row and column
    for x in 0..forest_width {
        'tree: for y in 0..forest_length {
            if x == 0 || y == 0 || x == forest_width - 1 || y == forest_length - 1 {
                visible_trees += 1;
                continue 'tree;
            }
            let tree_len = forest[x][y];
            // Part 1
            // Check for higher or equal trees in 4 directions
            let largest_tree_left = (0..x).map(|i| forest[i][y]).max().expect("No trees");
            let largest_tree_right = (x + 1..forest_width)
                .map(|i| forest[i][y])
                .max()
                .expect("No trees");
            let largest_tree_top = (0..y).map(|i| forest[x][i]).max().expect("No trees");
            let largest_tree_bottom = (y + 1..forest_length)
                .map(|i| forest[x][i])
                .max()
                .expect("No trees");
            if [
                largest_tree_bottom,
                largest_tree_top,
                largest_tree_right,
                largest_tree_left,
            ]
            .iter()
            .any(|t| tree_len > *t)
            {
                visible_trees += 1
            }

            // Part 2
            let visible_trees_left =
                get_visible_trees((0..x).map(|i| forest[i][y]).rev().collect(), tree_len);
            let visible_trees_right = get_visible_trees(
                (x + 1..forest_width).map(|i| forest[i][y]).collect(),
                tree_len,
            );
            let visible_trees_top =
                get_visible_trees((0..y).map(|i| forest[x][i]).rev().collect(), tree_len);
            let visible_trees_bottom = get_visible_trees(
                (y + 1..forest_length).map(|i| forest[x][i]).collect(),
                tree_len,
            );
            scenic_scores.push(
                visible_trees_left * visible_trees_right * visible_trees_top * visible_trees_bottom,
            )
        }
    }
    println!(
        "visible_trees: {:?}\nscenic_score: {:?}",
        visible_trees,
        scenic_scores.iter().max().expect("No scores")
    );
}
