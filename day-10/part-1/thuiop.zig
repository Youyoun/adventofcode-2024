const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Position = struct {
    i: usize,
    j: usize,
};

const Map = struct {
    array: []u4,
    row_length: usize,
    marks: *[]bool,

    fn get(self: Map, pos: Position) ?u4 {
        if (0 <= pos.j and pos.j < self.row_length and 0 <= pos.i and pos.i < self.row_length) {
            return self.array[pos.j + self.row_length * pos.i];
        } else {
            return null;
        }
    }

    fn is_marked(self: Map, pos: Position) bool {
        if (0 <= pos.j and pos.j < self.row_length and 0 <= pos.i and pos.i < self.row_length) {
            return self.marks.*[pos.j + self.row_length * pos.i];
        } else {
            return false;
        }
    }

    fn mark(self: Map, pos: Position) void {
        if (0 <= pos.j and pos.j < self.row_length and 0 <= pos.i and pos.i < self.row_length) {
            self.marks.*[pos.j + self.row_length * pos.i] = true;
        }
    }
};

fn trailblaze(map: Map, pos: Position) i64 {
    const current_num = map.get(pos).?;
    map.mark(pos);
    if (current_num == 9) {
        return 1;
    }
    var total: i64 = 0;
    const i = pos.i;
    const j = pos.j;
    const new_i = [4]usize{ i + 1, i - 1, i, i };
    const new_j = [4]usize{ j, j, j - 1, j + 1 };
    for (new_i, new_j) |ni, nj| {
        const new_pos: Position = Position{ .i = ni, .j = nj };
        if (map.get(new_pos) == current_num + 1 and !map.is_marked(new_pos)) {
            total += trailblaze(map, new_pos);
        }
    }
    return total;
}

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator;
    const row_length = std.mem.indexOf(u8, input, "\n").?;
    var map_array = allocator.alloc(u4, row_length * row_length) catch unreachable;
    var i: usize = 0;
    for (input) |elem| {
        if (elem == "\n"[0]) {
            continue;
        }
        map_array[i] = std.fmt.parseInt(u4, &[1]u8{elem}, 10) catch 15;
        i += 1;
    }
    var marks = allocator.alloc(bool, row_length * row_length) catch unreachable;
    @memset(marks, false);
    var map = Map{ .array = map_array, .row_length = row_length, .marks = &marks };
    var total: i64 = 0;
    for (0..row_length) |x| {
        for (0..row_length) |y| {
            const pos = Position{ .i = x, .j = y };
            if (map.get(pos) == 0) {
                total += trailblaze(map, pos);
                @memset(map.marks.*, false);
            }
        }
    }

    return total;
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
