const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Direction = enum {
    left,
    right,
    up,
    down,
};

const Position = struct {
    i: usize,
    j: usize,

    fn get_next(pos: Position, dir: Direction) Position {
        var new_pos: Position = .{ .i = pos.i, .j = pos.j };
        switch (dir) {
            Direction.up => new_pos.j -= 1,
            Direction.down => new_pos.j += 1,
            Direction.left => new_pos.i -= 1,
            Direction.right => new_pos.i += 1,
        }
        return new_pos;
    }

    fn is_not_out(pos: Position, length: usize) bool {
        return pos.i != 0 and pos.i != length - 2 and pos.j != 0 and pos.j != length - 2;
    }

    fn get_val(pos: Position, comptime T: type, array: []T, row_length: usize) T {
        return array[pos.i + pos.j * row_length];
    }

    fn set_val(pos: Position, comptime T: type, value: T, array: *[]T, row_length: usize) void {
        array.*[pos.i + pos.j * row_length] = value;
    }
};

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator;
    const total_length: f32 = @floatFromInt(input.len);
    const row_length: usize = @intFromFloat(@sqrt(total_length) + 1);

    var direction = Direction.up;
    const initial_index = std.mem.indexOf(u8, input, "^").?;
    var pos: Position = .{ .i = initial_index % row_length, .j = initial_index / row_length };
    var visited = allocator.alloc(bool, input.len) catch unreachable;
    var visit_count: i64 = 0;

    while (pos.is_not_out(row_length)) {
        if (!pos.get_val(bool, visited, row_length)) {
            pos.set_val(bool, true, &visited, row_length);
            visit_count += 1;
        }
        const new_pos = pos.get_next(direction);
        if (new_pos.get_val(u8, @constCast(input), row_length) == "#"[0]) {
            direction = switch (direction) {
                Direction.up => Direction.right,
                Direction.right => Direction.down,
                Direction.down => Direction.left,
                Direction.left => Direction.up,
            };
        } else {
            pos = new_pos;
        }
    }
    return visit_count + 1;
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
