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
                std.debug.print("{any}\n", .{self.array[i * self.row_length .. (i + 1) * self.row_length]});
            }
        }
    };
}
const RoomGrid = Grid(u8);

fn GridWithDir(comptime T: type) type {
    return struct {
        array: []T,
        row_length: usize,

        const Self = @This();
        fn get(self: Self, pos: Position) T {
            return self.array[pos.i + pos.j * self.row_length + @intFromEnum(pos.dir) * self.row_length * self.row_length];
        }

        fn set(self: Self, pos: Position, val: T) void {
            self.array[pos.i + pos.j * self.row_length + @intFromEnum(pos.dir) * self.row_length * self.row_length] = val;
        }
    };
}
const DistGrid = GridWithDir(usize);
const BoolGrid = GridWithDir(bool);

const Position = struct {
    i: usize,
    j: usize,
    dir: Direction,

    fn next(self: Position, dir: Direction) Position {
        return switch (dir) {
            Direction.East => Position{ .i = self.i + 1, .j = self.j, .dir = dir },
            Direction.West => Position{ .i = self.i - 1, .j = self.j, .dir = dir },
            Direction.South => Position{ .i = self.i, .j = self.j + 1, .dir = dir },
            Direction.North => Position{ .i = self.i, .j = self.j - 1, .dir = dir },
        };
    }
};

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings
    defer arena.deinit(); // clear memory
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
    var pos_list = std.ArrayList(Position).init(allocator);
    pos_list.append(initial_pos) catch unreachable;
    var dist_array = DistGrid{ .array = allocator.alloc(usize, row_length * row_length * 4) catch unreachable, .row_length = row_length };
    @memset(dist_array.array, 1000000);
    var checked_array = BoolGrid{ .array = allocator.alloc(bool, row_length * row_length * 4) catch unreachable, .row_length = row_length };
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
            return @intCast(current_min);
        }
        if (checked_array.get(min_pos)) {
            continue;
        }
        checked_array.set(min_pos, true);

        var next_pos = min_pos.next(min_pos.dir);
        if (room_array.get(next_pos) != "#"[0] and !checked_array.get(next_pos)) {
            const new_dist = dist_array.get(min_pos) + 1;
            if (dist_array.get(next_pos) > new_dist) {
                dist_array.set(next_pos, new_dist);
            }
            pos_list.append(next_pos) catch unreachable;
        }

        next_pos = min_pos.next(clockwise(min_pos.dir));
        if (room_array.get(next_pos) != "#"[0] and !checked_array.get(next_pos)) {
            const new_dist = dist_array.get(min_pos) + 1001;
            if (dist_array.get(next_pos) > new_dist) {
                dist_array.set(next_pos, new_dist);
            }
            pos_list.append(next_pos) catch unreachable;
        }

        next_pos = min_pos.next(counterclockwise(min_pos.dir));
        if (room_array.get(next_pos) != "#"[0] and !checked_array.get(next_pos)) {
            const new_dist = dist_array.get(min_pos) + 1001;
            if (dist_array.get(next_pos) > new_dist) {
                dist_array.set(next_pos, new_dist);
            }
            pos_list.append(next_pos) catch unreachable;
        }
    }
    unreachable;
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
