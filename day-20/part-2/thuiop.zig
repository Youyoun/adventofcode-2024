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
        results.set(pos, 0);
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
    const initial_pos = Position{ .i = index % row_length, .j = index / row_length, .dir = Direction.East };
    var results = Grid(?i64){ .array = allocator.alloc(?i64, row_length * row_length) catch unreachable, .row_length = row_length };
    @memset(results.array, null);
    _ = get_length(initial_pos, room_array, &results).?;

    var n_cheats: i64 = 0;

    var k: i64 = 0;
    const row_length_s: i64 = @intCast(row_length);
    while (k < row_length_s * row_length_s) : (k += 1) {
        const i_1 = @mod(k, row_length_s);
        const j_1 = @divTrunc(k, row_length_s);
        const res1 = results.array[@as(usize, @intCast(i_1 + row_length_s * j_1))] orelse continue;
        var l: i64 = 0;
        while (l < row_length_s * row_length_s) : (l += 1) {
            const i_2 = @mod(l, row_length_s);
            const j_2 = @divTrunc(l, row_length_s);
            const res2 = results.array[@as(usize, @intCast(i_2 + row_length_s * j_2))] orelse continue;
            const dist: i64 = @intCast(@abs(i_2 - i_1) + @abs(j_2 - j_1));
            if (dist <= 20 and res2 - (res1 + dist) >= 100) {
                n_cheats += 1;
            }
        }
    }

    return n_cheats;
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
