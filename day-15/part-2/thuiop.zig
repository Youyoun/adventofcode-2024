const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Position = struct {
    i: usize,
    j: usize,

    fn next(self: Position, dir: Direction) Position {
        return Position{ .i = self.i + @as(usize, @bitCast(dir.i)), .j = self.j + @as(usize, @bitCast(dir.j)) };
    }
};

const Direction = struct {
    i: i64,
    j: i64,
};

fn push(pos: Position, dir: Direction, room_array: *[]u8, row_length: usize, dry: bool) bool {
    const next_pos = pos.next(dir);
    const horizontal = dir.i != 0;
    var array = room_array.*;
    switch (array[next_pos.i + row_length * next_pos.j]) {
        "."[0] => {
            if (!dry) {
                array[next_pos.i + row_length * next_pos.j] = array[pos.i + row_length * pos.j];
                array[pos.i + row_length * pos.j] = "."[0];
            }
            return true;
        },
        "#"[0] => return false,
        "["[0], "]"[0] => |char| {
            if (horizontal) {
                if (push(next_pos, dir, room_array, row_length, dry)) {
                    if (!dry) {
                        array[next_pos.i + row_length * next_pos.j] = array[pos.i + row_length * pos.j];
                        array[pos.i + row_length * pos.j] = "."[0];
                    }
                    return true;
                } else {
                    return false;
                }
            } else {
                const other_pos = switch (char) {
                    "["[0] => Position{ .i = next_pos.i + 1, .j = next_pos.j },
                    "]"[0] => Position{ .i = next_pos.i - 1, .j = next_pos.j },
                    else => unreachable,
                };
                if (push(next_pos, dir, room_array, row_length, true) and push(other_pos, dir, room_array, row_length, true)) {
                    _ = push(next_pos, dir, room_array, row_length, dry);
                    _ = push(other_pos, dir, room_array, row_length, dry);
                    if (!dry) {
                        array[next_pos.i + row_length * next_pos.j] = array[pos.i + row_length * pos.j];
                        array[pos.i + row_length * pos.j] = "."[0];
                        array[other_pos.i + row_length * other_pos.j] = array[pos.i + row_length * pos.j];
                        array[pos.i + row_length * pos.j] = "."[0];
                    }
                    return true;
                } else {
                    return false;
                }
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
    const length = it.peek().?.len;
    const row_length = length * 2;
    var room_array = allocator.alloc(u8, length * row_length) catch unreachable;

    var j: usize = 0;
    while (it.next()) |row| {
        if (row.len == 0) {
            break;
        }
        for (0..length, row) |i, char| {
            switch (char) {
                "@"[0] => {
                    room_array[i * 2 + j * row_length] = "@"[0];
                    room_array[i * 2 + 1 + j * row_length] = "."[0];
                },
                "O"[0] => {
                    room_array[i * 2 + j * row_length] = "["[0];
                    room_array[i * 2 + 1 + j * row_length] = "]"[0];
                },
                else => |x| {
                    room_array[i * 2 + j * row_length] = x;
                    room_array[i * 2 + 1 + j * row_length] = x;
                },
            }
        }
        j += 1;
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
            const push_success = push(pos, dir, &room_array, row_length, false);
            if (push_success) {
                pos = pos.next(dir);
            }
        }
    }
    var result: i64 = 0;
    for (0..row_length - 1) |k| {
        for (0..length - 1) |l| {
            if (room_array[k + l * row_length] == "["[0]) {
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
