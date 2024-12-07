const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn parseRules(input: []const u8) struct { std.AutoHashMap(i64, std.ArrayList(i64)), std.AutoHashMap(i64, std.ArrayList(i64)) } {
    var before_rules = std.AutoHashMap(i64, std.ArrayList(i64)).init(a);
    var after_rules = std.AutoHashMap(i64, std.ArrayList(i64)).init(a);

    var it = std.mem.splitScalar(u8, input, '\n');
    while (it.next()) |str| {
        var it2 = std.mem.splitScalar(u8, str, '|');
        const n1 = std.fmt.parseInt(i64, it2.next().?, 10) catch unreachable;
        const n2 = std.fmt.parseInt(i64, it2.next().?, 10) catch unreachable;

        const gop1 = before_rules.getOrPut(n2) catch unreachable;
        if (!gop1.found_existing) {
            gop1.value_ptr.* = std.ArrayList(i64).init(a);
        }
        gop1.value_ptr.append(n1) catch unreachable;

        const gop2 = after_rules.getOrPut(n1) catch unreachable;
        if (!gop2.found_existing) {
            gop2.value_ptr.* = std.ArrayList(i64).init(a);
        }
        gop2.value_ptr.append(n2) catch unreachable;
    }

    return .{ before_rules, after_rules };
}

fn parseOrdering(input: []const u8, numbers: *std.ArrayList(i64)) void {
    var it = std.mem.splitScalar(u8, input, ',');
    while (it.next()) |str| {
        const n = std.fmt.parseInt(i64, str, 10) catch unreachable;
        numbers.append(n) catch unreachable;
    }
}

fn run(input: [:0]const u8) i64 {
    var it = std.mem.splitSequence(u8, input, "\n\n");
    const first_part = it.next().?;
    const second_part = it.next().?;

    const before_rules, const after_rules = parseRules(first_part);
    _ = before_rules; // autofix

    var it2 = std.mem.splitScalar(u8, second_part, '\n');
    var numbers = std.ArrayList(i64).init(a);
    while (it2.next()) |str| {
        numbers.clearRetainingCapacity();
        parseOrdering(str, &numbers);

        var is_valid: bool = false;
        _ = is_valid; // autofix
        for (0..numbers.items.len - 1) |i| {
            const n = numbers.items[i];
            const rule = after_rules.get(n) orelse continue;
            _ = rule; // autofix
            for (i..numbers.items.len) |j| {
                const n2 = numbers.items[j];
                _ = n2; // autofix
            }
        }
    }

    // your code here
    return 0;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory
    a = arena.allocator();

    var arg_it = try std.process.argsWithAllocator(a);
    _ = arg_it.skip(); // skip over exe name
    const input: [:0]const u8 = arg_it.next().?;

    const start: i128 = std.time.nanoTimestamp(); // start time
    const answer = run(input); // compute answer
    const end: i128 = std.time.nanoTimestamp();
    const elapsed_nano: f64 = @floatFromInt(end - start);
    const elapsed_milli = elapsed_nano / 1_000_000.0;
    try stdout.print("_duration:{d}\n{}\n", .{ elapsed_milli, answer }); // emit actual lines parsed by AOC
}

test "example" {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory
    a = arena.allocator();

    const input =
        \\47|53
        \\97|13
        \\97|61
        \\97|47
        \\75|29
        \\61|13
        \\75|53
        \\29|13
        \\97|29
        \\53|29
        \\61|53
        \\97|53
        \\61|29
        \\47|13
        \\75|47
        \\97|75
        \\47|61
        \\75|61
        \\47|29
        \\75|13
        \\53|13
        \\
        \\75,47,61,53,29
        \\97,61,53,29,13
        \\75,29,13
        \\75,97,47,61,53
        \\61,13,29
        \\97,13,75,29,47
    ;

    const result = run(input);
    try std.testing.expectEqual(@as(i64, 18), result);
}
