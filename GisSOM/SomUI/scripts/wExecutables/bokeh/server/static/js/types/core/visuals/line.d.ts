import { VisualProperties, VisualUniforms, ValuesOf } from "./visual";
import { uint32 } from "../types";
import * as p from "../properties";
import * as mixins from "../property_mixins";
import { LineJoin, LineCap, LineDash } from "../enums";
import { Context2d } from "../util/canvas";
export declare function resolve_line_dash(line_dash: LineDash | string | number[]): number[];
export interface Line extends Readonly<mixins.Line> {
}
export declare class Line extends VisualProperties {
    get doit(): boolean;
    apply(ctx: Context2d): boolean;
    Values: ValuesOf<mixins.Line>;
    values(): this["Values"];
    set_value(ctx: Context2d): void;
}
export declare class LineScalar extends VisualUniforms {
    readonly line_color: p.UniformScalar<uint32>;
    readonly line_alpha: p.UniformScalar<number>;
    readonly line_width: p.UniformScalar<number>;
    readonly line_join: p.UniformScalar<LineJoin>;
    readonly line_cap: p.UniformScalar<LineCap>;
    readonly line_dash: p.UniformScalar<LineDash | number[]>;
    readonly line_dash_offset: p.UniformScalar<number>;
    get doit(): boolean;
    apply(ctx: Context2d): boolean;
    Values: ValuesOf<mixins.Line>;
    values(): this["Values"];
    set_value(ctx: Context2d): void;
}
export declare class LineVector extends VisualUniforms {
    readonly line_color: p.Uniform<uint32>;
    readonly line_alpha: p.Uniform<number>;
    readonly line_width: p.Uniform<number>;
    readonly line_join: p.Uniform<LineJoin>;
    readonly line_cap: p.Uniform<LineCap>;
    readonly line_dash: p.Uniform<LineDash | number[]>;
    readonly line_dash_offset: p.Uniform<number>;
    get doit(): boolean;
    apply(ctx: Context2d, i: number): boolean;
    Values: ValuesOf<mixins.Line>;
    values(i: number): this["Values"];
    set_vectorize(ctx: Context2d, i: number): void;
}
//# sourceMappingURL=line.d.ts.map