const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Position = struct {
    i: usize,
    j: usize,

    fn is_not_out(pos: Position, length: usize) bool {
        return pos.i >= 0 and pos.i <= length - 1 and pos.j >= 0 and pos.j <= length - 1;
    }

    fn get_val(pos: Position, comptime T: type, array: []T, row_length: usize) T {
        return array[pos.i + pos.j * row_length];
    }

    fn set_val(pos: Position, comptime T: type, value: T, array: *[]T, row_length: usize) void {
        array.*[pos.i + pos.j * row_length] = value;
    }
};

const Antenna = struct {
    i: usize,
    j: usize,
    type: u8,
};

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator;
    var it = std.mem.splitScalar(u8, input, '\n');
    var j: usize = 0;
    var antenna_list = std.ArrayList(Antenna).init(allocator);
    const length = it.peek().?.len;
    while (it.next()) |row| {
        for (0..row.len, row) |i, x| {
            if (x == "."[0]) {
                continue;
            } else {
                antenna_list.append(Antenna{ .i = i, .j = j, .type = x }) catch unreachable;
            }
        }
        j += 1;
    }

    var antinode_count: i64 = 0;
    var antinodes = allocator.alloc(bool, length * length) catch unreachable;
    @memset(antinodes, false);
    for (antenna_list.items) |antenna_1| {
        for (antenna_list.items) |antenna_2| {
            if (antenna_1.type == antenna_2.type and !std.meta.eql(antenna_1, antenna_2)) {
                const antinode_pos = Position{ .i = antenna_2.i + (antenna_2.i - antenna_1.i), .j = antenna_2.j + (antenna_2.j - antenna_1.j) };
                if (antinode_pos.is_not_out(length) and !antinode_pos.get_val(bool, antinodes, length)) {
                    antinode_count += 1;
                    antinode_pos.set_val(bool, true, &antinodes, length);
                }
            }
        }
    }
    return antinode_count;
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
