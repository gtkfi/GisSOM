import { CanvasLayer } from "../util/canvas";
import { Color } from "../types";
import { HatchPattern } from "../property_mixins";
export declare type PatternSource = CanvasImageSource;
export declare const hatch_aliases: {
    [key: string]: HatchPattern;
};
export declare function get_pattern(layer: CanvasLayer, pattern: HatchPattern, color: Color, alpha: number, scale: number, weight: number): PatternSource;
//# sourceMappingURL=patterns.d.ts.map