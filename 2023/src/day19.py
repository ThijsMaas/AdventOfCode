#!/usr/bin/env python3

from dataclasses import dataclass
import operator
import profile
import re
from typing import NamedTuple


EXAMPLE_INPUT = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int


class PartRange(NamedTuple):
    start: int
    end: int

    def __contains__(self, value: int):
        return self.start <= value <= self.end


@dataclass
class Rule:
    cat: str
    op: callable
    value: int
    next_workflow: str


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    otherwise: str


def test_part(part: Part, workflows: dict[str, Workflow]):
    next_workflow = workflows["in"]
    while True:
        for rule in next_workflow.rules:
            value: int = getattr(part, rule.cat)
            if rule.op(value, rule.value):
                next_name = rule.next_workflow
                break
        else:
            next_name = next_workflow.otherwise
        if next_name == "A":
            return True
        elif next_name == "R":
            return False
        else:
            next_workflow = workflows[next_name]


def part_1(input_text: str):
    print("Part 1")
    workflows: dict[str, Workflow] = {}
    workflows_string, ratings_string = input_text.split("\n\n")
    for workflow_string in workflows_string.split("\n"):
        name, rules_string = workflow_string.split("{")
        rules = []
        rule_parts = rules_string[:-1].split(",")
        for rule_string in rule_parts[:-1]:
            cat, op, value, next_workflow = re.match(r"(\w)([<>])(\d+):(\w+)", rule_string).groups()

            rules.append(Rule(cat, operator.lt if op == "<" else operator.gt, int(value), next_workflow))
        otherwise = rule_parts[-1]
        workflow = Workflow(name, rules, otherwise)
        workflows[name] = workflow

    accepted_parts = []
    for rating in ratings_string.strip().split("\n"):
        part = Part(*map(int, re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", rating).groups()))
        if test_part(part, workflows):
            accepted_parts.append(part)

    # Sum accepted part values
    print(sum(part.x + part.m + part.a + part.s for part in accepted_parts))


def part_2(input_text: str):
    print("Part 2")
    workflows: dict[str, Workflow] = {}
    workflows_string, _ = input_text.split("\n\n")
    for workflow_string in workflows_string.split("\n"):
        name, rules_string = workflow_string.split("{")
        rules = []
        rule_parts = rules_string[:-1].split(",")
        for rule_string in rule_parts[:-1]:
            cat, op, value, next_workflow = re.match(r"(\w)([<>])(\d+):(\w+)", rule_string).groups()

            rules.append(Rule(cat, operator.lt if op == "<" else operator.gt, int(value), next_workflow))
        otherwise = rule_parts[-1]
        workflow = Workflow(name, rules, otherwise)
        workflows[name] = workflow

    part_ranges = []

    # Initialize the queue
    queue = [
        (
            {"x": PartRange(1, 4000), "m": PartRange(1, 4000), "a": PartRange(1, 4000), "s": PartRange(1, 4000)},
            "in",
        )
    ]

    while queue:
        part, workflow_name = queue.pop(0)

        if workflow_name == "A":
            part_ranges.append(part)
            continue
        elif workflow_name == "R":
            continue

        workflow = workflows[workflow_name]
        for rule in workflow.rules:
            if (rule.op == operator.lt and part[rule.cat].end < rule.value) or (
                rule.op == operator.gt and part[rule.cat].start > rule.value
            ):
                # Completely inside, add next_workflow to queue and finish this workflow
                queue.append((part, rule.next_workflow))
                break
            elif (rule.op == operator.lt and part[rule.cat].start > rule.value) or (
                rule.op == operator.gt and part[rule.cat].end < rule.value
            ):
                # Completely outside, go to next rule or otherwise
                continue
            else:
                # Part needs to be split
                part_inside_range = part.copy()
                part_outside_range = part.copy()
                if rule.op == operator.lt:
                    part_inside_range[rule.cat] = PartRange(part[rule.cat].start, rule.value - 1)
                    part_outside_range[rule.cat] = PartRange(rule.value, part[rule.cat].end)
                else:
                    part_inside_range[rule.cat] = PartRange(rule.value + 1, part[rule.cat].end)
                    part_outside_range[rule.cat] = PartRange(part[rule.cat].start, rule.value)

                queue.append((part_inside_range, rule.next_workflow))
                part = part_outside_range
        else:
            queue.append((part, workflow.otherwise))

    combinations = sum(
        (part["x"].end - part["x"].start + 1)
        * (part["m"].end - part["m"].start + 1)
        * (part["a"].end - part["a"].start + 1)
        * (part["s"].end - part["s"].start + 1)
        for part in part_ranges
    )
    print(combinations)


def solution(input_text: str, part_number: int):
    if part_number == 1:
        part_1(input_text)
    elif part_number == 2:
        part_2(input_text)
    else:
        raise ValueError(f"Invalid part number: {part_number}")
