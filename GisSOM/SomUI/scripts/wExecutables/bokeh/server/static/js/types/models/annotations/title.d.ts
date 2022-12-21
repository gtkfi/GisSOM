import { TextAnnotation, TextAnnotationView } from "./text_annotation";
import { VerticalAlign, TextAlign } from "../../core/enums";
import { Size, Layoutable } from "../../core/layout";
import { Panel } from "../../core/layout/side_panel";
import * as mixins from "../../core/property_mixins";
import * as p from "../../core/properties";
export declare class TitleView extends TextAnnotationView {
    model: Title;
    visuals: Title.Visuals;
    layout: Layoutable;
    panel: Panel;
    protected _get_location(): [number, number];
    protected _render(): void;
    protected _get_size(): Size;
}
export declare namespace Title {
    type Attrs = p.AttrsOf<Props>;
    type Props = TextAnnotation.Props & {
        text: p.Property<string>;
        vertical_align: p.Property<VerticalAlign>;
        align: p.Property<TextAlign>;
        offset: p.Property<number>;
        standoff: p.Property<number>;
    } & Mixins;
    type Mixins = mixins.Text & mixins.BorderLine & mixins.BackgroundFill;
    type Visuals = TextAnnotation.Visuals;
}
export interface Title extends Title.Attrs {
}
export declare class Title extends TextAnnotation {
    properties: Title.Props;
    __view_type__: TitleView;
    constructor(attrs?: Partial<Title.Attrs>);
}
//# sourceMappingURL=title.d.ts.map