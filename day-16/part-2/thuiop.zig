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

const Turn = enum { Left, Right, Straight };

const PrevList = struct {
    items: [3]Position,
    len: usize = 0,

    fn append(self: *PrevList, pos: Position) void {
        self.items[self.len] = pos;
        self.len += 1;
    }
};

const Position = struct {
    i: usize,
    j: usize,
    dir: Direction,
    current_distance: usize = 0,

    fn next(self: Position, comptime turn: Turn) Position {
        const dir = switch (turn) {
            .Left => counterclockwise(self.dir),
            .Right => clockwise(self.dir),
            .Straight => self.dir,
        };
        const cost = switch (turn) {
            .Left => 1001,
            .Right => 1001,
            .Straight => 1,
        };
        return switch (dir) {
            Direction.East => Position{ .i = self.i + 1, .j = self.j, .dir = dir, .current_distance = self.current_distance + cost },
            Direction.West => Position{ .i = self.i - 1, .j = self.j, .dir = dir, .current_distance = self.current_distance + cost },
            Direction.South => Position{ .i = self.i, .j = self.j + 1, .dir = dir, .current_distance = self.current_distance + cost },
            Direction.North => Position{ .i = self.i, .j = self.j - 1, .dir = dir, .current_distance = self.current_distance + cost },
        };
    }

    fn unwind(self: Position, bool_array: *Grid(bool), prev_grid: GridWithDir(*PrevList)) i64 {
        const unchecked = !bool_array.*.get(self);
        if (unchecked) {
            bool_array.set(self, true);
        }
        const prev_list = prev_grid.get(self);
        var value: i64 = @intFromBool(unchecked);
        for (prev_list.items[0..prev_list.len]) |prev_pos| {
            value += prev_pos.unwind(bool_array, prev_grid);
        }
        return value;
    }
};

fn compare_distance(context: void, pos_1: Position, pos_2: Position) std.math.Order {
    _ = context;
    const dist_1 = pos_1.current_distance;
    const dist_2 = pos_2.current_distance;
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
    const initial_pos = Position{ .i = index % row_length, .j = index / row_length, .dir = Direction.East };

    var dist_array = DistGrid{ .array = allocator.alloc(usize, row_length * row_length * 4) catch unreachable, .row_length = row_length };
    @memset(dist_array.array, 1000000);
    dist_array.set(initial_pos, 0);

    var pos_list = std.PriorityQueue(Position, void, compare_distance).init(allocator, {});
    pos_list.add(initial_pos) catch unreachable;

    var prev_grid = GridWithDir(*PrevList){ .array = allocator.alloc(*PrevList, row_length * row_length * 4) catch unreachable, .row_length = row_length };
    var prev_list_array = allocator.alloc(PrevList, row_length * row_length * 4) catch unreachable;
    for (0..row_length * row_length * 4) |j| {
        prev_list_array[j].len = 0;
        prev_grid.array[j] = &prev_list_array[j];
    }

    var shortest: usize = 10000000;
    var end_pos: Position = undefined;

    while (pos_list.removeOrNull()) |min_pos| {
        const current_dist = dist_array.get(min_pos);
        if (current_dist > shortest or min_pos.current_distance > current_dist) {
            continue;
        }
        if (room_array.get(min_pos) == "E"[0]) {
            shortest = current_dist;
            end_pos = min_pos;
            continue;
        }

        inline for ([3]Turn{ .Straight, .Left, .Right }) |turn| {
            const next_pos = min_pos.next(turn);
            if (room_array.get(next_pos) != "#"[0]) {
                const new_dist = next_pos.current_distance;
                const old_dist = dist_array.get(next_pos);
                if (old_dist >= new_dist) {
                    dist_array.set(next_pos, new_dist);
                    var prev_list = prev_grid.get(next_pos);
                    if (old_dist > new_dist) {
                        pos_list.add(next_pos) catch unreachable;
                        prev_list.len = 0;
                    }
                    prev_list.append(min_pos);
                }
            }
        }
    }
    // for (0..row_length) |l| {
    //     for (0..row_length) |k| {
    //         if (good_pos_array.array[k + l * row_length]) {
    //             room_array.array[k + l * row_length] = "O"[0];
    //         }
    //     }
    // }
    // for (0..row_length) |l| {
    //     std.debug.print("{s}\n", .{room_array.array[l * row_length .. (l + 1) * row_length]});
    // }
    var good_pos_array = Grid(bool){ .array = allocator.alloc(bool, row_length * row_length) catch unreachable, .row_length = row_length };
    @memset(good_pos_array.array, false);
    return end_pos.unwind(&good_pos_array, prev_grid);
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
