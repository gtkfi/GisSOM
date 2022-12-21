import { TextLikeInput, TextLikeInputView } from "./text_like_input";
import * as p from "../../core/properties";
export declare class TextAreaInputView extends TextLikeInputView {
    model: TextAreaInput;
    protected input_el: HTMLTextAreaElement;
    connect_signals(): void;
    protected _render_input(): void;
    render(): void;
}
export declare namespace TextAreaInput {
    type Attrs = p.AttrsOf<Props>;
    type Props = TextLikeInput.Props & {
        cols: p.Property<number>;
        rows: p.Property<number>;
    };
}
export interface TextAreaInput extends TextAreaInput.Attrs {
}
export declare class TextAreaInput extends TextLikeInput {
    properties: TextAreaInput.Props;
    __view_type__: TextAreaInputView;
    constructor(attrs?: Partial<TextAreaInput.Attrs>);
}
//# sourceMappingURL=textarea_input.d.ts.map