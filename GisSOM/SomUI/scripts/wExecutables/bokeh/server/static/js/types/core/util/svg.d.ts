/**
 * Based on https://github.com/gliffy/canvas2svg
 */
import { AffineTransform } from "./affine";
import { Random } from "./random";
declare type KV<T> = {
    [key: string]: T;
};
declare type FontData = {
    style: string;
    size: string;
    family: string;
    weight: string;
    decoration: string;
};
declare type Style = {
    svgAttr?: string;
    canvas: unknown;
    svg?: unknown;
    apply?: string;
};
declare type StyleAttr = "strokeStyle" | "fillStyle" | "lineCap" | "lineJoin" | "miterLimit" | "lineWidth" | "globalAlpha" | "font" | "shadowColor" | "shadowOffsetX" | "shadowOffsetY" | "shadowBlur" | "textAlign" | "textBaseline" | "lineDash" | "lineDashOffset";
declare type StyleState = {
    [key in StyleAttr]: Style;
};
declare class CanvasGradient implements globalThis.CanvasGradient {
    __root: SVGElement;
    __ctx: SVGRenderingContext2D;
    constructor(gradientNode: SVGElement, ctx: SVGRenderingContext2D);
    /**
     * Adds a color stop to the gradient root
     */
    addColorStop(offset: number, color: string): void;
}
declare class CanvasPattern implements globalThis.CanvasPattern {
    __root: SVGPatternElement;
    __ctx: SVGRenderingContext2D;
    constructor(pattern: SVGPatternElement, ctx: SVGRenderingContext2D);
    setTransform(_transform?: DOMMatrix2DInit): void;
}
declare type Options = {
    width?: number;
    height?: number;
    document?: Document;
    ctx?: CanvasRenderingContext2D;
};
declare type Path = string;
declare type SVGCanvasState = {
    transform: AffineTransform;
    clip_path: Path | null;
    attributes: StyleState;
};
/**
 * The mock canvas context
 * @param o - options include:
 * ctx - existing Context2D to wrap around
 * width - width of your canvas (defaults to 500)
 * height - height of your canvas (defaults to 500)
 * document - the document object (defaults to the current document)
 */
