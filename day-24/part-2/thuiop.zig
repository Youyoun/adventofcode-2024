const std = @import("std");

var a: std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn compareStrings(_: void, lhs: [3]u8, rhs: [3]u8) bool {
    return std.mem.order(u8, &lhs, &rhs).compare(std.math.CompareOperator.lt);
}

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

fn check_registers(register_name: [3]u8, registers: std.AutoHashMap([3]u8, RegisterVal), registers_to_swap: *std.AutoHashMap([3]u8, bool), expected_ops: []Operation) void {
    switch (registers.get(register_name).?) {
        .bool => return,
        .regexpr => |expr| {
            const new_expected_ops: []Operation = switch (expr.operation) {
                .And => @constCast(&[2]Operation{ .Or, .Xor }),
                .Or => @constCast(&[1]Operation{.And}),
                .Xor => @constCast(&[3]Operation{ .And, .Or, .Xor }),
            };
            var ok: bool = false;
            for (expected_ops) |op| {
                if (expr.operation == op) {
                    ok = true;
                }
            }
            if (!ok) {
                registers_to_swap.put(register_name, true) catch unreachable;
            }
            check_registers(expr.input1, registers, registers_to_swap, new_expected_ops);
            check_registers(expr.input2, registers, registers_to_swap, new_expected_ops);
            return;
        },
    }
}

fn run(input: [:0]const u8) [][3]u8 {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();

    var it = std.mem.splitScalar(u8, input, "\n"[0]);
    var registers = std.AutoHashMap([3]u8, RegisterVal).init(allocator);
    var integer_size: usize = 0;

    while (it.next()) |row| {
        if (row.len == 0) {
            break;
        }
        const val = allocator.create(RegisterVal) catch unreachable;
        val.* = RegisterVal{ .bool = row[5] == 49 };
        registers.put(row[0..3].*, val.*) catch unreachable;
        integer_size += 1;
    }
    integer_size /= 2;

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

    var i: usize = 0;
    var current_register: [3]u8 = "z00".*;
    var current_pow: usize = 1;
    var registers_to_swap = std.AutoHashMap([3]u8, bool).init(allocator);
    while (i < integer_size + 1) {
        const starting_op: []Operation = if (i == integer_size) @constCast(&[1]Operation{.Or}) else @constCast(&[1]Operation{.Xor});
        check_registers(current_register, registers, &registers_to_swap, starting_op);
        current_pow *= 2;
        i += 1;
        _ = std.fmt.bufPrint(&current_register, "z{d:0>2}", .{i}) catch unreachable;
    }
    var registers_to_swap_list = std.ArrayList([3]u8).init(allocator);
    var key_it = registers_to_swap.keyIterator();
    while (key_it.next()) |register| {
        registers_to_swap_list.append(register.*) catch unreachable;
    }
    std.mem.sort([3]u8, registers_to_swap_list.items, {}, compareStrings);
    return registers_to_swap_list.items;
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
    try stdout.print("_duration:{d}\n", .{elapsed_milli}); // emit actual lines parsed by AOC
    for (answer[0 .. answer.len - 1]) |value| {
        try stdout.print("{s},", .{value});
    }
    try stdout.print("{s}\n", .{answer[answer.len - 1]});
}
