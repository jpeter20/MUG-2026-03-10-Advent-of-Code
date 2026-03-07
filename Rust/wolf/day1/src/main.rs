use std::{env, fs, process};

const DIAL_SIZE: i32 = 100;
const START_POSITION: i32 = 50;

struct Rotation {
    direction: i32,
    distance: i32,
}

fn parse_rotations(input: &str) -> Vec<Rotation> {
    input
        .lines()
        .filter(|line| !line.is_empty())
        .map(|line| {
            let direction = match line.as_bytes()[0] {
                b'L' => -1,
                b'R' => 1,
                c => panic!("unexpected direction '{}'", c as char),
            };
            let distance: i32 = line[1..].parse().expect("invalid distance");
            Rotation {
                direction,
                distance,
            }
        })
        .collect()
}

/// Return the number of times a rotation stops at `0`.
fn part1(rotations: &[Rotation]) -> usize {
    let mut position = START_POSITION;
    let mut count = 0;

    for r in rotations {
        // For each rotation, see where it stops.
        // `rem_euclid` gives a true modulus (always non-negative), unlike `%`
        // which preserves the dividend's sign.
        position = (position + r.direction * r.distance).rem_euclid(DIAL_SIZE);
        if position == 0 {
            count += 1;
        }
    }

    count
}

/// Return the number of times a rotation stops at **or crosses over** `0`.
fn part2(rotations: &[Rotation]) -> usize {
    let mut position = START_POSITION;
    let mut count = 0;

    for r in rotations {
        // For each rotation...
        for _ in 0..r.distance {
            // ...for each step within that rotation, see if that step lands on `0`.
            position = (position + r.direction).rem_euclid(DIAL_SIZE);
            if position == 0 {
                count += 1;
            }
        }
    }

    count
}

fn main() {
    let input_path = match env::args().nth(1) {
        Some(path) => path,
        None => {
            eprintln!("Usage: secret-entrance <input-file>");
            process::exit(1);
        }
    };

    let input = fs::read_to_string(&input_path).unwrap_or_else(|e| {
        eprintln!("Error reading {input_path}: {e}");
        process::exit(1);
    });

    let rotations = parse_rotations(&input);

    println!(
        "Part 1: from the rotations provided in {input_path}, \
         those rotations, applied in order, stop at 0 a total of {} times.",
        part1(&rotations)
    );
    println!(
        "Part 2: from the rotations provided in {input_path}, \
         those rotations, applied in order, stop at or cross over 0 a total of {} times.",
        part2(&rotations)
    );
}
