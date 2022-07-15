import { equals, Equatable, Comparator } from "./eq";
import { Arrayable } from "../types";
export declare class BitSet implements Equatable {
    readonly size: number;
    private readonly _array;
    private readonly _nwords;
    constructor(size: number, init?: Uint32Array | 1 | 0);
    [Symbol.toStringTag]: string;
    clone(): BitSet;
    [equals](that: this, cmp: Comparator): boolean;
    static all_set(size: number): BitSet;
    static all_unset(size: number): BitSet;
    static from_indices(size: number, indices: Iterable<number>): BitSet;
    static from_booleans(size: number, booleans: boolean[]): BitSet;
    private _check_bounds;
    get(k: number): boolean;
    set(k: number, v?: boolean): void;
    unset(k: number): void;
    [Symbol.iterator](): Iterator<number>;
    private _count;
    get count(): number;
    protected _get_count(): number;
    ones(): Iterable<number>;
    zeros(): Iterable<number>;
    private _check_size;
    add(other: BitSet): void;
    intersect(other: BitSet): void;
    subtract(other: BitSet): void;
    union(other: BitSet): BitSet;
    intersection(other: BitSet): BitSet;
    difference(other: BitSet): BitSet;
    select<T>(array: Arrayable<T>): Arrayable<T>;
}
//# sourceMappingURL=bitset.d.ts.map