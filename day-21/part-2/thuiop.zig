const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var ar = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
const allocator = ar.allocator();

const Position = struct {
    x: i4,
    y: i4,
};

fn get_pos_num(char: u8) Position {
    return switch (char) {
        48 => Position{ .x = 1, .y = 3 },
        49 => Position{ .x = 0, .y = 2 },
        50 => Position{ .x = 1, .y = 2 },
        51 => Position{ .x = 2, .y = 2 },
        52 => Position{ .x = 0, .y = 1 },
        53 => Position{ .x = 1, .y = 1 },
        54 => Position{ .x = 2, .y = 1 },
        55 => Position{ .x = 0, .y = 0 },
        56 => Position{ .x = 1, .y = 0 },
        57 => Position{ .x = 2, .y = 0 },
        65 => Position{ .x = 2, .y = 3 },
        else => unreachable,
    };
}

fn get_pos_dir(char: u8) Position {
    return switch (char) {
        60 => Position{ .x = 0, .y = 1 },
        62 => Position{ .x = 2, .y = 1 },
        94 => Position{ .x = 1, .y = 0 },
        118 => Position{ .x = 1, .y = 1 },
        65 => Position{ .x = 2, .y = 0 },
        else => unreachable,
    };
}

const KeyboardType = enum {
    Numerical,
    Directional,
};

const ResultIndex = struct {
    new_pos: Position,
    prev_pos: Position,
    rec_num: usize,
};

fn get_shortest_recur(new_pos: Position, prev_pos: Position, rec_num: usize, keyboard_type: KeyboardType, results: *std.AutoHashMap(ResultIndex, usize)) usize {
    const result_index = ResultIndex{ .new_pos = new_pos, .prev_pos = prev_pos, .rec_num = rec_num };
    if (rec_num == 0) {
        return 1;
    }
    if (results.get(result_index)) |res| {
        return res;
    }
    const xchar = if (new_pos.x < prev_pos.x) "<"[0] else ">"[0];
    const ychar = if (new_pos.y < prev_pos.y) "^"[0] else "v"[0];

    const unsafe_xfirst = switch (keyboard_type) {
        .Numerical => prev_pos.y == 3 and new_pos.x == 0,
        .Directional => prev_pos.y == 0 and new_pos.x == 0,
    };
    const unsafe_yfirst = switch (keyboard_type) {
        .Numerical => prev_pos.x == 0 and new_pos.y == 3,
        .Directional => prev_pos.x == 0 and new_pos.y == 0,
    };

    var min: usize = 10000000000000000;
    if (!unsafe_xfirst) {
        var new_seq = std.ArrayList(u8).init(allocator);
        for (0..@abs(prev_pos.x - new_pos.x)) |_| {
            new_seq.append(xchar) catch unreachable;
        }
        for (0..@abs(prev_pos.y - new_pos.y)) |_| {
            new_seq.append(ychar) catch unreachable;
        }
        new_seq.append("A"[0]) catch unreachable;
        var new_length: usize = 0;
        var prev_pos_next = get_pos_dir("A"[0]);
        for (new_seq.items) |char| {
            const new_pos_next = get_pos_dir(char);
            new_length += get_shortest_recur(new_pos_next, prev_pos_next, rec_num - 1, .Directional, results);
            prev_pos_next = new_pos_next;
        }
        if (new_length < min) {
            min = new_length;
        }
        // std.debug.print("new_seq1 {s}\n", .{new_seq.items});
    }
    if (!unsafe_yfirst) {
        var new_seq = std.ArrayList(u8).init(allocator);
        for (0..@abs(prev_pos.y - new_pos.y)) |_| {
            new_seq.append(ychar) catch unreachable;
        }
        for (0..@abs(prev_pos.x - new_pos.x)) |_| {
            new_seq.append(xchar) catch unreachable;
        }
        new_seq.append("A"[0]) catch unreachable;
        var new_length: usize = 0;
        var prev_pos_next = get_pos_dir("A"[0]);
        for (new_seq.items) |char| {
            const new_pos_next = get_pos_dir(char);
            new_length += get_shortest_recur(new_pos_next, prev_pos_next, rec_num - 1, .Directional, results);
            prev_pos_next = new_pos_next;
        }
        if (new_length < min) {
            min = new_length;
        }
        // std.debug.print("new_seq2 {s}\n", .{new_seq.items});
    }
    results.put(result_index, min) catch unreachable;
    return min;
}

fn find_sequence_length(seq: []const u8) usize {
    var prev_pos: Position = get_pos_num("A"[0]);
    var total_length: usize = 0;
    var results = std.AutoHashMap(ResultIndex, usize).init(allocator);
    for (seq) |char| {
        const new_pos = get_pos_num(char);
        total_length += get_shortest_recur(new_pos, prev_pos, 26, .Numerical, &results);
        prev_pos = new_pos;
    }
    return total_length;
}

fn run(input: [:0]const u8) usize {
    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var result: usize = 0;
    while (it.next()) |row| {
        const length = find_sequence_length(row);
        std.debug.print("{} {}\n", .{ length, std.fmt.parseInt(usize, row[0..3], 10) catch unreachable });
        result += (std.fmt.parseInt(usize, row[0..3], 10) catch unreachable) * length;
    }
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
