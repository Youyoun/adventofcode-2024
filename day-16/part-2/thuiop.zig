const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

var ar = std.heap.ArenaAllocator.init(std.heap.page_allocator);
const allocator = ar.allocator();

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
        fn get(self: Self, pos: *Position) T {
            return self.array[pos.i + pos.j * self.row_length];
        }

        fn set(self: Self, pos: *Position, val: T) void {
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
        fn get(self: Self, pos: *Position) T {
            return self.array[pos.i + pos.j * self.row_length + @intFromEnum(pos.dir) * self.row_length * self.row_length];
        }

        fn set(self: Self, pos: *Position, val: T) void {
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
    prev_pos: ?*Position = null,

    fn next(self: *Position, dir: Direction) *Position {
        const new_pos = allocator.create(Position) catch unreachable;
        new_pos.* = switch (dir) {
            Direction.East => Position{ .i = self.i + 1, .j = self.j, .dir = dir, .prev_pos = self },
            Direction.West => Position{ .i = self.i - 1, .j = self.j, .dir = dir, .prev_pos = self },
            Direction.South => Position{ .i = self.i, .j = self.j + 1, .dir = dir, .prev_pos = self },
            Direction.North => Position{ .i = self.i, .j = self.j - 1, .dir = dir, .prev_pos = self },
        };
        return new_pos;
    }

    fn unwind(self: *Position, bool_array: *Grid(bool)) i64 {
        const unchecked = !bool_array.*.get(self);
        if (unchecked) {
            bool_array.*.set(self, true);
        }
        if (self.prev_pos == null) {
            return @intFromBool(unchecked);
        } else {
            if (self.prev_pos.?.i == self.i and self.prev_pos.?.j == self.j) {
                unreachable;
            }
            return @intFromBool(unchecked) + self.prev_pos.?.unwind(bool_array);
        }
    }
};

fn compare_distance(context: DistGrid, pos_1: *Position, pos_2: *Position) std.math.Order {
    const dist_1 = context.get(pos_1);
    const dist_2 = context.get(pos_2);
    return std.math.order(dist_1, dist_2);
}

fn run(input: [:0]const u8) i64 {
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

    var dist_array = DistGrid{ .array = allocator.alloc(usize, row_length * row_length * 4) catch unreachable, .row_length = row_length };
    @memset(dist_array.array, 1000000);
    dist_array.set(&initial_pos, 0);

    var pos_list = std.PriorityQueue(*Position, DistGrid, compare_distance).init(allocator, dist_array);
    pos_list.add(&initial_pos) catch unreachable;

    var shortest: usize = 10000000;
    var good_pos_array = Grid(bool){ .array = allocator.alloc(bool, row_length * row_length) catch unreachable, .row_length = row_length };
    @memset(good_pos_array.array, false);
    var case_count: i64 = 0;

    while (pos_list.removeOrNull()) |min_pos| {
        const current_dist = dist_array.get(min_pos);
        if (current_dist > shortest) {
            continue;
        }
        if (room_array.get(min_pos) == "E"[0]) {
            shortest = current_dist;
            case_count += min_pos.unwind(&good_pos_array);
            continue;
        }

        const next_positions = [3]*Position{ min_pos.next(min_pos.dir), min_pos.next(clockwise(min_pos.dir)), min_pos.next(counterclockwise(min_pos.dir)) };
        for (next_positions, [3]usize{ 1, 1001, 1001 }) |next_pos, score| {
            if (room_array.get(next_pos) != "#"[0]) {
                const new_dist = current_dist + score;
                if (dist_array.get(next_pos) >= new_dist) {
                    dist_array.set(next_pos, new_dist);
                    pos_list.add(next_pos) catch unreachable;
                }
            }
        }
    }
    return case_count;
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
