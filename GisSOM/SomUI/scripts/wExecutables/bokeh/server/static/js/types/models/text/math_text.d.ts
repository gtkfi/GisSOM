import * as p from "../../core/properties";
import * as visuals from "../../core/visuals";
import { Context2d } from "../../core/util/canvas";
import { Size } from "../../core/types";
import { GraphicsBox, TextHeightMetric, Position } from "../../core/graphics";
import { Rect } from "../../core/util/affine";
import { BBox } from "../../core/util/bbox";
import { BaseText, BaseTextView } from "./base_text";
import { MathJaxProvider } from "./providers";
/**
 * Helper class for rendering MathText into Canvas
 */
export declare abstract class MathTextView extends BaseTextView implements GraphicsBox {
    model: MathText;
    graphics(): GraphicsBox;
    angle?: number;
    _position: Position;
    align: "left" | "center" | "right" | "justify";
    infer_text_height(): TextHeightMetric;
    _x_anchor: "left" | "center" | "right";
    _y_anchor: "top" | "center" | "baseline" | "bottom";
    _base_font_size: number;
    set base_font_size(v: number | null | undefined);
    get base_font_size(): number;
    font_size_scale: number;
    private font;
    private color;
    private svg_image;
    private svg_element;
    get has_image_loaded(): boolean;
    _rect(): Rect;
    set position(p: Position);
    get position(): Position;
    get text(): string;
    get provider(): MathJaxProvider;
    lazy_initialize(): Promise<void>;
    connect_signals(): void;
    set visuals(v: visuals.Text["Values"]);
    /**
     * Calculates position of element after considering
     * anchor and dimensions
     */
    protected _computed_position(): {
        x: number;
        y: number;
    };
    /**
     * Uses the width, height and given angle to calculate the size
    */
    size(): Size;
    private get_text_dimensions;
    private get_image_dimensions;
    _size(): Size;
    bbox(): BBox;
    rect(): Rect;
    paint_rect(ctx: Context2d): void;
    paint_bbox(ctx: Context2d): void;
    protected abstract _process_text(text: string): HTMLElement | undefined;
    private load_image;
    /**
     * Takes a Canvas' Context2d and if the image has already
     * been loaded draws the image in it otherwise draws the model's text.
    */
    paint(ctx: Context2d): void;
}
export declare namespace MathText {
    type Attrs = p.AttrsOf<Props>;
    type Props = BaseText.Props & {
        text: p.Property<string>;
    };
}
export interface MathText extends MathText.Attrs {
}
export declare class MathText extends BaseText {
    properties: MathText.Props;
    __view_type__: MathTextView;
    constructor(attrs?: Partial<MathText.Attrs>);
}
export declare class AsciiView extends MathTextView {
    model: Ascii;
    protected _process_text(_text: string): HTMLElement | undefined;
}
export declare namespace Ascii {
    type Attrs = p.AttrsOf<Props>;
    type Props = MathText.Props;
}
export interface Ascii extends Ascii.Attrs {
}
export declare class Ascii extends MathText {
    properties: Ascii.Props;
    __view_type__: AsciiView;
    constructor(attrs?: Partial<Ascii.Attrs>);
}
export declare class MathMLView extends MathTextView {
    model: MathML;
    protected _process_text(text: string): HTMLElement | undefined;
}
export declare namespace MathML {
    type Attrs = p.AttrsOf<Props>;
    type Props = MathText.Props;
}
export interface MathML extends MathML.Attrs {
}
export declare class MathML extends MathText {
    properties: MathML.Props;
    __view_type__: MathMLView;
    constructor(attrs?: Partial<MathML.Attrs>);
}
export declare class TeXView extends MathTextView {
    model: TeX;
    protected _process_text(text: string): HTMLElement | undefined;
}
export declare namespace TeX {
    type Attrs = p.AttrsOf<Props>;
    type Props = MathText.Props & {
        macros: p.Property<{
            [key: string]: string | [string, number];
        }>;
        inline: p.Property<boolean>;
    };
}
export interface TeX extends TeX.Attrs {
}
export declare class TeX extends MathText {
    properties: TeX.Props;
    __view_type__: TeXView;
    constructor(attrs?: Partial<TeX.Attrs>);
}
//# sourceMappingURL=math_text.d.ts.map