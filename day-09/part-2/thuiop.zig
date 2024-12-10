const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Block = struct {
    index: usize,
    size: usize,
};

const Iterator = struct {
    array: *[]?u32,
    index: usize,

    fn next(self: *Iterator) ?Block {
        if (self.index >= self.array.len - 1) {
            return null;
        }
        while (self.array.*[self.index] != null) : (self.index += 1) {
            if (self.index >= self.array.len - 1) {
                return null;
            }
        }
        var size: usize = 0;
        while (self.array.*[self.index + size] == null) {
            size += 1;
            if (self.index + size >= self.array.len - 1) {
                break;
            }
        }
        const result = Block{ .index = self.index, .size = size };
        self.index += size;
        return result;
    }

    fn reset(self: *Iterator) void {
        self.index = 0;
    }
};

const ReverseIterator = struct {
    array: *[]?u32,
    index: usize,

    fn next(self: *ReverseIterator) ?Block {
        if (self.index <= 0) {
            return null;
        }
        while (self.array.*[self.index] == null) : (self.index -= 1) {
            if (self.index <= 0) {
                return null;
            }
        }
        var size: usize = 0;
        const value = self.array.*[self.index];
        while (self.array.*[self.index - size] == value) {
            size += 1;
            if (self.index - size <= 0) {
                break;
            }
        }
        const result = Block{ .index = self.index, .size = size };
        self.index -= size;
        return result;
    }
};

fn run(input: [:0]const u8) i64 {
    const allocator = std.heap.page_allocator;
    var layout_list = std.ArrayList(?u32).init(allocator);
    var current_num: u32 = 0;
    for (0..input.len) |i| {
        const size = std.fmt.parseInt(u4, input[i .. i + 1], 10) catch unreachable;
        var id: ?u32 = null;
        if (i % 2 == 0) {
            id = current_num;
            current_num += 1;
        }
        for (0..size) |_| {
            layout_list.append(id) catch unreachable;
        }
    }
    var layout = layout_list.items;
    var it = Iterator{ .array = &layout, .index = 0 };
    var reverse_it = ReverseIterator{ .array = &layout, .index = layout.len - 1 };
    while (reverse_it.next()) |file_block| {
        while (it.next()) |free_block| {
            if (free_block.index >= file_block.index) {
                break;
            }
            if (free_block.size >= file_block.size) {
                for (0..file_block.size) |i| {
                    layout[free_block.index + i] = layout[file_block.index - i];
                    layout[file_block.index - i] = null;
                }
            }
        }
        it.reset();
    }

    var checksum: i64 = 0;
    for (0..layout.len) |i| {
        if (layout[i] != null) {
            const pos: i64 = @intCast(i);
            const val: i64 = @intCast(layout[i].?);
            checksum += pos * val;
        }
    }
    return checksum;
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
