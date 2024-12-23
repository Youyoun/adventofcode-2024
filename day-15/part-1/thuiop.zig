const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Position = struct {
    i: usize,
    j: usize,

    fn next(self: Position, dir: Direction) Position {
        return Position{ .i = @addWithOverflow(self.i, @as(usize, @bitCast(dir.i)))[0], .j = @addWithOverflow(self.j, @as(usize, @bitCast(dir.j)))[0] };
    }
};

const Direction = struct {
    i: i64,
    j: i64,
};

fn push(pos: Position, dir: Direction, room_array: *[]u8, row_length: usize) bool {
    const next_pos = pos.next(dir);
    var array = room_array.*;
    switch (array[next_pos.i + row_length * next_pos.j]) {
        "."[0] => {
            array[next_pos.i + row_length * next_pos.j] = array[pos.i + row_length * pos.j];
            array[pos.i + row_length * pos.j] = "."[0];
            return true;
        },
        "#"[0] => return false,
        "O"[0] => {
            if (push(next_pos, dir, room_array, row_length)) {
                array[next_pos.i + row_length * next_pos.j] = array[pos.i + row_length * pos.j];
                array[pos.i + row_length * pos.j] = "."[0];
                return true;
            } else {
                return false;
            }
        },
        else => unreachable,
    }
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    defer arena.deinit(); // clear memory
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const row_length = it.peek().?.len;
    var room_array = allocator.alloc(u8, row_length * row_length) catch unreachable;

    var i: usize = 0;
    while (it.next()) |row| {
        if (row.len == 0) {
            break;
        }
        @memcpy(room_array[i * row_length .. (i + 1) * row_length], row);
        i += 1;
    }

    const index = std.mem.indexOf(u8, room_array, "@").?;
    var pos = Position{ .i = index % row_length, .j = index / row_length };

    while (it.next()) |row| {
        for (row) |command| {
            const dir: Direction = switch (command) {
                "^"[0] => Direction{ .i = 0, .j = -1 },
                ">"[0] => Direction{ .i = 1, .j = 0 },
                "v"[0] => Direction{ .i = 0, .j = 1 },
                "<"[0] => Direction{ .i = -1, .j = 0 },
                else => unreachable,
            };
            const push_success = push(pos, dir, &room_array, row_length);
            if (push_success) {
                pos = pos.next(dir);
            }
        }
    }
    var result: i64 = 0;
    for (0..row_length - 1) |k| {
        for (0..row_length - 1) |l| {
            if (room_array[k + l * row_length] == "O"[0]) {
                result += @intCast(l * 100 + k);
            }
        }
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
