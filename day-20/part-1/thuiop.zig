const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Direction = enum(u2) {
    North,
    East,
    South,
    West,
};

fn clockwise(dir: Direction) Direction {
    return switch (dir) {
        Direction.East => Direction.South,
        Direction.South => Direction.West,
        Direction.West => Direction.North,
        Direction.North => Direction.East,
    };
}

fn counterclockwise(dir: Direction) Direction {
    return switch (dir) {
        Direction.East => Direction.North,
        Direction.South => Direction.East,
        Direction.West => Direction.South,
        Direction.North => Direction.West,
    };
}

fn Grid(comptime T: type) type {
    return struct {
        array: []T,
        row_length: usize,

        const Self = @This();
        fn get(self: Self, pos: Position) T {
            return self.array[pos.i + pos.j * self.row_length];
        }

        fn set(self: Self, pos: Position, val: T) void {
            self.array[pos.i + pos.j * self.row_length] = val;
        }

        fn grid_print(self: Self) void {
            for (0..self.row_length) |i| {
                std.debug.print("{s}\n", .{self.array[i * self.row_length .. (i + 1) * self.row_length]});
            }
        }
    };
}
const RoomGrid = Grid(u8);
const DistGrid = Grid(usize);

const Position = struct {
    i: usize,
    j: usize,
    dir: Direction,

    fn next(self: Position, dir: Direction, row_length: usize) ?Position {
        return switch (dir) {
            Direction.East => if (self.i < row_length - 1) Position{ .i = self.i + 1, .j = self.j, .dir = Direction.East } else null,
            Direction.West => if (self.i > 0) Position{ .i = self.i - 1, .j = self.j, .dir = Direction.West } else null,
            Direction.South => if (self.j < row_length - 1) Position{ .i = self.i, .j = self.j + 1, .dir = Direction.South } else null,
            Direction.North => if (self.j > 0) Position{ .i = self.i, .j = self.j - 1, .dir = Direction.North } else null,
        };
    }
};

fn get_length(pos: Position, room: RoomGrid, results: *Grid(?i64)) ?i64 {
    if (room.get(pos) == "E"[0]) {
        return 0;
    }
    if (results.get(pos)) |res| {
        return res;
    }
    const possible_next: [3]?Position = .{ pos.next(pos.dir, room.row_length), pos.next(clockwise(pos.dir), room.row_length), pos.next(counterclockwise(pos.dir), room.row_length) };

    for (possible_next) |next_pos| {
        if (next_pos) |next_pos_unwrap| {
            if (room.get(next_pos_unwrap) != "#"[0]) {
                const length = get_length(next_pos_unwrap, room, results) orelse continue;
                results.set(pos, 1 + length);
                return 1 + length;
            }
        }
    }
    return null;
}

fn find_cheats(pos: Position, room: RoomGrid, results: *Grid(?i64)) i64 {
    if (room.get(pos) == "E"[0]) {
        return 0;
    }
    const ref_time = results.get(pos).?;
    const possible_next: [3]Direction = .{ clockwise(pos.dir), counterclockwise(pos.dir), pos.dir };
    var result: i64 = 0;
    var position_to_try: ?Position = null;
    for (possible_next) |next_dir| {
        const next_pos = pos.next(next_dir, room.row_length) orelse continue;
        if (room.get(next_pos) == "#"[0]) {
            const next_next_pos = next_pos.next(next_dir, room.row_length) orelse continue;
            if (results.get(next_next_pos)) |length| {
                if (ref_time - (length + 2) >= 100) {
                    result += 1;
                }
            }
        } else {
            position_to_try = next_pos;
        }
    }
    if (position_to_try) |next_pos| {
        result += find_cheats(next_pos, room, results);
    }
    return result;
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const row_length = it.peek().?.len;
    var room_array = RoomGrid{ .array = allocator.alloc(u8, row_length * row_length) catch unreachable, .row_length = row_length };

    var i: usize = 0;
    while (it.next()) |row| {
        if (row.len == 0) {
            break;
        }
        @memcpy(room_array.array[i * row_length .. (i + 1) * row_length], row);
        i += 1;
    }
    const index = std.mem.indexOf(u8, room_array.array, "S").?;
    var initial_pos = Position{ .i = index % row_length, .j = index / row_length, .dir = Direction.East };
    for ([4]Direction{ Direction.East, Direction.West, Direction.North, Direction.South }) |dir| {
        if (room_array.get(initial_pos.next(dir, row_length).?) == "."[0]) {
            initial_pos.dir = dir;
            break;
        }
    }
    var results = Grid(?i64){ .array = allocator.alloc(?i64, row_length * row_length) catch unreachable, .row_length = row_length };
    @memset(results.array, null);
    _ = get_length(initial_pos, room_array, &results).?;

    return find_cheats(initial_pos, room_array, &results) + 2;
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
