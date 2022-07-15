import { ColumnDataSource } from "./column_data_source";
import { UpdateMode } from "../../core/enums";
import { CallbackLike1 } from "../callbacks/callback";
import { Data } from "../../core/types";
import * as p from "../../core/properties";
import { Arrayable } from "../../core/types";
export declare namespace WebDataSource {
    type Attrs = p.AttrsOf<Props>;
    type Props = ColumnDataSource.Props & {
        max_size: p.Property<number | null>;
        mode: p.Property<UpdateMode>;
        adapter: p.Property<CallbackLike1<WebDataSource, {
            response: Data;
        }, Data> | null>;
        data_url: p.Property<string>;
    };
}
export interface WebDataSource extends WebDataSource.Attrs {
}
export declare abstract class WebDataSource extends ColumnDataSource {
    properties: WebDataSource.Props;
    constructor(attrs?: Partial<WebDataSource.Attrs>);
    get_column(colname: string): Arrayable;
    get_length(): number;
    abstract setup(): void;
    initialize(): void;
    load_data(raw_data: any, mode: UpdateMode, max_size?: number): void;
}
//# sourceMappingURL=web_data_source.d.ts.map