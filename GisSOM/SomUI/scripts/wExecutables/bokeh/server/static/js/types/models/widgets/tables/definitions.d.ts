/// <reference types="slickgrid" />
import { Column } from "@bokeh/slickgrid";
import type { CellEditor } from "./cell_editors";
export declare type Item = {
    [key: string]: any;
};
export declare type ColumnType = Column<Item> & {
    model?: CellEditor;
};
export declare const DTINDEX_NAME = "__bkdt_internal_index__";
//# sourceMappingURL=definitions.d.ts.map