declare type BaseCanvasRenderingContext2D = CanvasCompositing & CanvasDrawImage & CanvasDrawPath & CanvasFillStrokeStyles & CanvasFilters & CanvasImageData & CanvasImageSmoothing & CanvasPath & CanvasPathDrawingStyles & CanvasRect & CanvasShadowStyles & CanvasState & CanvasText & CanvasTextDrawingStyles & CanvasTransform & CanvasUserInterface;
export declare class SVGRenderingContext2D implements BaseCanvasRenderingContext2D {
    __canvas: HTMLCanvasElement;
    __ctx: CanvasRenderingContext2D;
    __root: SVGSVGElement;
    __ids: Set<string>;
    __defs: SVGElement;
    __stack: SVGCanvasState[];
    __document: Document;
    __currentElement: SVGElement;
    __currentDefaultPath: string;
    __currentPosition: {
        x: number;
        y: number;
    } | null;
    static __random: Random;
    get canvas(): SVGRenderingContext2D;
    strokeStyle: string | CanvasGradient | CanvasPattern;
    fillStyle: string | CanvasGradient | CanvasPattern;
    lineCap: CanvasLineCap;
    lineJoin: CanvasLineJoin;
    miterLimit: number;
    lineWidth: number;
    globalAlpha: number;
    globalCompositeOperation: string;
    font: string;
    direction: CanvasDirection;
    shadowColor: string;
    shadowOffsetX: number;
    shadowOffsetY: number;
    shadowBlur: number;
    textAlign: CanvasTextAlign;
    textBaseline: CanvasTextBaseline;
    lineDash: string | number[] | null;
    lineDashOffset: number;
    filter: string;
    imageSmoothingEnabled: boolean;
    imageSmoothingQuality: ImageSmoothingQuality;
    private _width;
    private _height;
    get width(): number;
    set width(width: number);
    get height(): number;
    set height(height: number);
    private _transform;
    constructor(options?: Options);
    protected _random_string(): string;
    /**
     * Creates the specified svg element
     */
    __createElement(elementName: string, properties?: KV<string | number>, resetFill?: boolean): SVGElement;
    /**
     * Applies default canvas styles to the context
     */
    __setDefaultStyles(): void;
    /**
     * Applies styles on restore
     */
    __applyStyleState(styleState: StyleState): void;
    /**
     * Gets the current style state
     */
    __getStyleState(): StyleState;
    /**
     * Apples the current styles to the current SVG element. On "ctx.fill" or "ctx.stroke"
     */
    __applyStyleToCurrentElement(type: string): void;
    /**
      * Returns the serialized value of the svg so far
      * @param fixNamedEntities - Standalone SVG doesn't support named entities, which document.createTextNode encodes.
      *                           If true, we attempt to find all named entities and encode it as a numeric entity.
      * @return serialized svg
      */
    get_serialized_svg(fixNamedEntities?: boolean): string;
    get_svg(): SVGSVGElement;
    /**
      * Will generate a group tag.
      */
    save(): void;
    /**
      * Sets current element to parent, or just root if already root
      */
    restore(): void;
    private _apply_transform;
    /**
      *  scales the current element
      */
    scale(x: number, y?: number): void;
    /**
      * rotates the current element
      */
    rotate(angle: number): void;
    /**
      * translates the current element
      */
    translate(x: number, y: number): void;
    /**
      * applies a transform to the current element
      */
    transform(a: number, b: number, c: number, d: number, e: number, f: number): void;
    /**
      * Create a new Path Element
      */
    beginPath(): void;
    protected __init_element(): void;
    /**
      * Helper function to apply currentDefaultPath to current path element
      */
    __applyCurrentDefaultPath(): void;
    /**
      * Helper function to add path command
      */
    __addPathCommand(x: number, y: number, path: string): void;
    get _hasCurrentDefaultPath(): boolean;
    /**
      * Adds the move command to the current path element,
      * if the currentPathElement is not empty create a new path element
      */
    moveTo(x: number, y: number): void;
    /**
      * Closes the current path
      */
    closePath(): void;
    /**
      * Adds a line to command
      */
    lineTo(x: number, y: number): void;
    /**
      * Add a bezier command
      */
    bezierCurveTo(cp1x: number, cp1y: number, cp2x: number, cp2y: number, x: number, y: number): void;
    /**
      * Adds a quadratic curve to command
      */
    quadraticCurveTo(cpx: number, cpy: number, x: number, y: number): void;
    /**
      * Adds the arcTo to the current path
      *
      * @see http://www.w3.org/TR/2015/WD-2dcontext-20150514/#dom-context-2d-arcto
      */
    arcTo(x1: number, y1: number, x2: number, y2: number, radius: number): void;
    /**
      * Sets the stroke property on the current element
      */
    stroke(): void;
    /**
      * Sets fill properties on the current element
      */
    fill(fill_rule?: CanvasFillRule): void;
    fill(path: Path2D, fill_rule?: CanvasFillRule): void;
    /**
      *  Adds a rectangle to the path.
      */
    rect(x: number, y: number, width: number, height: number): void;
    /**
      * adds a rectangle element
      */
    fillRect(x: number, y: number, width: number, height: number): void;
    /**
      * Draws a rectangle with no fill
      * @param x
      * @param y
      * @param width
      * @param height
      */
    strokeRect(x: number, y: number, width: number, height: number): void;
    /**
      * Clear entire canvas:
      * 1. save current transforms
      * 2. remove all the childNodes of the root g element
      */
    __clearCanvas(): void;
    /**
      * "Clears" a canvas by just drawing a white rectangle in the current group.
      */
    clearRect(x: number, y: number, width: number, height: number): void;
    /**
      * Adds a linear gradient to a defs tag.
      * Returns a canvas gradient object that has a reference to it's parent def
      */
    createLinearGradient(x1: number, y1: number, x2: number, y2: number): CanvasGradient;
    /**
      * Adds a radial gradient to a defs tag.
      * Returns a canvas gradient object that has a reference to it's parent def
      */
    createRadialGradient(x0: number, y0: number, r0: number, x1: number, y1: number, r1: number): CanvasGradient;
    /**
      * Parses the font string and returns svg mapping
      */
    __parseFont(): FontData;
    /**
      * Fills or strokes text
      */
    __applyText(text: string, x: number, y: number, action: "fill" | "stroke"): void;
    /**
      * Creates a text element, in position x,y
      */
    fillText(text: string, x: number, y: number): void;
    /**
      * Strokes text
      */
    strokeText(text: string, x: number, y: number): void;
    /**
      * No need to implement this for svg.
      */
    measureText(text: string): TextMetrics;
    arc(x: number, y: number, radius: number, start_angle: number, end_angle: number, counterclockwise?: boolean): void;
    ellipse(x: number, y: number, radius_x: number, radius_y: number, rotation: number, start_angle: number, end_angle: number, counterclockwise?: boolean): void;
    private _clip_path;
    /**
      * Generates a ClipPath from the clip command.
      */
    clip(): void;
    drawImage(image: CanvasImageSource, dx: number, dy: number): void;
    drawImage(image: CanvasImageSource, dx: number, dy: number, dw: number, dh: number): void;
    drawImage(image: CanvasImageSource, sx: number, sy: number, sw: number, sh: number, dx: number, dy: number, dw: number, dh: number): void;
    /**
      * Generates a pattern tag
      */
    createPattern(image: CanvasImageSource, _repetition: string | null): CanvasPattern | null;
    getLineDash(): number[];
    setLineDash(segments: number[]): void;
    private _to_number;
    getTransform(): DOMMatrix;
    setTransform(a: number, b: number, c: number, d: number, e: number, f: number): void;
    setTransform(transform?: DOMMatrix2DInit): void;
    setTransform(matrix: DOMMatrix): void;
    resetTransform(): void;
    isPointInPath(x: number, y: number, fill_rule?: CanvasFillRule): boolean;
    isPointInPath(path: Path2D, x: number, y: number, fill_rule?: CanvasFillRule): boolean;
    isPointInStroke(x: number, y: number): boolean;
    isPointInStroke(path: Path2D, x: number, y: number): boolean;
    createImageData(sw: number, sh: number): ImageData;
    createImageData(imagedata: ImageData): ImageData;
    getImageData(_sx: number, _sy: number, _sw: number, _sh: number): ImageData;
    putImageData(imagedata: ImageData, dx: number, dy: number): void;
    putImageData(imagedata: ImageData, dx: number, dy: number, dirtyX: number, dirtyY: number, dirtyWidth: number, dirtyHeight: number): void;
    drawFocusIfNeeded(element: Element): void;
    drawFocusIfNeeded(path: Path2D, element: Element): void;
    scrollPathIntoView(): void;
    scrollPathIntoView(path: Path2D): void;
}
export {};
//# sourceMappingURL=svg.d.ts.map