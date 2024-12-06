const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]const u8) i64 {
    var constraints: [100][100]bool = std.mem.zeroes([100][100]bool);

    var it = std.mem.splitScalar(u8, input, '\n');
    while (it.next()) |x| {
        if (x[2] != "|"[0]) {
            break;
        }
        const i = std.fmt.parseInt(usize, x[0..2], 10) catch unreachable;
        const j = std.fmt.parseInt(usize, x[3..5], 10) catch unreachable;
        constraints[i][j] = true;
    }
    var numbers: [50]usize = undefined;
    var total: usize = 0;
    while (it.next()) |update| {
        var pages = std.mem.splitScalar(u8, update, ',');
        var i: usize = 0;
        var unsafe: bool = false;
        while (pages.next()) |page| {
            numbers[i] = std.fmt.parseInt(usize, page, 10) catch unreachable;
            for (numbers[0..i]) |prev_number| {
                if (constraints[numbers[i]][prev_number]) {
                    unsafe = true;
                }
            }
            i += 1;
        }
        if (!unsafe) {
            continue;
        } else {
            for (0..i) |x| {
                for (x + 1..i) |y| {
                    if (constraints[numbers[y]][numbers[x]]) {
                        const tmp = numbers[x];
                        numbers[x] = numbers[y];
                        numbers[y] = tmp;
                    }
                }
            }
            total += numbers[i / 2];
        }
    }
    const result: i64 = @intCast(total);
    return result;
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
