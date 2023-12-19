/*
    Author: Thijs Maas
*/

const COOKIE_FILE = `${Bun.env.HOME}/.config/aocd/token`;
const CACHE_DIR = `${Bun.env.HOME}/.cache/aocd`;

const helpText = `\
Usage: bun solve <day> [option]
Options:
    <day>       The day to run [1-25]
    i, init     Initialize the day by creating a new file with template code
    e, example  Run the example input for the specified day
`;

const errorProgram = (errorMessage: string) => {
    console.error(errorMessage);
    console.log(helpText);
    process.exit(1);
};

const fetchInput = async (day: string, cookie: string) => {
    // Check if input is already cached
    const cacheFile = `${CACHE_DIR}/2021_${day}_input.txt`;
    const cacheExists = await Bun.file(cacheFile).exists();
    if (cacheExists) {
        return await Bun.file(cacheFile).text();
    }
    // Else fetch input
    const inputText = await fetch(`https://adventofcode.com/2021/day/${day}/input`, {
        headers: {
            cookie: `session=${cookie}`,
        },
    }).then((res) => res.text());
    // Cache input
    await Bun.write(cacheFile, inputText);
    return inputText;
};

const main = async () => {
    // Read cookie from file
    const cookie = await Bun.file(COOKIE_FILE).text();
    const days = [...Array(25).keys()];

    // Parse arguments
    const args = Bun.argv.slice(2);

    if (args.length === 0) {
        errorProgram('Please provide a day number');
    } else {
        const day = args[0];

        if (!days.includes(parseInt(day))) {
            errorProgram('Please provide a valid day number as first argument');
        }

        // Initialize day
        if (args.length === 2 && ['i', 'init'].includes(args[1])) {
            const template = await Bun.file('./src/template.ts').text();
            const dayFile = `./src/day${day}.ts`;
            if (await Bun.file(dayFile).exists()) {
                errorProgram(`File ${dayFile} already exists`);
            }
            console.log(`Initializing day ${day}`);
            await Bun.write(dayFile, template);
            return;
        }

        // Run day
        let dayModule;
        try {
            dayModule = await import(`./src/day${day}`);
        } catch {
            errorProgram(`Day ${day} not yet initialized`);
        }

        if (args.length === 2 && ['e', 'example'].includes(args[1])) {
            console.log(`Running example for day ${day}`);
            const input = dayModule.EXAMPLE_INPUT;
            dayModule.solution(input);
        } else {
            console.log(`Running solution for day ${day}`);
            const input = await fetchInput(day, cookie);
            dayModule.solution(input);
        }
    }
};

main();
