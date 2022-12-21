import { Arrayable } from "../types";
export declare type Point = {
    x: number;
    y: number;
};
export declare type Rect = {
    p0: Point;
    p1: Point;
    p2: Point;
    p3: Point;
};
export declare class AffineTransform {
    private a;
    private b;
    private c;
    private d;
    private e;
    private f;
    constructor(a?: number, b?: number, c?: number, d?: number, e?: number, f?: number);
    toString(): string;
    static from_DOMMatrix(matrix: DOMMatrix): AffineTransform;
    to_DOMMatrix(): DOMMatrix;
    clone(): AffineTransform;
    get is_identity(): boolean;
    apply_point(p: Point): Point;
    apply_rect(rect: Rect): Rect;
    apply(x: number, y: number): [number, number];
    iv_apply(xs: Arrayable<number>, ys: Arrayable<number>): void;
    transform(A: number, B: number, C: number, D: number, E: number, F: number): this;
    translate(tx: number, ty: number): this;
    scale(cx: number, cy: number): this;
    skew(sx: number, sy: number): this;
    rotate(angle: number): this;
    rotate_ccw(angle: number): this;
    translate_x(tx: number): this;
    translate_y(ty: number): this;
    flip(): this;
    flip_x(): this;
    flip_y(): this;
}
//# sourceMappingURL=affine.d.ts.map