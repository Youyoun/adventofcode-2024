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
const BoolGrid = Grid(bool);

const Position = struct {
    i: usize,
    j: usize,

    fn next(self: Position, dir: Direction, row_length: usize) ?Position {
        return switch (dir) {
            Direction.East => if (self.i < row_length - 1) Position{ .i = self.i + 1, .j = self.j } else null,
            Direction.West => if (self.i > 0) Position{ .i = self.i - 1, .j = self.j } else null,
            Direction.South => if (self.j < row_length - 1) Position{ .i = self.i, .j = self.j + 1 } else null,
            Direction.North => if (self.j > 0) Position{ .i = self.i, .j = self.j - 1 } else null,
        };
    }
};

const Result = struct { x: usize, y: usize };

fn run(input: [:0]const u8) Result {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    defer arena.deinit(); // clear memory
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    const row_length = 71;
    var room_array = RoomGrid{ .array = allocator.alloc(u8, row_length * row_length) catch unreachable, .row_length = row_length };
    @memset(room_array.array, "."[0]);

    var dist_array = DistGrid{ .array = allocator.alloc(usize, row_length * row_length) catch unreachable, .row_length = row_length };
    var checked_array = BoolGrid{ .array = allocator.alloc(bool, row_length * row_length) catch unreachable, .row_length = row_length };

    var lower: usize = 0;
    var upper: usize = 0;
    while (it.next()) |_| {
        upper += 1;
    }
    it.reset();

    outer: while (upper - lower > 1) {
        @memset(room_array.array, "."[0]);
        const lim = (upper + lower) / 2;
        var count: usize = 0;
        while (it.next()) |row| {
            var sub_it = std.mem.splitScalar(u8, row, ","[0]);
            const i = std.fmt.parseInt(usize, sub_it.next().?, 10) catch unreachable;
            const j = std.fmt.parseInt(usize, sub_it.next().?, 10) catch unreachable;
            room_array.array[i + row_length * j] = "#"[0];
            count += 1;
            if (count >= lim) {
                break;
            }
        }
        it.reset();
        room_array.array[row_length * row_length - 1] = "E"[0];

        const initial_pos = Position{ .i = 0, .j = 0 };
        var pos_list = std.ArrayList(Position).init(allocator);
        pos_list.append(initial_pos) catch unreachable;
        @memset(dist_array.array, 1000000);
        @memset(checked_array.array, false);
        dist_array.set(initial_pos, 0);
        while (pos_list.items.len != 0) {
            var min_i: usize = 0;
            var current_min: usize = 10000000;
            for (0..pos_list.items.len, pos_list.items) |k, pos| {
                const dist = dist_array.get(pos);
                if (dist < current_min) {
                    current_min = dist;
                    min_i = k;
                }
            }
            var min_pos = pos_list.swapRemove(min_i);
            if (room_array.get(min_pos) == "E"[0]) {
                lower = lim;
                continue :outer;
            }
            if (checked_array.get(min_pos)) {
                continue;
            }
            checked_array.set(min_pos, true);

            const dir_array = [_]Direction{ Direction.East, Direction.West, Direction.North, Direction.South };
            for (dir_array) |dir| {
                const next_pos = min_pos.next(dir, row_length) orelse continue;
                if (room_array.get(next_pos) != "#"[0] and !checked_array.get(next_pos)) {
                    const new_dist = dist_array.get(min_pos) + 1;
                    if (dist_array.get(next_pos) > new_dist) {
                        dist_array.set(next_pos, new_dist);
                    }
                    pos_list.append(next_pos) catch unreachable;
                }
            }
        }
        upper = lim;
    }

    var count: usize = 0;
    while (count < lower) {
        _ = it.next();
        count += 1;
    }
    var sub_it = std.mem.splitScalar(u8, it.next().?, ","[0]);
    const i = std.fmt.parseInt(usize, sub_it.next().?, 10) catch unreachable;
    const j = std.fmt.parseInt(usize, sub_it.next().?, 10) catch unreachable;
    return .{ .x = i, .y = j };
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
    try stdout.print("_duration:{d}\n{},{}\n", .{ elapsed_milli, answer.x, answer.y }); // emit actual lines parsed by AOC
}
