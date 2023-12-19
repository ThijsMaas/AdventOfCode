/*
    Author: Thijs Maas
*/

export const EXAMPLE_INPUT = `
199
200
208
210
200
207
240
269
260
263
`;

const partOne = (input: string) => {
    const numbers = input.trim().split('\n').map((line) => parseInt(line));
    const numberIncreasing = numbers.slice(1).map((number, index) => number > numbers[index]).filter(Boolean).length;
    return numberIncreasing
}

const partTwo = (input: string) => {
    const numbers = input.trim().split('\n').map((line) => parseInt(line));
    const windowSize = 3
    const windows = numbers.slice(0, numbers.length - windowSize + 1).map((number, index) => numbers.slice(index, index + windowSize).reduce((a, c) => a + c, 0));
    const numberIncreasing = windows.slice(1).map((window, index) => window > windows[index]).filter(Boolean).length;
        
    return numberIncreasing
}

export const solution = (input: string) => {
    console.log('Part 1:');
    console.log(partOne(input));
    console.log('Part 2:');
    console.log(partTwo(input));
};
