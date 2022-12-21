import { ContinuousAxis, ContinuousAxisView } from "./continuous_axis";
import { BasicTickFormatter } from "../formatters/basic_tick_formatter";
import { ContinuousTicker } from "../tickers/continuous_ticker";
import * as p from "../../core/properties";
export declare class LinearAxisView extends ContinuousAxisView {
    model: LinearAxis;
}
export declare namespace LinearAxis {
    type Attrs = p.AttrsOf<Props>;
    type Props = ContinuousAxis.Props & {
        ticker: p.Property<ContinuousTicker>;
        formatters: p.Property<BasicTickFormatter>;
    };
}
export interface LinearAxis extends LinearAxis.Attrs {
}
export declare class LinearAxis extends ContinuousAxis {
    properties: LinearAxis.Props;
    __view_type__: LinearAxisView;
    ticker: ContinuousTicker;
    formatters: BasicTickFormatter;
    constructor(attrs?: Partial<LinearAxis.Attrs>);
}
//# sourceMappingURL=linear_axis.d.ts.map