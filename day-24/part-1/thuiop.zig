const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const Operation = enum {
    And,
    Or,
    Xor,
};

const RegisterExpr = struct {
    input1: [3]u8,
    input2: [3]u8,
    operation: Operation,
};

const RegisterValTag = enum {
    regexpr,
    bool,
};

const RegisterVal = union(RegisterValTag) {
    regexpr: RegisterExpr,
    bool: bool,
};

fn get_result(register_name: [3]u8, registers: std.AutoHashMap([3]u8, RegisterVal), results: *std.AutoHashMap([3]u8, bool)) bool {
    if (results.get(register_name)) |val| {
        return val;
    }
    switch (registers.get(register_name).?) {
        .bool => |x| {
            return x;
        },
        .regexpr => |expr| {
            const val_1 = get_result(expr.input1, registers, results);
            const val_2 = get_result(expr.input2, registers, results);
            const result = switch (expr.operation) {
                Operation.And => val_1 and val_2,
                Operation.Or => val_1 or val_2,
                Operation.Xor => val_1 != val_2,
            };
            results.put(register_name, result) catch unreachable;
            return result;
        },
    }
}

fn run(input: [:0]const u8) i64 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var registers = std.AutoHashMap([3]u8, RegisterVal).init(allocator);

    while (it.next()) |row| {
        if (row.len == 0) {
            break;
        }
        const val = allocator.create(RegisterVal) catch unreachable;
        val.* = RegisterVal{ .bool = row[5] == 49 };
        registers.put(row[0..3].*, val.*) catch unreachable;
    }

    while (it.next()) |row| {
        var sub_it = std.mem.splitScalar(u8, row, " "[0]);
        const val_1 = sub_it.next().?[0..3];
        const operation = switch (sub_it.next().?[0]) {
            "AND"[0] => Operation.And,
            "XOR"[0] => Operation.Xor,
            "OR"[0] => Operation.Or,
            else => unreachable,
        };
        const val_2 = sub_it.next().?[0..3];
        _ = sub_it.next();
        const val = allocator.create(RegisterVal) catch unreachable;
        val.* = RegisterVal{ .regexpr = RegisterExpr{ .input1 = val_1.*, .input2 = val_2.*, .operation = operation } };
        registers.put(sub_it.next().?[0..3].*, val.*) catch unreachable;
    }

    var result: i64 = 0;
    var i: usize = 0;
    var current_register: [3]u8 = "z00".*;
    var current_pow: usize = 1;
    var results = std.AutoHashMap([3]u8, bool).init(allocator);
    while (registers.get(current_register)) |_| {
        result += @intCast(@intFromBool(get_result(current_register, registers, &results)) * current_pow);
        current_pow *= 2;
        i += 1;
        _ = std.fmt.bufPrint(&current_register, "z{d:0>2}", .{i}) catch unreachable;
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
