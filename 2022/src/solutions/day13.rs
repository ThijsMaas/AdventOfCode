// // use itertools::Itertools;
// use std::{collections::VecDeque, fs::read_to_string, path::Path};

// use serde_json::{Value, Number};

// pub fn solution() {
//     let base = Path::new(env!("CARGO_MANIFEST_DIR")).join("data/example.txt");
//     // let mut data = String::new();
//     // reader.read_line(&mut data).expect("");
//     let file_str = read_to_string(base).expect("Could not read file contents");

//     let mut pair_results = Vec::new();
//     // let t = serde_json::number::Number;
//     let zero = Value::Number(PosInt(0));

//     // let zero_value = Value::Null;
//     'pairs: for pair in file_str.split("\n\n") {
//         let (l1, l2) = pair.split_once("\n").unwrap();
//         let left: Value = serde_json::from_str(&l1).unwrap();
//         let right: Value = serde_json::from_str(&l2).unwrap();

//         let left_len = left.as_array().unwrap().len();
//         let right_len = right.as_array().unwrap().len();

//         // println!("{:?}", left[1]);
//         // println!("{:?}", left[1].as_u64());
//         // println!("{:?}", left[1].as_array());

//         for i in 0..left_len {
//             let mut to_compare = VecDeque::new();
//             to_compare.push_back((left[i].clone(), right[i].clone()));
//             while let Some((left_item, right_item)) = to_compare.pop_front() {
//                 let result = match (left_item.as_u64(), right_item.as_u64()) {
//                     // Both are ints, compare them
//                     (Some(left_int), Some(right_int)) => correct(left_int, right_int),
//                     // Both are not ints, convert to array
//                     (_, _) => {
//                         let left_array = left_item.as_array().expect("Shit");
//                         let right_array = right_item.as_array().expect("Shit");
//                         for i in 0..left_array.len().max(right_array.len()) {
//                             to_compare.push_back((
//                                 left_array.get(i).unwrap_or(&Value::Null).clone(),
//                                 right_array.get(i).unwrap_or(&Value::Null).clone()
//                             ));
//                         };
//                         None
//                     }
//                 };
//                 if result.is_some() {
//                     pair_results.push(resdef main():
//     input_file = "data/day1.txt"
//     with open(input_file) as f:
//         weights = [
//             sum(map(int, weight_str.split())) for weight_str in f.read().split("\n\n")
//         ]
//         print(max(weights))


// if __name__ == "__main__":
//     main()
// ult.unwrap());
//                     continue 'pairs
//                 }
//             }
//         }
//     }
//     println!("{:?}", pair_results)
// }

// fn correct(left: u64, right: u64) -> Option<bool> {
//     if left < right {
//         return Some(true);
//     } else if left > right {
//         return Some(false);
//     }
//     None
// }

// // fn parse_items(list_str: &str) {
// //     let items = Vec::new();
// //     let inner_str = &list_str[1..list_str.len()-1];

// // }
